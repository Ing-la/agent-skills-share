# Agent Skills Share

> Daily sharing of Agent Skills, generating Xiaohongshu copywriting and technical analysis documents.

## Introduction

This is a tool for generating Xiaohongshu content about Agent Skills. It intelligently selects skills, analyzes their functionality and technical implementation, and generates content copywriting and technical analysis documents suitable for the Xiaohongshu platform.

## Features

- 🎯 **Smart Recommendations**: Intelligently recommends skill directions based on history
- 📝 **Auto Generation**: Automatically generates Xiaohongshu copywriting and technical analysis documents
- 🔍 **Deep Analysis**: Optionally installs skills for code-level deep analysis
- 💬 **Experience Feedback**: Supports collecting actual usage experience and updating content
- 📊 **Source Tracking**: Complete tracking of information sources for each document

## Quick Start

Use the `/skill` command or invoke `@skill-share` skill to generate daily content.

## Directory Structure

```
Agent-skills-share/
├── README.md                    # Project introduction (this file)
├── templates/                  # Template directory
│   ├── xhs_template.md        # Default template (if multiple templates exist, will ask for selection)
│   └── [other templates].md   # Supports multiple templates, e.g., xhs_template_minimal.md
├── daily-posts/                 # Daily content directory
│   ├── RECORD.md               # Detailed records of all skills
│   └── YYYY-MM-DD-skill-name/  # Content for each skill
│       ├── draft.md            # Draft (with frontmatter)
│       ├── final.md            # Final copywriting (with frontmatter)
│       ├── technical-review.md # Technical analysis (with frontmatter)
│       ├── assets/            # Screenshots, recordings, etc.
│       └── workspace/         # Experimental files
└── .cursor/skills/skill-share/ # Main skill file
    └── SKILL.md
```

**Template Selection Logic**:
- Priority: Use templates in project directory `templates/`
- If multiple templates found, list and ask for selection
- If no template in project directory, use skill's default template

## Workflow

1. **Skill Selection**: Smart recommendation → User selects direction → Returns 3 options → User chooses
2. **Template Selection**: If multiple templates exist, ask for selection (otherwise auto-use)
3. **Draft Generation**: Generate draft.md based on skills.sh webpage information
4. **Installation Decision**: Ask if installation is needed for deep analysis
5. **Deep Analysis**: Optionally install skill, generate technical-review.md
6. **Experience Feedback**: Optionally experience skill, collect feedback and update final.md

## Document Description

- **draft.md**: Draft generated based on skills.sh page information
- **final.md**: Final copywriting, may be updated based on draft + technical analysis + experience feedback
- **technical-review.md**: Technical analysis document (800-1200 words), if installation is selected

All documents include frontmatter to track information sources.

## Details

View [daily-posts/RECORD.md](daily-posts/RECORD.md) for detailed records of all shared skills.

## License

MIT
