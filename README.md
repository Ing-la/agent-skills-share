# Agent Skills Share

> A skill for generating daily Xiaohongshu (小红书) content about Agent Skills. Automatically selects skills, generates copywriting, and optionally performs deep technical analysis.

## 📦 Install Skill

```bash
npx skills add Ing-la/agent-skills-share --skill skill-share
```

After installation, the skill will be installed to your `.cursor/skills/skill-share/` or `.agents/skills/skill-share/` directory.

## 🚀 Quick Start

When using skill-share, it will automatically create the `Agent-skills-share/` working directory in your project root (if it doesn't exist).

Then use the `/skill` command or invoke `@skill-share` skill to generate daily content.

## 📁 Repository Structure

```
agent-skills-share/
├── skill-share/              # Skill source code (shared on skills.sh)
│   ├── SKILL.md             # Main skill file
│   └── templates/           # Default templates included with skill
│       └── xhs_template.md
├── Agent-skills-share/       # Generated content (pushed to GitHub)
│   ├── daily-posts/         # Daily generated content
│   ├── templates/           # User custom templates
│   └── README.md           # Content documentation
└── README.md                # This file
```

## 🎯 Features

- 🎯 **Smart Recommendations**: Intelligently recommends skill directions based on history
- 📝 **Auto Generation**: Automatically generates Xiaohongshu copywriting and technical analysis documents
- 🔍 **Deep Analysis**: Optionally installs skills for code-level deep analysis
- 💬 **Experience Feedback**: Supports collecting actual usage experience and updating content
- 📊 **Source Tracking**: Complete tracking of information sources for each document
- 🛠️ **Auto Initialization**: Automatically creates necessary working directory structure on first use

## 📖 Usage

For detailed usage instructions and workflow, see [Agent-skills-share/README.md](Agent-skills-share/README.md).

## 🔗 Links

- [GitHub Repository](https://github.com/Ing-la/agent-skills-share) - Source code and documentation
- [skills.sh Page](https://skills.sh/) - Agent Skills Directory
- [Agent-skills-share Content](Agent-skills-share/) - Generated Xiaohongshu content and technical analysis

## 👤 Author & Maintainer

**Ing-la**

- GitHub: [@Ing-la](https://github.com/Ing-la)
- Skills.sh: [Ing-la/agent-skills-share](https://skills.sh/Ing-la/agent-skills-share)

## 📄 License

MIT License
