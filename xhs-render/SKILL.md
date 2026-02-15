---
name: xhs-render
description: "Converts Xiaohongshu copywriting into publish-ready images via HTML templates and scripts. Integrates with skill-share. No AI image generation. Use when user mentions '文案转图片', '小红书配图', 'XHS copy to image', '渲染 skill-share 的文案', or needs script-based text-to-image for Little Red Book."
license: MIT
metadata:
  version: "1.0.0"
---

# xhs-render — 小红书文案转图 + 配套文案

用户提供需渲染的文案所在目录（或指定文档），Skill 完成：选模板 → 定位文档 → 创建工作目录 → LLM 设计 blocks.json 与 xhs-copy → 渲染成图并写入配套文案。

## 流程

1. **选模板（先与用户交互）**：列出可选模板，询问用户选择，待用户确认后再继续。
   - 可选：ing-minimal、notion、memo
   - 示例：「可选模板：ing-minimal（品牌简约，推荐）、notion（知识卡片风）、memo（备忘录标签风）。请问用哪个？」→ 用户回复后记下，后续用 `-t <所选>`

2. **定位文档**：
   - 用户指定文案目录（如 `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>`）或具体文件
   - **优先顺序**：`skill-source.md` > 用户指定的文档
   - 若目录下有 `skill-source.md`（来自 skill-share Phase 2），优先读它
   - 若用户说「渲染 draft」则读 `draft.md`；说「渲染 final」或未指定则默认 `final.md`
   - 若用户指定其他文档（如 `my-copy.md`），读该文档

3. **创建工作目录**：
   - `python .cursor/skills/xhs-render/scripts/get_output_dir.py <文案目录> --source <source>`
   - source：用户指定 draft 时用 `draft`，指定其他自定义文档时用 `custom`，否则 `final`
   - 输出如 `xhs-render/from-final-v1`、`from-draft-v1`、`from-custom-v1`

4. **LLM 设计 blocks.json 与 xhs-copy**（一次产出）：
   - 读取定位到的文档
   - **角色**：你是小红书配图设计专家，不是简单切分文档。必须真正理解内容、重新设计规划、加工提炼——即使用户给的是结构化文档，也不要偷懒照抄结构，而要按视觉节奏和信息重点重新编排
   - **任务**：从文档中提炼核心信息，设计一套配图（blocks.json）及配套发帖文案（xhs-copy）
   - **blocks.json**：分几张图、每块 title/text/emoji、如何拆合，均由你专业判断。内容少可 2–3 张，某块可无标题无 emoji。避免同一张图内 title 与 emoji 重复。**纯 hashtag 不生成图片**（ending 若只有标签则 role 仍为 ending 但脚本会跳过渲染）
   - **xhs-copy**：与配图配套的发帖文案，XHS-ready 纯文本——无 `##`、`**`、`` ` ``，可直接复制到小红书。链接用 `[文字](url)`。**不含 hashtag**（用户发布时自选）
   - **输出**：写入 `<输出目录>/blocks.json` 与 `<输出目录>/xhs-copy.md`

5. **渲染**：`python .cursor/skills/xhs-render/scripts/render_images.py <输出目录>/blocks.json -t <用户所选模板> -o <输出目录>`

## blocks.json Schema

```json
[
  {"index": 1, "total": N, "text": "...", "title": "...", "role": "cover", "emoji": "✨"},
  {"index": i, "total": N, "text": "...", "title": "", "role": "content", "emoji": ""},
  {"index": N, "total": N, "text": "...", "title": "", "role": "ending", "emoji": "📌"}
]
```

- **role**: cover（仅第 1 块）| content | ending（若仅为 hashtag 则跳过渲染）
- **title、emoji**：均可为空，由你判断
- 脚本按 blocks.json 渲染，纯标签页自动跳过

## xhs-copy 规范

- 纯文本格式，存为 `xhs-copy.md`，内容无 markdown 语法
- 与配图内容一致，可直接复制到小红书作为发帖正文
- 不含 hashtag（用户发布时自选）

## 依赖

- `html2image`（`pip install html2image`）
- Chrome 或 Edge 浏览器

## 模板

| 名称 | 说明 |
|------|------|
| ing-minimal | 品牌感简约，页眉「线—Ing—线」，安利 skill 专用，支持 $$...$$ LaTeX 数学公式（推荐） |
| notion | 井字格背景，知识卡片风，内容直接显示在网格上 |
| memo | 备忘录风格，浅蓝数字标签 + 粗体标题，内容按段落填充、带圆点排版 |

纯标签页自动跳过，无页码。

## 异常与处理

渲染失败时根据错误信息处理：缺 Python → 提示安装；缺 html2image → **询问用户是否安装**，同意后 `pip install html2image` 再重试；pip 安装失败 → 提示可能版本冲突；其他 → 根据报错说明。不做预检查。

脚本、模板、参考文档均在本目录内。
