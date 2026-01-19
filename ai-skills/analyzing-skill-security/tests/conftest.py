"""
Pytest fixtures for security scanner tests.
"""

from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def malicious_samples_dir(fixtures_dir: Path) -> Path:
    """Return the path to the malicious samples directory."""
    return fixtures_dir / "malicious_samples"


@pytest.fixture
def scanner_script() -> Path:
    """Return the path to the security scanner script."""
    return Path(__file__).parent.parent / "scripts" / "security_scanner.py"
