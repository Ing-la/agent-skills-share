# xhs-render Reference

## 流程

用户给 Markdown 所在目录或指定文档 → **先选模板（列可选、问用户）** → 定位文档 → 建工作目录 → LLM 设计 blocks.json + xhs-copy → 渲染。

- 文案目录：`Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/` 或用户指定
- 输出：`xhs-render/from-{source}-v1/` 含 blocks.json、PNG、xhs-copy.md
- **文档优先**：`skill-source.md` > 用户指定（final/draft/自定义文件）

## blocks.json Schema

LLM 全权决定分几张、标题、布局等，生成时需遵守：

| 字段 | 必填 | 说明 |
|------|------|------|
| index | ✓ | 1-based 序号，连续 |
| total | ✓ | 总块数 |
| text | ✓ | 当前块正文 |
| title |  | cover 时填主标题 |
| role | ✓ | cover / content / ending |
| emoji |  | 完全由 LLM 决定，空则不渲染 |

## 模板变量

| 变量 | 说明 |
|------|------|
| `{{content}}` | 当前块文本 |
| `{{title}}` | 主标题 |
| `{{role}}` | cover / content / ending |
| `{{EMOJI_BLOCK}}` | emoji 区块，有值则渲染 div，空则无 |
| `{{TITLE_BLOCK}}` | 标题+装饰（ing-minimal 用） |

## 画布尺寸

3:4 比例，1242×1660 像素。

## 可用模板（均为 .html 单文件）

- minimal、cute、notion、bold、warm、ing-minimal、showcase

## 脚本

```bash
# source: final(默认) | draft | custom
python .cursor/skills/xhs-render/scripts/get_output_dir.py <文案目录> --source final
python .cursor/skills/xhs-render/scripts/render_images.py <输出目录>/blocks.json -t minimal -o <输出目录>
```
