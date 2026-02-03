# Test Suite for Python Practice Kit

This directory contains pytest tests for the Python practice exercises and CLI.

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_exercises.py

# Run with coverage
pytest --cov=cli --cov-report=html

# Run only fast tests
pytest -m "not slow"
```

## Test Structure

- `conftest.py` - Shared fixtures
- `test_exercises.py` - Tests for exercise structure and execution
- `test_cli.py` - Tests for CLI runner and utilities

## Coverage Goal

Target: 80%+ code coverage for CLI modules.

## Adding New Tests

1. Place tests in appropriate file
2. Use descriptive test names (test_what_is_expected)
3. Fixtures are in conftest.py
4. Run tests before committing
