# 小红书文案转图片 Skill 设计文档

**日期**: 2026-02-14  
**状态**: 已确认

---

## 1. 概述

将小红书文案通过 HTML 模板 + 脚本渲染为可直接发布的图片，不依赖大模型生成图片。采用混合型架构：脚本负责核心渲染逻辑，SKILL.md 描述工作流与调用方式。

---

## 2. 目录结构

```
xhs-copy-to-image/
├── SKILL.md                    # 主入口：触发条件、用法、参数
├── reference.md                 # 模板变量、尺寸规范、常见问题
├── templates/                   # HTML 模板
│   ├── minimal.html
│   ├── cute.html
│   └── ...
├── scripts/
│   ├── split_content.py        # 文案分割
│   ├── render_images.py        # 模板 + 内容 → PNG
│   └── batch_export.py         # 批量处理（可选）
└── references/
    └── canvas.md               # 小红书尺寸、安全区、比例
```

- SKILL.md 控制在 ~500 行内
- scripts/ 承担核心逻辑，Agent 以执行脚本为主
- templates/ 为独立 HTML 文件，占位符如 `{{content}}`、`{{title}}`

---

## 3. SKILL.md 核心设计

### description

```yaml
description: "Converts Xiaohongshu copywriting into publish-ready images via HTML templates and scripts. No AI image generation. Use when user mentions '文案转图片', '小红书配图', 'XHS copy to image', or needs script-based text-to-image for Little Red Book."
```

### Progress Checklist

```
- [ ] Step 1: Parse input (file path or pasted content)
- [ ] Step 2: Mode check (quick vs guided)
- [ ] Step 3a Quick: Run split + render with defaults
- [ ] Step 3b Guided: Confirmation 1 - Split preview → Confirmation 2 - Template choice → Run
- [ ] Step 4: Output location + preview summary
```

### Progressive Disclosure

- 主流程、参数、错误处理 → SKILL.md
- 模板变量、尺寸、高级配置 → reference.md
- 模板文件 → templates/（按需读取）

---

## 4. 脚本设计

### split_content.py

- **输入**: 文案文件路径或 stdin
- **输出**: JSON，每块含 `text`、`index`，可选 `emoji`、`role`
- **策略**: 按字数均匀分 / 按段落分 / 按 `---` 分页
- **参数**: `--blocks N` 指定块数

### render_images.py

- **输入**: `blocks.json` + `--template <name>` + `--output <dir>`
- **流程**: 读模板 → 填充 → html2image → 输出 PNG
- **依赖**: 在 SKILL.md 中说明（如 `pip install html2image`）

### 模板变量

| 变量 | 说明 |
|------|------|
| `{{content}}` | 当前块文本 |
| `{{title}}` | 主标题 |
| `{{index}}` | 序号 1/2/3... |
| `{{total}}` | 总张数 |
| `{{emoji}}` | 可选装饰 |

### 错误处理

- 模板不存在 → 提示可用模板列表
- 输出目录无写权限 → 提示指定其他路径
- html2image 失败 → 提示检查浏览器路径

---

## 5. 交互逻辑：可切换模式

### 模式判断

| 用户表达 | 模式 | 行为 |
|----------|------|------|
| "把这篇文案做成图" / "文案转图片" | 快速 | 默认参数直接跑 |
| "我想自己选模板" / "有哪些模板" | 引导 | 进入分步确认 |
| "先看看怎么分" / "分几张图合适" | 引导 | 展示分割预览 |
| "用 cute 模板" / "分成 5 张" | 快速 | 显式参数，直接执行 |
| 未说明偏好、只给内容 | 快速 | 默认参数 |

### 快速模式

```
内容 → 默认参数（模板 minimal、自动分割 3–5 张）→ 执行 → 输出路径 + 预览
```

失败时：提示原因 + 询问是否进入引导模式排查。

### 引导模式

**确认点 1 - 分割策略**
- 展示：预估块数、每块字数、内容预览
- 选项：接受 / 修改块数 / 手动分页（如 `---`）
- 工具：AskUserQuestion（如有）

**确认点 2 - 模板选择**
- 展示：模板列表 + 描述
- 选项：minimal / cute / warm / … 或默认
- 工具：AskUserQuestion

**确认点 3 - 执行前**（可选）
- 展示：模板 + 块数 + 输出目录
- 选项：执行 / 返回修改

### 偏好持久化（可选）

- 路径：`.xhs-copy-to-image/preferences.md` 或项目级
- 内容：默认模板、默认输出目录、默认块数
- 首次使用：询问并写入；快速模式优先读取

### 异常回退

| 情况 | 行为 |
|------|------|
| 内容过长/过短 | 提示建议块数，询问接受或手动指定 |
| 模板不存在 | 列出可用模板，请用户重选 |
| 渲染失败 | 提示检查依赖，提供引导模式入口 |
| 输出目录不可写 | 提示并建议其他路径 |

---

## 6. create-skill 对应

| 建议 | 落实 |
|------|------|
| SKILL.md < 500 行 | 主流程 + 参数约 300 行 |
| 脚本解决真实问题 | split/render 承担核心逻辑 |
| 明确执行 vs 参考 | Agent 执行脚本，不现场写渲染代码 |
| 避免过多选项 | 默认 1 模板 + 1 分割策略，参数扩展 |
| 术语统一 | block / template / render |

---

## 7. 下一步

- [ ] 创建 skill 目录结构
- [ ] 编写 SKILL.md
- [ ] 实现 split_content.py
- [ ] 实现 render_images.py
- [ ] 至少 2 个基础模板（minimal, cute）
- [ ] reference.md + canvas.md
