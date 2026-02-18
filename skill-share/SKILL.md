---
name: skill-share
description: "Generate daily Xiaohongshu content about Agent Skills. Selects a skill from skills.sh, generates initial copywriting, and optionally installs for deep technical analysis."
license: MIT
metadata:
  author: Ing-la
  version: "1.0.0"
---

# Skill Share - Daily Agent Skills Content Generator

## Overview

Generate daily Xiaohongshu (小红书) content about Agent Skills. Intelligently selects skills, generates copywriting, and optionally installs for deep technical analysis. 可与 xhs-render 配合，将 final.md 转为配图。

## Workflow

### Phase 0: Initialization (Smart Detection)

**Before starting any workflow, ensure the working directory structure exists:**

1. **Check if `Agent-skills-share/` directory exists**:
   - If exists → continue to Phase 1
   - If not exists → proceed to initialization

2. **Initialize directory structure** (if needed):
   - Create `Agent-skills-share/` directory
   - Create `Agent-skills-share/daily-posts/` directory
   - Create `Agent-skills-share/templates/` directory (if not exists)
   - Create `Agent-skills-share/daily-posts/RECORD.md` with initial content:
     ```markdown
     # Agent Skills 分享记录
     
     > 本文件记录所有已分享的Agent Skill详细信息，包括信息来源、生成时间、更新说明等。
     
     ## 记录格式
     
     每个skill记录包含：
     - Skill名称和链接
     - 状态（已完成/进行中）
     - draft.md的信息来源和链接（如果存在）
     - final.md的信息来源和链接（如果存在）
     - technical-review.md的信息来源和链接（如果存在）
     
     **注意**：如果某个文档未生成或不存在，该条目将不会出现在记录中（只列出实际存在的文档）。
     
     ---
     
     ## 已分享Skills
     
     （记录将自动添加到这里）
     ```
   - Create `Agent-skills-share/README.md` (copy from skill template or create basic version)
   - Inform user: "已创建 Agent-skills-share 目录结构，可以开始使用了"

3. **Continue to Phase 1**

### Phase 1: Skill Selection

**STEP 1: Recommend Direction**
1. **Read history and analyze**:
   - Read `Agent-skills-share/daily-posts/RECORD.md` to track history
   - Analyze recent posts for diversity:
     - Last 3 popular → recommend niche/domain-specific
     - Last 3 technical → recommend creative/design
     - Default: popular skills

2. **Present options**:
   - Present: 1 recommended + 4 alternatives (A/B/C/D)
   - Format: Clear list with labels (A/B/C/D) and descriptions
   - **Ask user**: "请选择方向 / Please select direction: [A/B/C/D] or type your custom direction"

3. **【Wait Point】** 请选择方向 [A/B/C/D] 或输入自定义方向

**STEP 2: Search & Present** (ONLY START AFTER USER SELECTS DIRECTION)
1. **Search skills based on user's direction selection**:
   - Fetch from https://skills.sh/ based on user's choice from Step 1
   - Extract: name, description, install count
   - Present top 3 matches with format:
     ```
     1. [skill-name] - [core description] (安装数: X.XK)
       - [key feature 1]
       - [key feature 2]
       - 适合 [target audience]
     ```

2. **【Wait Point】** 请选择技能 [1/2/3]

### Phase 2: Draft Generation

1. **Fetch detailed skill information**:
   - Get full skill page from skills.sh: `https://skills.sh/<owner>/<repo>/<skill-name>` (selected in Phase 1 Step 2)
   - Extract detailed information: name, description, install count, GitHub link, owner/repo, full description, features
   - **Note source clearly** in draft frontmatter: "信息来源: skills.sh页面"

2. **Select 文案风格模板**（.md 文件，与 xhs-render 的配图渲染模板 .html 不同）：
   - **Scan both sources**：`.cursor/skills/skill-share/templates/`、`Agent-skills-share/templates/`（如 xhs-cute.md、xhs_template_xxx.md 若存在）
   - **合并去重**：将两处找到的 .md 模板合并为一份列表，按文件名排序后展示
   - **交互**：
     - 若找到 0 个 → 直接按内容清单生成，不使用模板
     - 若找到 1 个 → 自动使用
     - 若找到 2 个及以上 → **【Wait Point】** 请选择风格 [1/2/3...] 对应各模板

