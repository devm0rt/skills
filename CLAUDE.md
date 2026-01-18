# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is Anthropic's official Agent Skills repository - an implementation of the Agent Skills standard providing modular packages that extend Claude's capabilities. Skills are self-contained folders containing instructions, scripts, and resources that Claude loads dynamically for specialized tasks.

**Specification**: https://agentskills.io/specification

## Skill Structure

Every skill follows this structure:
```
skill-name/
├── SKILL.md              # Required: YAML frontmatter (name, description) + markdown instructions
├── scripts/              # Optional: Executable code for deterministic tasks
├── references/           # Optional: Documentation loaded into context as needed
└── assets/               # Optional: Files used in output (templates, icons, fonts)
```

## Working With This Repository

### No Build System
Skills are standalone - no package.json, Makefile, or setup.py. Skills are distributed via Claude Code Plugin Marketplace.

### Creating a New Skill
1. Run `ai-skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>`
2. Edit SKILL.md frontmatter: `name` and `description` are required
3. Add scripts/, references/, or assets/ as needed
4. Package with `ai-skills/skill-creator/scripts/package_skill.py <path/to/skill-folder>`

### Modifying Skills
- Read the full SKILL.md first to understand the interface
- Check `scripts/` for black-box implementations (run with `--help` first)
- Check `references/` for detailed technical documentation
- Document skills (docx, pdf, pptx, xlsx) are production-grade; others are examples

## Key Design Principles

### Context Efficiency
The context window is shared. Only add information Claude doesn't already have. Challenge every line: "Does this justify its token cost?"

### Progressive Disclosure
1. Metadata (name + description): ~100 words, always loaded
2. SKILL.md body: <5k words, loaded when skill triggers
3. Bundled resources: loaded as needed

Keep SKILL.md under 500 lines. Split detailed content into references/ files and link to them from SKILL.md.

### Degrees of Freedom
- **High freedom** (text instructions): When multiple approaches are valid
- **Medium freedom** (pseudocode/parameterized scripts): When a preferred pattern exists
- **Low freedom** (specific scripts): When operations are fragile or consistency is critical

## Directory Overview

- `document-skills/` - Document processing skills (production, source-available)
  - `docx/`, `pdf/`, `pptx/`, `xlsx/`
- `ai-skills/` - AI agent building skills (Apache 2.0)
  - `mcp-builder/`, `skill-creator/`
- `dev-skills/` - Developer workflow skills (Apache 2.0)
  - `doc-coauthoring/`, `internal-comms/`
- `misc-skills/` - Creative and experimental skills (Apache 2.0)
  - `algorithmic-art/`, `brand-guidelines/`, `canvas-design/`, `frontend-design/`
  - `slack-gif-creator/`, `theme-factory/`, `web-artifacts-builder/`, `webapp-testing/`
- `spec/` - Link to Agent Skills specification
- `template/` - Minimal SKILL.md template

## Installing Skills in Claude Code
```
/plugin marketplace add devm0rt/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```
