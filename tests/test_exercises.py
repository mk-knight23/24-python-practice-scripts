"""
Test suite for Python practice exercises.

Tests that exercises:
- Are valid Python files
- Have proper structure (shebang, docstrings)
- Can run without errors
- Follow the exercise format
"""

import ast
import subprocess
from pathlib import Path
from typing import List

import pytest


class TestExerciseStructure:
    """Test that exercises have proper structure."""

    def test_exercise_has_shebang(self, exercise_files: List[Path]):
        """All exercises should start with a shebang."""
        for exercise in exercise_files:
            content = exercise.read_text()
            lines = content.split('\n')
            assert lines[0].startswith('#!'), f"{exercise} missing shebang"
            assert 'python3' in lines[0], f"{exercise} should use python3"

    def test_exercise_has_docstring(self, exercise_files: List[Path]):
        """All exercises should have a module docstring."""
        for exercise in exercise_files:
            content = exercise.read_text()
            tree = ast.parse(content)

            docstring = ast.get_docstring(tree)
            assert docstring is not None, f"{exercise} missing module docstring"
            assert len(docstring) > 50, f"{exercise} docstring too short"

    def test_exercise_has_purpose(self, exercise_files: List[Path]):
        """All exercises should document their purpose."""
        for exercise in exercise_files:
            content = exercise.read_text()
            assert 'Purpose:' in content, f"{exercise} missing Purpose statement"

    def test_exercise_has_why(self, exercise_files: List[Path]):
        """All exercises should explain why they matter."""
        for exercise in exercise_files:
            content = exercise.read_text()
            assert 'Why:' in content, f"{exercise} missing Why statement"

    def test_exercise_has_example(self, exercise_files: List[Path]):
        """All exercises should show example usage."""
        for exercise in exercise_files:
            content = exercise.read_text()
            assert 'Example:' in content, f"{exercise} missing Example section"


class TestExerciseExecution:
    """Test that exercises can run successfully."""

    def test_exercise_syntax_valid(self, exercise_files: List[Path]):
        """All exercises should have valid Python syntax."""
        for exercise in exercise_files:
            try:
                with open(exercise) as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                pytest.fail(f"{exercise} has syntax error: {e}")

    def test_exercise_runs_without_error(self, exercise_files: List[Path]):
        """All exercises should run without errors."""
        for exercise in exercise_files:
            result = subprocess.run(
                ['python3', str(exercise)],
                capture_output=True,
                timeout=10
            )
            assert result.returncode == 0, f"{exercise} failed with: {result.stderr.decode()}"

    def test_exercise_produces_output(self, exercise_files: List[Path]):
        """All exercises should produce some output."""
        for exercise in exercise_files:
            result = subprocess.run(
                ['python3', str(exercise)],
                capture_output=True,
                timeout=10
            )
            output = result.stdout.decode()
            assert len(output) > 0, f"{exercise} produced no output"


class TestExerciseCategories:
    """Test exercise organization."""

    def test_basics_exist(self, skills_dir: Path):
        """Basics directory should exist and have exercises."""
        basics_dir = skills_dir / "basics"
        assert basics_dir.exists(), "Basics directory missing"
        exercises = list(basics_dir.glob("*.py"))
        assert len(exercises) >= 5, f"Only {len(exercises)} basic exercises"

    def test_core_exist(self, skills_dir: Path):
        """Core directory should exist and have exercises."""
        core_dir = skills_dir / "core"
        assert core_dir.exists(), "Core directory missing"
        exercises = list(core_dir.glob("*.py"))
        assert len(exercises) >= 4, f"Only {len(exercises)} core exercises"

    def test_advanced_exist(self, skills_dir: Path):
        """Advanced directory should exist and have exercises."""
        advanced_dir = skills_dir / "advanced"
        assert advanced_dir.exists(), "Advanced directory missing"
        exercises = list(advanced_dir.glob("*.py"))
        assert len(exercises) >= 3, f"Only {len(exercises)} advanced exercises"

    def test_exercises_numbered(self, exercise_files: List[Path]):
        """Exercise filenames should be numbered for ordering."""
        for exercise in exercise_files:
            # Filename should start with a number
            assert exercise.stem[0].isdigit(), f"{exercise} should start with a number"


class TestExerciseContent:
    """Test exercise content quality."""

    def test_exercise_not_empty(self, exercise_files: List[Path]):
        """Exercises should contain actual code."""
        for exercise in exercise_files:
            content = exercise.read_text()
            # Remove comments and empty lines
            code_lines = [
                line for line in content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            ]
            assert len(code_lines) > 5, f"{exercise} has too little code"

    def test_exercise_has_print_statements(self, exercise_files: List[Path]):
        """Exercises should demonstrate with print() calls."""
        for exercise in exercise_files:
            content = exercise.read_text()
            assert 'print(' in content, f"{exercise} should have print() statements"

    def test_exercise_readable(self, exercise_files: List[Path]):
        """Exercises should be readable (not obfuscated)."""
        for exercise in exercise_files:
            content = exercise.read_text()
            lines = content.split('\n')
            # Check for reasonable line length
            long_lines = [line for line in lines if len(line) > 100]
            assert len(long_lines) < 3, f"{exercise} has too many long lines (>100 chars)"
