"""
Pytest configuration and shared fixtures for testing Python practice exercises.
"""

import os
import sys
from pathlib import Path
from typing import List

import pytest


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def skills_dir() -> Path:
    """Path to the skills directory."""
    return Path(__file__).parent.parent / "skills"


@pytest.fixture
def cli_dir() -> Path:
    """Path to the cli directory."""
    return Path(__file__).parent.parent / "cli"


@pytest.fixture
def exercise_files(skills_dir: Path) -> List[Path]:
    """List all exercise Python files."""
    exercises = []
    for category in ['basics', 'core', 'advanced']:
        cat_dir = skills_dir / category
        if cat_dir.exists():
            exercises.extend(sorted(cat_dir.glob("*.py")))
    return exercises


@pytest.fixture
def runner_path(cli_dir: Path) -> Path:
    """Path to the main CLI runner."""
    return cli_dir / "runner.py"


@pytest.fixture
def utils_path(cli_dir: Path) -> Path:
    """Path to the CLI utilities module."""
    return cli_dir / "utils.py"
