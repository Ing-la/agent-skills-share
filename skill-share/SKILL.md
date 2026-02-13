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

Generate daily Xiaohongshu (小红书) content about Agent Skills. Intelligently selects skills, generates copywriting, and optionally installs for deep technical analysis.

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

3. **CRITICAL WAIT POINT - END OF STEP 1**:
   - **STOP HERE. DO NOT proceed to Step 2.**
   - **WAIT for user input**: Accept A/B/C/D (case-insensitive) or custom direction text
   - **DO NOT proceed** until user provides explicit choice
   - **DO NOT assume** user's selection or proceed automatically

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

2. **CRITICAL WAIT POINT - END OF STEP 2**:
   - **STOP HERE. DO NOT proceed to Phase 2.**
   - **Ask user**: "请选择技能 / Please select a skill: [1/2/3]"
   - **WAIT for user input**: Accept 1, 2, or 3 (as number or text)
   - **DO NOT proceed** until user selects one of the options
   - **DO NOT assume** user's choice or proceed automatically

### Phase 2: Draft Generation

1. **Fetch detailed skill information**:
   - Get full skill page from skills.sh: `https://skills.sh/<owner>/<repo>/<skill-name>` (selected in Phase 1 Step 2)
   - Extract detailed information: name, description, install count, GitHub link, owner/repo, full description, features
   - **Note source clearly** in draft frontmatter: "信息来源: skills.sh页面"

2. **Select Template**:
   - **Priority 1**: Check `Agent-skills-share/templates/` directory for available templates
     - If multiple templates found (e.g., `xhs_template.md`, `xhs_template_minimal.md`):
       - List available templates with brief descriptions
       - **CRITICAL: STOP and ASK user**: "请选择模板 / Please select a template: [list options with numbers 1/2/3...] or [d] for default"
       - **WAIT for user input**: Accept number (1/2/3...) or 'd' for default
       - **DO NOT proceed** until user selects a template or explicitly confirms using default
       - **DO NOT assume** default without user confirmation
     - If only one template found → use it automatically
   - **Priority 2**: If no template in project directory, try to find skill's default template:
     - Check `.cursor/skills/skill-share/templates/xhs_template.md` (if exists)
     - Or check `.agents/skills/skill-share/templates/xhs_template.md` (if exists)
     - Use the first found template
   - **Priority 3**: If still not found, inform user and proceed without template (generate from scratch)
   - **Priority order**: Project templates > Skill default template (from installation directory)

3. **Generate draft.md**:
   - Create directory: `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/`
   - **Note**: Do NOT create `workspace/` directory at this stage
   - Path: `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/draft.md`
   - Use selected template
   - **Add frontmatter**:
     ```markdown
     ---
     信息来源: skills.sh页面
     生成时间: YYYY-MM-DD HH:MM:SS
     ---
     ```
   - Structure: Title, Opening, Functions, Audience, Installation command, Tags
   - Length: 300-500 words, accessible style (not hardcore technical)

### Phase 3: Installation Decision

**CRITICAL: STOP and ASK user**: "是否需要安装完成更详细的技术分析和体验反馈？/ Do you want to install the skill for detailed technical analysis and experience feedback? [y/n]"
- **WAIT for user input**: Accept y/yes/是 or n/no/否 (case-insensitive)
- **DO NOT proceed** until user provides explicit answer
- **DO NOT assume** or proceed automatically

**If user answers "n" or "否" or "no"**:
- Copy `draft.md` to `final.md`
- **Add frontmatter** to final.md: "信息来源: draft.md (直接复制), 更新说明: 未进行安装和技术分析"
- Generate brief `technical-review.md` (skills.sh info only, 50-200 words, note: "未进行深度代码分析")
- **Update RECORD.md** → **End**

**If user answers "y" or "是" or "yes"** → Phase 4

### Phase 4: Installation

**CRITICAL: STOP and ASK user**: "你自己安装还是我安装？/ Do you want to install it yourself or should I install it? [m/a] (m=myself/我自己, a=auto/你安装)"
- **WAIT for user input**: Accept m/myself/我自己 or a/auto/你安装 (case-insensitive)
- **DO NOT proceed** until user provides explicit choice
- **DO NOT assume** or proceed automatically

**If user answers "m" or "myself" or "我自己"**:
- Provide command: `npx skills add <owner/repo> --skill <skill-name>`
- Brief guide: "安装过程中会询问安装到哪些agent，可以选择多个或全部 / During installation, you'll be asked which agents to install to, you can select multiple or all"
- Say: "安装完成后告诉我，我会继续进行分析 / Please tell me when installation is complete, and I'll continue the analysis"
- **CRITICAL: STOP and WAIT for user confirmation** - Accept: "完成/done/y/yes" or similar confirmation
- **DO NOT proceed** until user confirms installation is complete

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

