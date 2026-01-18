#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import fnmatch
import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill


# Whitelist of allowed top-level items (per Agent Skills spec)
ALLOWED_TOP_LEVEL = {
    'SKILL.md',      # Required
    'LICENSE.txt',   # License file
    'scripts',       # Executable code
    'references',    # Documentation
    'assets',        # Static resources
}

# Patterns excluded from any directory
EXCLUDE_PATTERNS = [
    # Test files
    'tests',
    '*_test.py',
    'test_*.py',
    'conftest.py',
    '.pytest_cache',
    '.coverage',
    'htmlcov',
    # Python artifacts
    '__pycache__',
    '*.pyc',
    '*.pyo',
    # Editor/IDE/OS
    '.vscode',
    '.idea',
    '*.swp',
    '.DS_Store',
    # Version control
    '.git',
    '.gitignore',
    # Environment
    '.env',
    '.env.*',
    'venv',
    '.venv',
]


def should_include(file_path, skill_path):
    """Check if file should be included based on whitelist and exclusions."""
    rel = file_path.relative_to(skill_path)
    parts = rel.parts

    # Check top-level item against whitelist
    top_level = parts[0]
    if top_level not in ALLOWED_TOP_LEVEL:
        return False

    # Check all path components against exclusion patterns
    for part in parts:
        for pattern in EXCLUDE_PATTERNS:
            if fnmatch.fnmatch(part, pattern):
                return False
    return True


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .skill file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .skill file (defaults to current directory)

    Returns:
        Path to the created .skill file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # Create the .skill file (zip format)
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Always include SKILL.md first (it's at root level)
            skill_md = skill_path / 'SKILL.md'
            arcname = skill_md.relative_to(skill_path.parent)
            zipf.write(skill_md, arcname)
            print(f"  Added: {arcname}")

            # Include LICENSE.txt if it exists
            license_file = skill_path / 'LICENSE.txt'
            if license_file.exists():
                arcname = license_file.relative_to(skill_path.parent)
                zipf.write(license_file, arcname)
                print(f"  Added: {arcname}")

            # Walk through the skill directory for other files
            included = 0
            skipped = 0
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Skip files already added
                    if file_path.name in ('SKILL.md', 'LICENSE.txt') and file_path.parent == skill_path:
                        continue
                    if should_include(file_path, skill_path):
                        arcname = file_path.relative_to(skill_path.parent)
                        zipf.write(file_path, arcname)
                        print(f"  Added: {arcname}")
                        included += 1
                    else:
                        skipped += 1
            if skipped:
                print(f"\n  Skipped {skipped} file(s) not in allowed directories or matching exclusions")

        print(f"\n✅ Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ Error creating .skill file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        print("\nExample:")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
