#!/usr/bin/env python3
"""
Progress tracking system for Python practice exercises.

Legacy interface that now uses SQLite database for storage.
Maintains backward compatibility with old .progress.json system.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Import database module
try:
    from database import (
        init_database, get_active_user, create_user,
        mark_exercise_complete as db_mark_complete,
        get_exercise_progress as db_get_exercise_progress,
        get_user_progress, get_all_users,
        migrate_from_json, export_user_data, import_user_data
    )
    HAS_DATABASE = True
except ImportError:
    HAS_DATABASE = False


PROGRESS_FILE = ".progress.json"


def load_progress() -> Dict[str, Dict[str, any]]:
    """
    Load progress from JSON file (legacy).

    Returns:
        Dictionary mapping exercise paths to progress data
    """
    if not os.path.exists(PROGRESS_FILE):
        return {}

    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_progress(progress: Dict[str, Dict[str, any]]) -> None:
    """
    Save progress to JSON file (legacy).

    Args:
        progress: Dictionary mapping exercise paths to progress data
    """
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save progress: {e}")


def _get_or_create_user() -> Optional[Dict[str, any]]:
    """Get active user or create default user."""
    if not HAS_DATABASE:
        return None

    # Initialize database if needed
    init_database()

    # Try to migrate old data
    migrate_from_json()

    # Get or create user
    user = get_active_user()
    if not user:
        user = create_user("default", "Default User")

    return user


def mark_exercise_complete(filepath: str, success: bool = True, time_spent: int = 0) -> None:
    """
    Mark an exercise as complete (or failed).

    Args:
        filepath: Full path to exercise file
        success: Whether the exercise completed successfully
        time_spent: Time spent in seconds (optional)
    """
    # Try database first
    if HAS_DATABASE:
        user = _get_or_create_user()
        if user:
            db_mark_complete(user['id'], filepath, success, time_spent)
            return

    # Fallback to JSON
    progress = load_progress()

    # Use relative path for portability
    rel_path = os.path.relpath(filepath)

    if rel_path not in progress:
        progress[rel_path] = {
            'attempts': 0,
            'completed': False,
            'last_attempt': None,
            'first_attempt': None
        }

    progress[rel_path]['attempts'] += 1
    progress[rel_path]['last_attempt'] = datetime.now().isoformat()

    if progress[rel_path]['first_attempt'] is None:
        progress[rel_path]['first_attempt'] = progress[rel_path]['last_attempt']

    if success:
        progress[rel_path]['completed'] = True

    save_progress(progress)


def get_exercise_progress(filepath: str) -> Optional[Dict[str, any]]:
    """
    Get progress for a specific exercise.

    Args:
        filepath: Full path to exercise file

    Returns:
        Progress dict or None if not found
    """
    # Try database first
    if HAS_DATABASE:
        user = _get_or_create_user()
        if user:
            prog = db_get_exercise_progress(user['id'], filepath)
            if prog:
                return {
                    'attempts': prog['attempts'],
                    'completed': bool(prog['completed']),
                    'last_attempt': prog['last_attempt'],
                    'first_attempt': prog['first_attempt'],
                    'time_spent_seconds': prog['time_spent_seconds']
                }

    # Fallback to JSON
    progress = load_progress()
    rel_path = os.path.relpath(filepath)
    return progress.get(rel_path)


def get_summary() -> Dict[str, any]:
    """
    Get overall progress summary.

    Returns:
        Dictionary with total, completed, remaining counts
    """
    # Try database first
    if HAS_DATABASE:
        user = _get_or_create_user()
        if user:
            prog = get_user_progress(user['id'])
            return {
                'total': prog['total'],
                'completed': prog['completed'],
                'remaining': prog['remaining'],
                'percentage': prog['percentage']
            }

    # Fallback to JSON
    progress = load_progress()

    total = len(progress)
    completed = sum(1 for p in progress.values() if p.get('completed', False))
    remaining = total - completed

    return {
        'total': total,
        'completed': completed,
        'remaining': remaining,
        'percentage': round((completed / total * 100) if total > 0 else 0, 1)
    }


def format_summary() -> str:
    """
    Format progress summary for display.

    Returns:
        Formatted string with progress information
    """
    summary = get_summary()

    lines = [
        "Progress Summary",
        "=" * 40,
        f"Total exercises: {summary['total']}",
        f"Completed: {summary['completed']}",
        f"Remaining: {summary['remaining']}",
        f"Progress: {summary['percentage']}%",
        "=" * 40
    ]

    return "\n".join(lines)


def get_completed_exercises() -> List[str]:
    """
    Get list of completed exercise paths.

    Returns:
        List of relative paths to completed exercises
    """
    progress = load_progress()
    return [
        path for path, data in progress.items()
        if data.get('completed', False)
    ]


def get_pending_exercises() -> List[str]:
    """
    Get list of pending (not completed) exercise paths.

    Returns:
        List of relative paths to pending exercises
    """
    progress = load_progress()
    return [
        path for path, data in progress.items()
        if not data.get('completed', False)
    ]


def reset_progress() -> None:
    """Reset all progress (delete progress file)."""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("Progress reset.")
    else:
        print("No progress file found.")


if __name__ == '__main__':
    # Test the progress system
    print(format_summary())
