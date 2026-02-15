#!/usr/bin/env python3
"""Render XHS copywriting blocks to PNG images via HTML templates."""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_ROOT / "templates"

# XHS 3:4 推荐尺寸
WIDTH, HEIGHT = 1242, 1660

# Windows 浏览器路径（优先 Chrome）
BROWSER_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def load_blocks(path: str) -> list[dict]:
    """从 JSON 加载 blocks。支持 [{}] 或 {"blocks": []} 格式。"""
    p = Path(path)
    if not p.exists():
        print(f"Error: Blocks file not found: {path}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if "blocks" in data:
        return data["blocks"]
    print("Error: Invalid blocks JSON structure", file=sys.stderr)
    sys.exit(1)


def load_template(name: str) -> str:
    """加载模板。优先 {name}.html，回退 {name}/index.html。"""
    for candidate in (TEMPLATES_DIR / f"{name}.html", TEMPLATES_DIR / name / "index.html"):
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    available = sorted({f.stem for f in TEMPLATES_DIR.glob("*.html")} |
                      {d.name for d in TEMPLATES_DIR.iterdir() if d.is_dir() and (d / "index.html").exists()})
    print(f"Error: Template '{name}' not found. Available: {available}", file=sys.stderr)
    sys.exit(1)


def is_tags_only_block(block: dict) -> bool:
    """纯 hashtag 的 ending 块不渲染。"""
    return (block.get("role") == "ending" and
            block.get("text", "").strip().startswith("#") and
            block.get("text", "").count("#") >= 2)


def _extract_page_bg(template: str) -> str:
    """从模板提取页面背景色（用于 html2image 与 html 兜底）。
    优先解析 /* xhs-page-bg: #RRGGBB */，否则取 body background 第一个 hex。
    返回无 # 的六位十六进制，如 fefefe。
    """
    # 显式声明优先
    m = re.search(r"/\*\s*xhs-page-bg:\s*#([0-9a-fA-F]{6})\s*\*/", template)
    if m:
        return m.group(1).upper()
    # 从 body 的 background 取第一个 #RRGGBB
    m = re.search(
        r"body\s*\{[^}]*background[^#]*(#[0-9a-fA-F]{6})",
        template,
        re.DOTALL,
    )
    if m:
        return m.group(1)[1:].upper()  # 去掉 #
    return "FFFFFF"


def build_block_html(block: dict, template: str, page_bg_hex: str) -> str:
    """将 block 填充进模板，返回完整 HTML。"""
    emoji_val = block.get("emoji", "").strip()
    title_val = block.get("title", "").strip()
    emoji_block = f'<div class="emoji">{emoji_val}</div>' if emoji_val else ""
    title_block = (
        f'<div class="title">{title_val}</div>'
        f'<div class="title-dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>'
        if title_val else ""
    )
    html = template
    for k, v in (
        ("EMOJI_BLOCK", emoji_block),
        ("TITLE_BLOCK", title_block),
        ("content", block.get("text", "")),
        ("title", title_val),
        ("index", block.get("index", 0)),
        ("total", block.get("total")),
        ("role", block.get("role", "content")),
    ):
        html = html.replace(f"{{{{{k}}}}}", str(v or ""))
    html = re.sub(r"\{\{[^}]+\}\}", "", html)  # 清除未替换占位符
    return _inject_viewport_styles(html, page_bg_hex)


def _inject_viewport_styles(html: str, page_bg_hex: str = "FFFFFF") -> str:
    """注入 viewport 约束与 html 背景，避免截到浏览器 chrome 或露出黑/白条。"""
    bg = f"#{page_bg_hex}"
    styles = (
        f"html,body{{margin:0!important;padding:0!important;overflow:hidden!important;}}"
        f"html{{width:{WIDTH}px!important;height:{HEIGHT}px!important;background:{bg}!important;}}"
        f"body{{min-width:{WIDTH}px!important;min-height:{HEIGHT}px!important;"
        f"max-width:{WIDTH}px!important;max-height:{HEIGHT}px!important;}}"
    )
    if "<style>" in html:
        return html.replace("<style>", f"<style>{styles}", 1)
    return html.replace("<head>", f"<head><style>{styles}</style>", 1)


def _crop_to_canvas(filepath: Path) -> None:
    """若截图大于目标尺寸，裁切为 WIDTH×HEIGHT。"""
    try:
        from PIL import Image
        img = Image.open(filepath).convert("RGB")
        if img.width >= WIDTH and img.height >= HEIGHT:
            img.crop((0, 0, WIDTH, HEIGHT)).save(filepath, "PNG")
    except ImportError:
        pass
    except Exception:
        pass


def _find_browser() -> str | None:
    """返回首个存在的浏览器路径。"""
    for exe in BROWSER_PATHS:
        if Path(exe).exists():
            return exe
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Render XHS blocks to PNG images")
    parser.add_argument("blocks_file", help="JSON file with blocks")
    parser.add_argument("-t", "--template", default="ing-minimal", help="Template name (ing-minimal, notion)")
    parser.add_argument("-o", "--output", default="xhs-render", help="Output directory")
    args = parser.parse_args()

    blocks = load_blocks(args.blocks_file)
    template = load_template(args.template)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from html2image import Html2Image
    except ImportError:
        print("Error: html2image not installed. Run: pip install html2image", file=sys.stderr)
        sys.exit(1)

    # 从模板提取背景色，避免深色模板出现白条、浅色模板出现黑条
    page_bg = _extract_page_bg(template)
    hti = Html2Image(
        size=(WIDTH, HEIGHT),
        output_path=str(out_dir),
        custom_flags=[
            f"--default-background-color={page_bg}",
            "--hide-scrollbars",
        ],
    )
    if (exe := _find_browser()):
        hti.browser.executable = exe

    # 使用 html_file 而非 html_str：html2image 对 html_str 会再包一层结构，导致嵌套布局、底部黑条
    temp_html_dir = out_dir / ".temp_html"
    temp_html_dir.mkdir(exist_ok=True)

    output_paths = []
    for block in blocks:
        if is_tags_only_block(block):
            print(f"Skipped tags-only block {block.get('index')}", file=sys.stderr)
            continue

        html = build_block_html(block, template, page_bg)
        fname = f"{block.get('index', 0):02d}-{block.get('role', 'content')}.png"
        out_path = out_dir / fname

        try:
            html_path = temp_html_dir / fname.replace(".png", ".html")
            html_path.write_text(html, encoding="utf-8")
            hti.screenshot(html_file=str(html_path), save_as=fname, size=(WIDTH, HEIGHT))
            html_path.unlink(missing_ok=True)
            _crop_to_canvas(out_path)
            output_paths.append(str(out_path))
            print(f"Rendered: {out_path}", file=sys.stderr)
        except Exception as e:
            print(f"Error rendering block {block.get('index')}: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        if temp_html_dir.exists():
            for f in temp_html_dir.iterdir():
                f.unlink(missing_ok=True)
            temp_html_dir.rmdir()
    except OSError:
        pass

    print(json.dumps({"output_dir": str(out_dir), "files": output_paths}))


if __name__ == "__main__":
    main()