3. **Generate draft.md**:
   - Create directory: `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/`
   - **Note**: Do NOT create `workspace/` directory at this stage
   - Path: `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/draft.md`
   - **Use template as style reference** (not fill-in): Template shows tone and must-have elements; section structure and naming are yours to decide based on skill characteristics.
   - **Must include**: hook opening, features/highlights, target audience, install command, developer credits, hashtags. Optionally add: usage notes, technical details, hands-on feedback.
   - **Output format: XHS-ready** — use `【小节名】` for sections (no `##`), no `**` for bold, links as `[text](url)`, install command on its own line without code fences. Emoji allowed in body.
   - **Add frontmatter**:
     ```markdown
     ---
     信息来源: skills.sh页面
     生成时间: YYYY-MM-DD HH:MM:SS
     ---
     ```
   - Length: 300-500 words, accessible style (not hardcore technical)

### Phase 3: Installation Decision

**【Wait Point】** 是否需要安装完成更详细的技术分析？ [y/n]

**If user answers "n" or "否" or "no"**:
- Copy `draft.md` to `final.md` (draft is already XHS-ready)
- **Add frontmatter** to final.md: "信息来源: draft.md (直接复制), 更新说明: 未进行安装和技术分析"
- Generate brief `technical-review.md` (skills.sh info only, 50-200 words, note: "未进行深度代码分析")
- **Update RECORD.md** → **End**

**If user answers "y" or "是" or "yes"** → Phase 4

### Phase 4: Installation

**【Wait Point】** 你自己安装还是我安装？ [m/a] (m=我自己, a=你安装)

**If user answers "m" or "myself" or "我自己"**:
- Provide command: `npx skills add <owner/repo> --skill <skill-name>`
- Brief guide: "安装过程中会询问安装到哪些agent，可以选择多个或全部 / During installation, you'll be asked which agents to install to, you can select multiple or all"
- Say: "安装完成后告诉我，我会继续进行分析"
- **【Wait Point】** 等待用户确认安装完成

**If user answers "a" or "auto" or "你安装"**:
- Run: `npx skills add <owner/repo> --skill <skill-name> --agent cursor --yes`
- This installs to `.agents/skills/<skill-name>/`
- **Copy to target**:
  - Read `SKILL.md` content and write to `.cursor/skills/<skill-name>/SKILL.md`
  - If `scripts/` exists: Copy recursively to `.cursor/skills/<skill-name>/scripts/`
    - Windows: Use PowerShell `Copy-Item -Recurse`
    - Unix: Use `cp -r`
  - Copy other files (README.md, etc.) if they exist
- Clean up: Remove `.agents/skills/<skill-name>/`

**After installation (both branches)**:
- Verify: Check `.cursor/skills/<skill-name>/SKILL.md` exists
- If verified → Phase 5
- If verification fails: Ask user to confirm or proceed with web info only

### Phase 5: Deep Analysis

1. **Read & Analyze**:
   - Read `.cursor/skills/<skill-name>/SKILL.md` completely
   - Extract: name, description, workflow, usage instructions
   - If `scripts/` exists: List code files (.py, .js, .ts, .sh, etc.), analyze each:
     - Code volume, tech stack, implementation highlights, code quality

2. **Generate technical-review.md**:
   - Path: `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/technical-review.md`
   - **Add frontmatter**: "信息来源: 已安装skill分析 (.cursor/skills/<skill-name>/SKILL.md + scripts/)"
   - Structure:
     - Core Function (100-150 words)
     - Design Philosophy (200-300 words)
     - Technical Implementation (300-400 words)
     - Use Cases & Limitations (100-150 words)
     - Technical Evaluation (100-150 words)
     - Developer Info (50 words, optional)
   - Length: 800-1200 words, concise and professional

3. **【Wait Point】** 是否要体验这个 skill？ [y/n]

**If user answers "n" or "否" or "no"**:
- **Generate final.md**（按 Document Structure 中的 generate_final.md 规则），frontmatter 更新说明：基于技术分析文档更新，未进行实际体验
- **Update RECORD.md** → **End**

**If user answers "y" or "是" or "yes"**:
- **Create workspace directory**:
  - Create `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/workspace/` directory
