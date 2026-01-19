# Claude Skill Quality Analyzer

Comprehensive quality analysis tool for Claude Skills. Evaluates skills from any source across five critical dimensions using balanced scoring and multiple output modes.

## Features

- **Multi-Source Support**: GitHub URLs, marketplace links, ZIP files, local directories
- **Five-Dimensional Evaluation**: Structure, security, UX, code quality, integration
- **Three Output Modes**: Comprehensive report, interactive review, pass/fail certification
- **Security Integration**: Leverages skill-security-analyzer for vulnerability detection

## Quick Start

### Analyze a Skill

```
User: Analyze skill quality for https://github.com/user/my-skill
User: Review this skill: ~/.claude/skills/my-skill
User: Run quality certification on my-skill
```

### Trigger Phrases

- "analyze skill quality"
- "review this skill"
- "evaluate skill"
- "skill quality check"

## Installation

```bash
/plugin install analyzing-skill-quality@anthropic-agent-skills
```

## Documentation

See [SKILL.md](SKILL.md) for complete workflow and evaluation criteria.

### References

- `references/report-templates.md` - Output templates for all modes
- `references/quality-checklist.md` - Detailed evaluation criteria
- `references/best-practices-patterns.md` - Proven patterns
- `references/anti-patterns.md` - Common mistakes to flag

## License

Apache 2.0
