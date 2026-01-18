# Testing Skill Scripts

Comprehensive guide for testing skill scripts with pytest.

## Directory Structure

```
skill-name/
├── scripts/
│   ├── process.py
│   └── validate.py
└── tests/
    ├── conftest.py           # Shared fixtures
    ├── test_process.py       # Tests for process.py
    ├── test_validate.py      # Tests for validate.py
    └── fixtures/             # Test data
        ├── sample_input.json
        └── expected_output.json
```

## Importing Scripts

Since scripts/ isn't a Python package, add it to `sys.path`:

```python
# tests/test_process.py
import sys
from pathlib import Path

# Add scripts/ to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from process import transform, validate
```

**Alternative: Use conftest.py for shared path setup:**

```python
# tests/conftest.py
import sys
from pathlib import Path

# Add scripts/ to path once for all tests
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
```

Then imports work directly in test files:

```python
# tests/test_process.py
from process import transform
```

## Writing Tests

### Basic Test Structure

```python
# tests/test_process.py
from process import transform

def test_transform_returns_dict():
    """Test that transform returns a dictionary."""
    result = transform({'input': 'data'})
    assert isinstance(result, dict)

def test_transform_success_status():
    """Test successful transformation sets status."""
    result = transform({'input': 'data'})
    assert result['status'] == 'success'

def test_transform_handles_empty_input():
    """Test graceful handling of empty input."""
    result = transform({})
    assert result['status'] == 'error'
    assert 'message' in result
```

### Using Fixtures

```python
# tests/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture
def skill_dir():
    """Return path to skill root directory."""
    return Path(__file__).parent.parent

@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / 'fixtures'

@pytest.fixture
def sample_input(fixtures_dir):
    """Load sample input data."""
    with open(fixtures_dir / 'sample_input.json') as f:
        return json.load(f)

@pytest.fixture
def expected_output(fixtures_dir):
    """Load expected output data."""
    with open(fixtures_dir / 'expected_output.json') as f:
        return json.load(f)
```

Using fixtures in tests:

```python
# tests/test_process.py
from process import transform

def test_transform_with_fixture(sample_input, expected_output):
    """Test transform with fixture data."""
    result = transform(sample_input)
    assert result == expected_output
```

### Testing File Operations

```python
# tests/test_file_operations.py
import tempfile
from pathlib import Path
from process import process_file

def test_process_file_creates_output(tmp_path):
    """Test that process_file creates output file."""
    input_file = tmp_path / 'input.txt'
    input_file.write_text('test content')

    output_file = tmp_path / 'output.txt'
    process_file(input_file, output_file)

    assert output_file.exists()
    assert output_file.read_text() == 'processed: test content'
```

### Testing CLI Scripts

```python
# tests/test_cli.py
import subprocess
import sys
from pathlib import Path

def test_script_help():
    """Test script --help output."""
    script = Path(__file__).parent.parent / 'scripts' / 'process.py'
    result = subprocess.run(
        [sys.executable, str(script), '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage' in result.stdout.lower()

def test_script_with_input(tmp_path):
    """Test script with actual input file."""
    script = Path(__file__).parent.parent / 'scripts' / 'process.py'
    input_file = tmp_path / 'input.json'
    input_file.write_text('{"key": "value"}')

    result = subprocess.run(
        [sys.executable, str(script), str(input_file)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
```

### Testing with Mocks

```python
# tests/test_with_mocks.py
from unittest.mock import patch, MagicMock
from process import fetch_and_transform

def test_fetch_handles_network_error():
    """Test graceful handling of network errors."""
    with patch('process.requests.get') as mock_get:
        mock_get.side_effect = ConnectionError('Network unreachable')

        result = fetch_and_transform('https://example.com/data')

        assert result['status'] == 'error'
        assert 'network' in result['message'].lower()
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_process.py

# Run specific test function
pytest tests/test_process.py::test_transform_basic

# Verbose output
pytest tests/ -v

# Stop on first failure
pytest tests/ -x
```

### With Coverage

```bash
# Run with coverage
pytest tests/ --cov=scripts --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=scripts --cov-report=html

# Coverage with minimum threshold
pytest tests/ --cov=scripts --cov-fail-under=80
```

## Package Exclusions

The following are automatically excluded from `.skill` packages:

| Pattern | Description |
|---------|-------------|
| `tests/` | Test directory |
| `test_*.py` | Test files (pytest convention) |
| `*_test.py` | Test files (alternative convention) |
| `conftest.py` | Pytest configuration |
| `.pytest_cache/` | Pytest cache |
| `.coverage` | Coverage data |
| `htmlcov/` | HTML coverage reports |
| `__pycache__/` | Python bytecode cache |

## Example: Complete Test Setup

### conftest.py

```python
# tests/conftest.py
"""Shared pytest fixtures for skill tests."""
import sys
import json
import pytest
from pathlib import Path

# Add scripts/ to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

@pytest.fixture
def skill_dir():
    """Return path to skill root directory."""
    return Path(__file__).parent.parent

@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / 'fixtures'

@pytest.fixture
def load_fixture(fixtures_dir):
    """Factory fixture to load JSON test data."""
    def _load(filename):
        with open(fixtures_dir / filename) as f:
            return json.load(f)
    return _load
```

### Test File

```python
# tests/test_example.py
"""Example tests for skill scripts."""
from example import process_data

def test_process_data_basic():
    """Test basic data processing."""
    result = process_data({'value': 42})
    assert result['processed'] is True
    assert result['value'] == 42

def test_process_data_with_fixture(load_fixture):
    """Test with fixture data."""
    input_data = load_fixture('sample_input.json')
    result = process_data(input_data)
    assert result['processed'] is True
```
