"""
Pytest tests for the Security Scanner.

Tests scanner against malicious samples and verifies detection capabilities.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Test cases: (sample_file, expected_patterns, xfail_reason)
# Each tuple contains the filename, patterns to detect, and optional xfail reason
# xfail_reason is None if the test is expected to pass
DETECTION_TEST_CASES = [
    pytest.param(
        "01_indirect_execution.py",
        ["Obfuscated Execution", "getattr"],
        None,
        id="01_indirect_execution",
    ),
    pytest.param(
        "02_hidden_payload.txt",
        ["Command Injection"],
        None,
        id="02_hidden_payload",
    ),
    pytest.param(
        "03_encoding.py",
        ["Code Obfuscation", "ROT"],
        None,
        id="03_encoding",
    ),
    pytest.param(
        "04_shell.py",
        ["Shell Injection"],
        None,
        id="04_shell",
    ),
    pytest.param(
        "05_timebomb.py",
        ["Time Bomb"],
        None,
        id="05_timebomb",
    ),
    pytest.param(
        "06_typosquat.py",
        ["Supply Chain", "typosquat"],
        None,
        id="06_typosquat",
    ),
    pytest.param(
        "07_env.py",
        ["Environment Manipulation"],
        None,
        id="07_env",
    ),
    pytest.param(
        "08_sandbox.py",
        ["Obfuscated Execution"],
        None,
        id="08_sandbox",
    ),
    pytest.param(
        "09_exfil.py",
        ["Network Access"],
        None,
        id="09_exfil",
    ),
    pytest.param(
        "10_yaml.md",
        ["YAML Injection"],
        None,
        id="10_yaml",
    ),
    pytest.param(
        "11_import_hook.py",
        ["Obfuscated Execution", "import hook"],
        None,
        id="11_import_hook",
    ),
]

# Minimal SKILL.md content for test fixtures
MINIMAL_SKILL_MD = """---
name: test-skill
description: Test skill for security scanner
---

# Test Skill

This is a minimal skill for testing the security scanner.
"""


@pytest.fixture
def scanner_path() -> Path:
    """Return the path to the security scanner script."""
    return Path(__file__).parent.parent / "scripts" / "security_scanner.py"


@pytest.fixture
def create_test_skill(tmp_path: Path, malicious_samples_dir: Path):
    """Factory fixture to create a test skill directory with a malicious sample."""

    def _create(sample_file: str) -> Path:
        """Create a skill directory structure containing the malicious sample."""
        skill_dir = tmp_path / f"test-skill-{sample_file}"
        scripts_dir = skill_dir / "scripts"
        references_dir = skill_dir / "references"
        scripts_dir.mkdir(parents=True)
        references_dir.mkdir(parents=True)

        # Create SKILL.md
        (skill_dir / "SKILL.md").write_text(MINIMAL_SKILL_MD)

        # Copy the malicious sample to appropriate location
        sample_path = malicious_samples_dir / sample_file
        if sample_path.exists():
            # Put .md files in references, others in scripts
            if sample_file.endswith(".md"):
                shutil.copy(sample_path, references_dir / sample_file)
            else:
                shutil.copy(sample_path, scripts_dir / sample_file)

        return skill_dir

    return _create


class TestSecurityScanner:
    """Test suite for the security scanner detection capabilities."""

    @pytest.mark.parametrize(
        "sample_file,expected_patterns,xfail_reason", DETECTION_TEST_CASES
    )
    def test_malicious_sample_detection(
        self,
        sample_file: str,
        expected_patterns: list[str],
        xfail_reason: str | None,
        malicious_samples_dir: Path,
        scanner_path: Path,
        create_test_skill,
    ):
        """Test that scanner detects expected patterns in malicious samples."""
        if xfail_reason:
            pytest.xfail(xfail_reason)

        sample_path = malicious_samples_dir / sample_file

        if not sample_path.exists():
            pytest.skip(f"Sample file not found: {sample_file}")

        # Create a proper skill directory structure with the sample
        skill_dir = create_test_skill(sample_file)

        result = subprocess.run(
            [sys.executable, str(scanner_path), str(skill_dir)],
            capture_output=True,
            text=True,
            timeout=10,
        )

        report = json.loads(result.stdout)
        findings_text = json.dumps(report["findings"]).lower()

        for pattern in expected_patterns:
            assert pattern.lower() in findings_text, (
                f"Expected pattern '{pattern}' not found in findings for {sample_file}. "
                f"Findings: {report['findings']}"
            )

    def test_scanner_exists(self, scanner_path: Path):
        """Verify the scanner script exists."""
        assert scanner_path.exists(), f"Scanner not found at {scanner_path}"

    def test_scanner_help(self, scanner_path: Path):
        """Verify the scanner has help output."""
        result = subprocess.run(
            [sys.executable, str(scanner_path), "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "help" in result.stdout.lower()

    def test_scanner_returns_valid_json(
        self, malicious_samples_dir: Path, scanner_path: Path, create_test_skill
    ):
        """Verify the scanner returns valid JSON output."""
        sample_path = malicious_samples_dir / "01_indirect_execution.py"
        if not sample_path.exists():
            pytest.skip("Sample file not found")

        skill_dir = create_test_skill("01_indirect_execution.py")

        result = subprocess.run(
            [sys.executable, str(scanner_path), str(skill_dir)],
            capture_output=True,
            text=True,
            timeout=10,
        )

        report = json.loads(result.stdout)
        assert "skill" in report
        assert "summary" in report
        assert "findings" in report
        assert "total_findings" in report["summary"]

    def test_scanner_nonexistent_path(self, scanner_path: Path, tmp_path: Path):
        """Verify the scanner handles non-existent paths gracefully."""
        fake_path = tmp_path / "nonexistent_skill"

        result = subprocess.run(
            [sys.executable, str(scanner_path), str(fake_path)],
            capture_output=True,
            text=True,
            timeout=5,
        )

        # Scanner should exit with error or report the issue
        assert result.returncode != 0 or "error" in result.stderr.lower()
