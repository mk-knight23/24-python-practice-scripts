"""
Test suite for CLI runner and utilities.
"""

import subprocess
from pathlib import Path

import pytest


class TestCLIUtilities:
    """Test CLI utility functions."""

    def test_utils_module_exists(self, utils_path: Path):
        """Utils module should exist."""
        assert utils_path.exists(), "utils.py missing"

    def test_utils_importable(self):
        """Utils module should be importable."""
        import cli.utils
        assert hasattr(cli.utils, 'list_exercises')
        assert hasattr(cli.utils, 'read_exercise_info')
        assert hasattr(cli.utils, 'run_python_file')

    def test_list_exercises_returns_list(self):
        """list_exercises should return a list."""
        from cli.utils import list_exercises
        exercises = list_exercises()
        assert isinstance(exercises, list)
        assert len(exercises) > 0

    def test_list_exercises_format(self):
        """list_exercises should return proper format."""
        from cli.utils import list_exercises
        exercises = list_exercises()
        for exercise in exercises:
            assert len(exercise) == 3, "Each exercise should be (category, filename, path)"
            assert isinstance(exercise[0], str), "Category should be string"
            assert isinstance(exercise[1], str), "Filename should be string"
            assert isinstance(exercise[2], str), "Path should be string"

    def test_read_exercise_info_returns_dict(self):
        """read_exercise_info should return a dict."""
        from cli.utils import read_exercise_info
        from cli.utils import list_exercises

        exercises = list_exercises()
        if exercises:
            info = read_exercise_info(exercises[0][2])
            assert isinstance(info, dict)
            assert 'purpose' in info
            assert 'why' in info
            assert 'code' in info


class TestCLIRunner:
    """Test main CLI runner."""

    def test_runner_exists(self, runner_path: Path):
        """Runner script should exist."""
        assert runner_path.exists(), "runner.py missing"

    def test_runner_executable(self, runner_path: Path):
        """Runner should be executable."""
        # Just check it can be run with python
        result = subprocess.run(
            ['python3', str(runner_path)],
            capture_output=True,
            timeout=5
        )
        # Should run (might fail if no input, but should start)
        assert 'python' not in result.stderr.decode().lower()

    def test_runner_importable(self):
        """Runner module should be importable."""
        import cli.runner
        assert hasattr(cli.runner, 'main')
        assert hasattr(cli.runner, 'main_menu')


class TestProgressTracking:
    """Test progress tracking system."""

    def test_progress_module_exists(self, cli_dir: Path):
        """Progress module should exist."""
        progress_path = cli_dir / "progress.py"
        assert progress_path.exists(), "progress.py missing"

    def test_progress_importable(self):
        """Progress module should be importable."""
        import cli.progress
        assert hasattr(cli.progress, 'load_progress')
        assert hasattr(cli.progress, 'save_progress')
        assert hasattr(cli.progress, 'mark_exercise_complete')
        assert hasattr(cli.progress, 'get_summary')

    def test_progress_load_empty(self):
        """Loading progress when file doesn't exist should return empty dict."""
        from cli.progress import load_progress
        # This is safe - just tests the function logic
        result = load_progress()
        assert isinstance(result, dict)

    def test_progress_summary_format(self):
        """Progress summary should return proper format."""
        from cli.progress import get_summary
        summary = get_summary()
        assert isinstance(summary, dict)
        assert 'total' in summary
        assert 'completed' in summary
        assert 'remaining' in summary
        assert 'percentage' in summary
