---
name: analyzing-skill-quality
description: "Analyze Claude Skill quality across five dimensions (structure, security, UX, code quality, integration). Use when evaluating skills from GitHub, marketplace, ZIP, or local directories. Triggers: 'analyze skill quality', 'review this skill', 'evaluate skill', 'skill quality check'."
license: Complete terms in LICENSE.txt
---

# Claude Skill Quality Analyzer

## Overview

Evaluate Claude Skills from any source (GitHub, marketplaces, ZIP files, local directories) across five critical dimensions using balanced scoring. Security analysis leverages the skill-security-analyzer skill for automated vulnerability detection.

## Output Modes

Users select one of three analysis modes:

1. **Comprehensive Report** - Detailed markdown report with numerical scores (0-100) across all dimensions
2. **Interactive Review** - Step-by-step analysis with specific, actionable recommendations
3. **Pass/Fail Certification** - Binary quality assessment with specific issues blocking certification

## Evaluation Dimensions

### 1. Structure & Documentation (20%)

**Evaluate:** SKILL.md existence and format, YAML frontmatter validity, description with trigger phrases, section organization, examples/templates, references directory, README.

**Scoring:**
- 90-100: Exemplary documentation, comprehensive examples
- 70-89: Good documentation with minor gaps
- 50-69: Basic documentation lacking detail
- 0-49: Missing critical documentation

### 2. Security (30%)

**Evaluate:** Use skill-security-analyzer for automated scanning. Check for command injection, data exfiltration, YAML injection, file operation safety, hardcoded secrets, input validation, supply chain risks, obfuscation.

**Scoring based on risk rating:**
- SAFE/LOW: 90-100
- MEDIUM: 70-89
- HIGH: 50-69
- CRITICAL: 0-49

### 3. User Experience (20%)

**Evaluate:** Trigger phrase clarity, workflow documentation, practical examples, references/ usage, logical organization, scope definition.

**Scoring:**
- 90-100: Exceptional UX, immediately clear
- 70-89: Good UX with minor confusion points
- 50-69: Usable but requires effort
- 0-49: Confusing or poorly organized

### 4. Code Quality (15%)

**Evaluate:** Best practices adherence, resource organization (references/, scripts/, assets/), structure clarity, script documentation, complexity, formatting consistency.

**Scoring:**
- 90-100: Exemplary quality and organization
- 70-89: Good quality with minor issues
- 50-69: Acceptable but improvable
- 0-49: Poor quality, hard to maintain

### 5. Integration & Tools (15%)

**Evaluate:** Tool/skill invocation patterns, MCP integration, resource efficiency, script integration, tool usage balance.

**Scoring:**
- 90-100: Perfect tool integration
- 70-89: Good integration with minor improvements
- 50-69: Basic integration, missing optimizations
- 0-49: Poor integration or tool misuse

## Analysis Workflow

### Step 1: Get Source and Mode

Ask user for:
1. **Source:** GitHub URL, marketplace link, ZIP file, or local directory
2. **Mode:** Comprehensive report, interactive review, or pass/fail certification

**Fetch the skill:**
```bash
# GitHub
git clone <github-url> /tmp/skill-analysis/<skill-name>

# Marketplace (check installed locations)
ls -la ~/.claude/skills/
ls -la ~/.claude/plugins/marketplaces/*/

# ZIP
unzip <path-to-zip> -d /tmp/skill-analysis/<skill-name>

# Local - use path directly
```

### Step 2: Understand Purpose

Read SKILL.md to understand:
- What the skill does
- Intended use cases
- Documented workflow

### Step 3: Run Security Analysis

**Always invoke skill-security-analyzer first** to get:
- Automated vulnerability detection
- Malicious code pattern identification
- Risk rating (CRITICAL/HIGH/MEDIUM/LOW/SAFE)

Map results to security score.

### Step 4: Evaluate Structure

Check SKILL.md for:
- Valid YAML frontmatter (+20 pts)
- Clear description with triggers (+20 pts)
- Well-organized sections (+20 pts)
- Examples/templates present (+20 pts)
- Resources documented (+20 pts)

### Step 5: Evaluate User Experience

Review from user perspective:
- Quick understanding of purpose?
- Clear, natural trigger phrases?
- Easy-to-follow workflow?
- Practical examples?
- Well-defined scope?

Check for anti-patterns: vague description, no triggers, missing examples, unclear workflow.

### Step 6: Evaluate Code Quality

Check structure:
```
skill-name/
├── SKILL.md (required)
├── README.md (optional)
├── scripts/ (optional)
├── references/ (optional)
└── assets/ (optional)
```

Evaluate: proper organization, script documentation, maintainability, consistent style.

### Step 7: Evaluate Integration

Check tool usage patterns, MCP integration docs, script efficiency, resource optimization.

### Step 8: Generate Output

Use template from `references/report-templates.md` matching the selected mode.

## Grading Scale

**Score → Grade:**
- 90-100: A+/A (Excellent)
- 80-89: B+/B (Good)
- 70-79: C+/C (Acceptable)
- 60-69: D (Needs Improvement)
- 0-59: F (Poor)

**Certification Requirements:**
- Overall ≥ 70
- Security ≥ 80
- Structure ≥ 70
- UX ≥ 70
- Code Quality ≥ 60
- Integration ≥ 60
- No CRITICAL security findings

## Resources

### references/report-templates.md
Output templates for all three analysis modes. Load when generating reports.

### references/quality-checklist.md
Comprehensive evaluation checklist with detailed scoring criteria.

### references/best-practices-patterns.md
Proven patterns from high-quality skills. Load for specific recommendations.

### references/anti-patterns.md
Common mistakes and issues to flag. Quick pattern matching reference.

---

**Important:** Always run skill-security-analyzer before evaluating other dimensions.
