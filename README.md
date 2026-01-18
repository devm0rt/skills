# Agent Skills

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. This repository contains useful skills for developers.

**Specification**: [agentskills.io](https://agentskills.io)

## Installation

### Claude Code

```bash
# Add the marketplace
/plugin marketplace add devm0rt/skills

# Install skill sets
/plugin install document-skills@devm0rt-skills
/plugin install ai-skills@devm0rt-skills
```

After installing, invoke skills by mentioning them: *"Use the PDF skill to extract form fields from invoice.pdf"*

### Claude.ai

Skills are available to paid plans. See [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

### Claude API

See [Skills API Quickstart](https://docs.claude.com/en/api/skills-guide).

## Required Tools

Skills require external tools to function. Install only what you need based on which skills you use.

### Tool to Skill Matrix

| Tool | pdf | docx | pptx | xlsx | webapp-testing | web-artifacts | slack-gif |
|------|-----|------|------|------|----------------|---------------|-----------|
| poppler | ✓ | ✓ | ✓ | | | | |
| pandoc | | ✓ | | | | | |
| libreoffice | | ✓ | ✓ | ✓ | | | |
| qpdf | ✓ | | | | | | |
| tesseract | ✓ | | | | | | |
| node | | | ✓ | | | ✓ | |
| playwright | | | ✓ | | ✓ | | |
| pillow | ✓ | | | | | | ✓ |
| openpyxl | | | | ✓ | | | |
| python-pptx | | | ✓ | | | | |
| python-docx | | ✓ | | | | | |

### System Tools

#### Arch Linux

```bash
# Core document processing
sudo pacman -S poppler qpdf pandoc tesseract libreoffice-fresh

# Node.js (for pptx, web-artifacts-builder)
sudo pacman -S nodejs npm

# Playwright system dependencies
sudo pacman -S webkit2gtk gtk3 nss
```

#### Homebrew (macOS/Linux)

```bash
# Core document processing
brew install poppler qpdf pandoc tesseract libreoffice

# Node.js
brew install node

# Playwright dependencies are installed automatically via npm
```

### Python Libraries

Create a virtual environment with [uv](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12
source .venv/bin/activate.fish  # fish shell
# source .venv/bin/activate     # bash/zsh
```

#### PDF Skill

```bash
pip install pypdf pdfplumber reportlab pypdfium2 pdf2image pytesseract pillow
```

#### DOCX Skill

```bash
pip install python-docx defusedxml
```

#### PPTX Skill

```bash
pip install python-pptx markitdown defusedxml
```

#### XLSX Skill

```bash
pip install openpyxl pandas
```

#### Webapp Testing Skill

```bash
pip install playwright
playwright install  # Downloads browser binaries
```

#### Slack GIF Creator Skill

```bash
pip install pillow imageio numpy
```

### Node.js Packages

#### PPTX Skill

```bash
npm install pptxgenjs playwright sharp react react-dom react-icons
```

#### Web Artifacts Builder Skill

```bash
npm install react@18 react-dom@18 typescript vite tailwindcss parcel html-inline
```

## Skill Reference

### document-skills (source-available)

Production skills powering [Claude's document capabilities](https://www.anthropic.com/news/create-files).

| Skill | Description |
|-------|-------------|
| [pdf](./document-skills/pdf) | Read, analyze, fill forms, create PDFs |
| [docx](./document-skills/docx) | Create and edit Word documents |
| [pptx](./document-skills/pptx) | Create and edit PowerPoint presentations |
| [xlsx](./document-skills/xlsx) | Create and edit Excel spreadsheets |

### ai-skills (Apache 2.0)

| Skill | Description |
|-------|-------------|
| [mcp-builder](./ai-skills/mcp-builder) | Create MCP servers for LLM tool integration |
| [skill-creator](./ai-skills/skill-creator) | Create and package new skills |

### dev-skills (Apache 2.0)

| Skill | Description |
|-------|-------------|
| [doc-coauthoring](./dev-skills/doc-coauthoring) | Collaborative document workflows |
| [internal-comms](./dev-skills/internal-comms) | Internal communications templates |
| [webapp-testing](./dev-skills/webapp-testing) | Automated testing with Playwright |

### misc-skills (Apache 2.0)

| Skill | Description |
|-------|-------------|
| [algorithmic-art](./misc-skills/algorithmic-art) | Generate art with p5.js |
| [brand-guidelines](./misc-skills/brand-guidelines) | Create brand guideline documents |
| [canvas-design](./misc-skills/canvas-design) | Design graphics programmatically |
| [frontend-design](./misc-skills/frontend-design) | HTML/CSS/JS frontend prototypes |
| [slack-gif-creator](./misc-skills/slack-gif-creator) | Create animated GIFs for Slack |
| [theme-factory](./misc-skills/theme-factory) | Generate UI themes |
| [web-artifacts-builder](./misc-skills/web-artifacts-builder) | Build React web components |

## Creating Skills

Use the skill-creator skill to create new skills:

```
/plugin install example-skills@anthropic-agent-skills
```

Then ask Claude: *"Use the skill-creator to make a new skill for [your use case]"*

The skill-creator handles:
- Proper SKILL.md structure with frontmatter
- Progressive disclosure patterns
- Script scaffolding
- Packaging for distribution

## Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Equipping agents for the real world](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
