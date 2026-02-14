# Agent Skills Share

> 每天为 Agent Skills 生成小红书种草内容，从选 skill、写文案到配图一条龙。

## 简介

本项目帮助你持续产出 Agent Skills 相关的小红书内容：从 [skills.sh](https://skills.sh) 选 skill、生成初稿、技术拆解，再到文案转配图，全部由 Agent 辅助完成。内含两个可独立安装的 Skill，可在 [skills.sh](https://skills.sh/Ing-la/agent-skills-share) 检索到。

## 功能

- **skill-share**：选 skill、抓取信息、生成 draft/final 文案，支持深度技术分析
- **xhs-render**：文案转配图，多套模板可选，输出 3:4 小红书规格 PNG

## 快速开始

### 安装 Skill

两个 skill 可分别安装，按需选择：

```bash
# 生成小红书文案
npx skills add Ing-la/agent-skills-share --skill skill-share

# 文案转配图
npx skills add Ing-la/agent-skills-share --skill xhs-render
```

安装后技能会出现在 `.cursor/skills/`（或对应 agent 目录）。

### 使用

- **skill-share**：在 Cursor 中 @skill-share 或输入 `/skill`，按流程选 skill、生成文案
- **xhs-render**：在已有文案目录（如 `Agent-skills-share/daily-posts/xxx/`）下，让 Agent 调用 xhs-render 即可完成文案 → blocks.json → 配图

## 项目结构

```
├── skills/                 # 可被 skills.sh 检索的两个 skill 源码
│   ├── skill-share/
│   └── xhs-render/
├── Agent-skills-share/      # 日常生成的内容（文案、配图等）
└── README.md
```

## 链接

- [skills.sh](https://skills.sh/Ing-la/agent-skills-share) - 在 Vercel 技能目录中查看与安装
- [GitHub](https://github.com/Ing-la/agent-skills-share)

## 许可

MIT