- **Inform user**:
  - Say: "已创建 workspace 目录，你可以在 `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/workspace/` 目录下进行体验和测试。/ Workspace directory created. You can test the skill in the workspace directory."
  - Say: "体验完成后告诉我，我会收集反馈并更新文案"
- **【Wait Point】** 等待用户确认体验完成

### Phase 6: Feedback & Final Update

**Context**: User chose to experience the skill in Phase 5, completed experience, and confirmed completion. At this point:
- `technical-review.md` exists (generated in Phase 5)
- `final.md` does NOT exist yet (will be created in this phase)

**【Wait Point】** 是否要更新文案？ [y/n]

**If user answers "n" or "否" or "no"**:
- **Generate final.md**（按 generate_final.md 规则），frontmatter 更新说明：基于技术分析文档更新，已体验但未收集反馈
- **Update RECORD.md** → **End**

**If user answers "y" or "是" or "yes"**:
- **Generate final.md first**（按 generate_final.md 规则），frontmatter 更新说明：基于技术分析文档更新，准备收集体验反馈
- **Collect feedback**:
  - **【Wait Point】** 选择反馈方式 [1/2] (1=自由输入, 2=回答预设问题)
  - Option 1: User provides feedback freely
  - Option 2: Ask one by one:
    - "这个skill最让你惊喜的是什么？"
    - "有什么使用上的痛点吗？"
    - "实际使用场景是什么？"
- **Update final.md** with feedback:
  - Maintain original structure, update content
  - Can add: actual usage experience, real scenarios, notes, improvement suggestions
  - Keep XHS-ready format
- **Update frontmatter**: "信息来源: draft.md + technical-review.md技术分析 + 实际体验反馈, 更新说明: 基于技术分析和实际体验更新"
- **Update RECORD.md** → **End**

## Document Structure

**generate_final.md 规则**（draft + technical-review → final）：
- 读取 `draft.md` 与 `technical-review.md`
- 融入技术分析亮点，精炼功能描述，必要时更新目标受众、安装命令
- 输出 XHS-ready：`【】` 小节，无 `##`/`**`，链接 `[文字](url)`，安装命令独立成行
- 保持口语化，补充不合并；frontmatter 更新说明由调用方指定

**final.md**:
- XHS-ready，可直接复制到小红书。用 `【小节名】` 作分隔，不用 `##`/`**`，链接 `[文字](url)`，安装命令独立成行无代码块。

**Frontmatter format** (all documents):
```markdown
---
信息来源: [actual source]
生成时间: YYYY-MM-DD HH:MM:SS
[更新说明: optional, context-specific]
---
```

**RECORD.md update** (at workflow end):
- File: `Agent-skills-share/daily-posts/RECORD.md`
- Check which files exist: `draft.md`, `final.md`, `technical-review.md`
- Add entry (only list existing files):
  ```markdown
  ## YYYY-MM-DD - <skill-name>
  
  - **Skill**: [skill-name](https://skills.sh/owner/repo/skill-name)
  - **状态**: ✅ 已完成
  - **draft.md信息来源**: [source] | [链接](daily-posts/YYYY-MM-DD-skill-name/draft.md)
  - **final.md信息来源**: [source] | [链接](daily-posts/YYYY-MM-DD-skill-name/final.md)
  - **technical-review.md信息来源**: [source] | [链接](daily-posts/YYYY-MM-DD-skill-name/technical-review.md)
  ```

## Key Principles

- **【Wait Point】**：遇到标注处必须停止、等待用户输入；不得自动继续或假设用户选择。
- **Smooth workflow**: No retries, use available info gracefully
- **Accessibility first**: Not always hardcore technical, focus on user-friendly content
- **User control**: User decides installation and experience - **always wait for explicit confirmation**
- **Clear sources**: Always note information source in frontmatter
- **Flexible feedback**: Support both free input and guided questions

## Error Handling

- **Installation fails**: Inform user, proceed with web info only
- **File read fails**: Use web info, note limitation in technical-review.md

## Usage

可与 xhs-render 联动：生成 final.md 后，用 xhs-render 将其转为配图。

When user says `/skill` or requests daily skill content:
1. Start Phase 1: Skill Selection
2. Proceed through phases sequentially based on user choices
3. Generate documents based on available information
4. Update RECORD.md at workflow end
5. Confirm completion with user
