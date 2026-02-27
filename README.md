# agent-skills-share

> 个人 Agent Skills 分享仓库 · 各类方向的 Cursor Skill 集中在此，同步至 [skills.sh](https://skills.sh) 供社区使用。

## 简介

本仓库包含我维护的多个 Cursor Agent Skills，涵盖内容创作、知识库构建、视觉设计等方向。每个 Skill 均可独立安装，按需选用。

## Skills 一览

| Skill | 功能 | 状态 |
|-------|------|------|
| [skill-share](#skill-share) | 选 skill、生成小红书文案、技术拆解 | ✅ 已上架 skills.sh |
| [xhs-render](#xhs-render) | 文案转配图，输出小红书规格 PNG | ✅ 已上架 skills.sh |
| [content-to-knowledge-base](#content-to-knowledge-base) | 内容转知识库，结构化 Markdown | ✅ 已上架 skills.sh |

---

## skill-share

**选 skill、写文案、技术拆解一条龙**

从 [skills.sh](https://skills.sh) 选 skill → 生成 draft / technical-review / final 文案，支持深度技术分析。可与 xhs-render 联动，将 final 转为配图。

**适用场景**：持续产出 Agent Skills 相关的小红书内容、技术分享、技能评测。

**安装**：`npx skills add Ing-la/agent-skills-share --skill skill-share`

---

## xhs-render

**文案转配图，输出小红书规格 PNG**

将 Markdown 文案转为可发布的配图，基于 HTML 模板 + 脚本渲染，无需 AI 生成。支持多种模板：ing-minimal、ing-notion、ing-skillshare 等。

**适用场景**：文案转图片、小红书配图、与 skill-share 联动产出完整图文内容。

**安装**：`npx skills add Ing-la/agent-skills-share --skill xhs-render`

---

## content-to-knowledge-base

**内容转知识库，结构化 Markdown**

将待整理内容（粘贴或文件）按知识库规范转换，生成可沉淀的 Markdown，并建议保存路径。支持配置模块列表与命名规则，支持从零搭建知识库架构。

**适用场景**：知识库构建、内容规范化、调研材料转结构化文档。

**安装**：`npx skills add Ing-la/agent-skills-share --skill content-to-knowledge-base`

---

## 快速开始

```bash
# 按需安装单个 skill
npx skills add Ing-la/agent-skills-share --skill skill-share
npx skills add Ing-la/agent-skills-share --skill xhs-render
npx skills add Ing-la/agent-skills-share --skill content-to-knowledge-base
```

安装后 Skill 会出现在 `.cursor/skills/`（或对应 agent 目录）。

## 项目结构

```
agent-skills-share/
├── skill-share/              # 选 skill、生成小红书文案
├── xhs-render/               # 文案转配图
├── content-to-knowledge-base/ # 内容转知识库
├── README.md
└── LICENSE
```

## 链接

- [skills.sh](https://skills.sh/Ing-la/agent-skills-share) - 在 Vercel 技能目录中查看与安装
- [GitHub](https://github.com/Ing-la/agent-skills-share)

## 许可

MIT
