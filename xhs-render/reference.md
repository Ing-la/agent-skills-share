# xhs-render Reference

流程与使用详见 **SKILL.md**。本文档保留实现相关细节。

## 输出路径

- 输出目录：`<文案目录>/xhs-render/from-{source}-v{N}/`，含 blocks.json、PNG、xhs-copy.md

## 画布尺寸

3:4 比例，输出 1242×1660 像素。渲染时画布高度 1800px，裁切取顶部 1242×1660 避免底部留白。

## 模板变量

| 变量 | 说明 |
|------|------|
| `{{content}}` | 当前块文本 |
| `{{title}}` | 主标题 |
| `{{role}}` | cover / content / ending |
| `{{EMOJI_BLOCK}}` | emoji 区块，有值则渲染 div，空则无 |
| `{{TITLE_BLOCK}}` | 标题+装饰（部分模板含圆点等） |

## 渲染实现

脚本使用 `html_file` 而非 `html_str`：html2image 对 `html_str` 会再包一层 `<html><body>...</body></html>`，导致完整文档被嵌套、布局错位、底部露出默认背景色。通过将 HTML 写入临时文件后以 `html_file` 加载，避免嵌套。

## 模板背景色（兜底）

每个模板在 `<style>` 内声明 `/* xhs-page-bg: #RRGGBB */`，用于 `--default-background-color` 与 html 兜底。未声明时从 body background 取第一个 hex。