3. **CRITICAL: STOP and ASK user**: "是否要体验这个skill？/ Do you want to experience this skill? [y/n]"
   - **WAIT for user input**: Accept y/yes/是 or n/no/否 (case-insensitive)
   - **DO NOT proceed** until user provides explicit answer
   - **DO NOT assume** or proceed automatically

**If user answers "n" or "否" or "no"**:
- **Generate final.md**: Enhance draft.md with technical-review.md insights:
  - Read `draft.md` and `technical-review.md`
  - Add technical highlights from code analysis
  - Refine function descriptions based on deeper understanding
  - Update target audience if needed
  - Enhance installation command section
  - **Important**: final.md is still Xiaohongshu copywriting, not technical doc
  - Maintain accessible style, supplement not merge
- **Add frontmatter**: "信息来源: draft.md + technical-review.md技术分析, 更新说明: 基于技术分析文档更新，未进行实际体验"
- **Update RECORD.md** → **End**

**If user answers "y" or "是" or "yes"**:
- **Create workspace directory**:
  - Create `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/workspace/` directory
- **Inform user**:
  - Say: "已创建 workspace 目录，你可以在 `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>/workspace/` 目录下进行体验和测试。/ Workspace directory created. You can test the skill in the workspace directory."
  - Say: "体验完成后告诉我，我会收集反馈并更新文案 / Please tell me when you're done experiencing, and I'll collect feedback and update the copywriting"
- **CRITICAL: STOP and WAIT for user confirmation** - Accept: "完成/done/y/yes" or similar confirmation
- **DO NOT proceed** to Phase 6 until user confirms experience is complete

### Phase 6: Feedback & Final Update

**Context**: User chose to experience the skill in Phase 5, completed experience, and confirmed completion. At this point:
- `technical-review.md` exists (generated in Phase 5)
- `final.md` does NOT exist yet (will be created in this phase)

**CRITICAL: STOP and ASK user**: "是否要更新文案？/ Do you want to update the copywriting? [y/n]"
- **WAIT for user input**: Accept y/yes/是 or n/no/否 (case-insensitive)
- **DO NOT proceed** until user provides explicit answer
- **DO NOT assume** or proceed automatically

**If user answers "n" or "否" or "no"**:
- **Generate final.md** (enhance draft.md with technical-review.md insights, same logic as Phase 5 "否" branch):
  - Read `draft.md` and `technical-review.md`
  - Add technical highlights from code analysis
  - Refine function descriptions based on deeper understanding
  - Update target audience if needed
  - Enhance installation command section
  - Maintain accessible style, supplement not merge
- **Add frontmatter**: "信息来源: draft.md + technical-review.md技术分析, 更新说明: 基于技术分析文档更新，已体验但未收集反馈"
- **Update RECORD.md** → **End**

**If user answers "y" or "是" or "yes"**:
- **Generate final.md first** (if not exists, use same enhancement logic as "否" branch above):
  - Read `draft.md` and `technical-review.md`
  - Enhance draft.md with technical-review.md insights
  - Add frontmatter: "信息来源: draft.md + technical-review.md技术分析, 更新说明: 基于技术分析文档更新，准备收集体验反馈"
- **Collect feedback**:
  - **CRITICAL: STOP and ASK user**: "选择反馈方式 / Please select feedback method: [1/2] (1=自由输入/free input, 2=回答预设问题/preset questions)"
  - **WAIT for user input**: Accept 1 or 2 (as number or text)
  - **DO NOT proceed** until user selects an option
  - Option 1: User provides feedback freely
  - Option 2: Ask one by one:
    - "这个skill最让你惊喜的是什么？"
    - "有什么使用上的痛点吗？"
    - "实际使用场景是什么？"
- **Update final.md** with feedback:
  - Maintain original structure, update content
  - Can add: actual usage experience, real scenarios, notes, improvement suggestions
- **Update frontmatter**: "信息来源: draft.md + technical-review.md技术分析 + 实际体验反馈, 更新说明: 基于技术分析和实际体验更新"
- **Update RECORD.md** → **End**

## Document Structure

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

- **CRITICAL: Always wait for user input**: When asking questions or presenting options, **STOP and WAIT** for explicit user response. **NEVER proceed automatically** or assume user's choice.
- **Smooth workflow**: No retries, use available info gracefully
- **Accessibility first**: Not always hardcore technical, focus on user-friendly content
- **User control**: User decides installation and experience - **always wait for explicit confirmation**
- **Clear sources**: Always note information source in frontmatter
- **Flexible feedback**: Support both free input and guided questions
- **Explicit waits**: Use phrases like "STOP and WAIT", "DO NOT proceed", "CRITICAL" to emphasize waiting points

## Error Handling

- **Installation fails**: Inform user, proceed with web info only
- **File read fails**: Use web info, note limitation in technical-review.md

## Usage

When user says `/skill` or requests daily skill content:
1. Start Phase 1: Skill Selection
2. Proceed through phases sequentially based on user choices
3. Generate documents based on available information
4. Update RECORD.md at workflow end
5. Confirm completion with user
