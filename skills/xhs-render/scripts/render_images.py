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


def build_block_html(block: dict, template: str) -> str:
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
    return _inject_viewport_styles(html)


def _inject_viewport_styles(html: str) -> str:
    """注入 viewport 约束，避免截到浏览器 chrome。"""
    styles = (
        f"html,body{{margin:0!important;padding:0!important;overflow:hidden!important;}}"
        f"html{{width:{WIDTH}px!important;height:{HEIGHT}px!important;}}"
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
    parser.add_argument("-t", "--template", default="minimal", help="Template name")
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

    hti = Html2Image(size=(WIDTH, HEIGHT), output_path=str(out_dir))
    if (exe := _find_browser()):
        hti.browser.executable = exe

    output_paths = []
    for block in blocks:
        if is_tags_only_block(block):
            print(f"Skipped tags-only block {block.get('index')}", file=sys.stderr)
            continue

        html = build_block_html(block, template)
        fname = f"{block.get('index', 0):02d}-{block.get('role', 'content')}.png"
        out_path = out_dir / fname

        try:
            hti.screenshot(html_str=html, save_as=fname, size=(WIDTH, HEIGHT))
            _crop_to_canvas(out_path)
            output_paths.append(str(out_path))
            print(f"Rendered: {out_path}", file=sys.stderr)
        except Exception as e:
            print(f"Error rendering block {block.get('index')}: {e}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps({"output_dir": str(out_dir), "files": output_paths}))


if __name__ == "__main__":
    main()
