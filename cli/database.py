#!/usr/bin/env python3
"""
SQLite database layer for Python practice system.

Stores:
- User profiles and settings
- Exercise progress and time tracking
- Quiz results
- Achievements
- Notes and bookmarks
"""

from __future__ import annotations

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


# Database file location
DB_DIR = Path.home() / ".python-practice"
DB_FILE = DB_DIR / "practice.db"
BACKUP_DIR = DB_DIR / "backups"


def init_database() -> None:
    """Initialize database schema and create directories."""
    # Create directory if it doesn't exist
    DB_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            display_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_active TEXT DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 0,
            settings_json TEXT DEFAULT '{}'
        )
    """)

    # Exercise progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercise_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exercise_path TEXT NOT NULL,
            category TEXT,
            attempts INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            first_attempt TEXT,
            last_attempt TEXT,
            time_spent_seconds INTEGER DEFAULT 0,
            notes TEXT,
            bookmarked BOOLEAN DEFAULT 0,
            UNIQUE(user_id, exercise_path),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Quiz results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_type TEXT,
            questions_count INTEGER,
            correct_count INTEGER,
            score REAL,
            time_taken_seconds INTEGER,
            taken_at TEXT DEFAULT CURRENT_TIMESTAMP,
            answers_json TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Achievements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            earned_at TEXT DEFAULT CURRENT_TIMESTAMP,
            metadata_json TEXT DEFAULT '{}',
            UNIQUE(user_id, achievement_type),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Time tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS time_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exercise_path TEXT,
            activity_type TEXT,
            duration_seconds INTEGER,
            logged_at TEXT DEFAULT CURRENT_TIMESTAMP,
            metadata_json TEXT DEFAULT '{}',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create indexes for performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_exercise_user
        ON exercise_progress(user_id, completed)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_exercise_category
        ON exercise_progress(category, completed)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_quiz_user
        ON quiz_results(user_id, taken_at)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_time_user
        ON time_logs(user_id, logged_at)
    """)

    conn.commit()
    conn.close()


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate_from_json(progress_file: str = ".progress.json") -> bool:
    """Migrate old JSON progress to SQLite database.

    Args:
        progress_file: Path to old progress.json file

    Returns:
        True if migration succeeded, False otherwise
    """
    if not os.path.exists(progress_file):
        return False

    try:
        with open(progress_file, 'r') as f:
            old_progress = json.load(f)

        if not old_progress:
            return False

        # Get or create default user
        user = get_active_user()
        if not user:
            user = create_user("default", "Default User")

        conn = get_connection()
        cursor = conn.cursor()

        for exercise_path, data in old_progress.items():
            # Check if already migrated
            cursor.execute("""
                SELECT id FROM exercise_progress
                WHERE user_id = ? AND exercise_path = ?
            """, (user['id'], exercise_path))

            if cursor.fetchone():
                continue  # Already exists

            # Extract category from path
            category = exercise_path.split('/')[0] if '/' in exercise_path else None

            cursor.execute("""
                INSERT INTO exercise_progress
                (user_id, exercise_path, category, attempts, completed,
                 first_attempt, last_attempt)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user['id'],
                exercise_path,
                category,
                data.get('attempts', 0),
                data.get('completed', False),
                data.get('first_attempt'),
                data.get('last_attempt')
            ))

        conn.commit()
        conn.close()

        # Rename old file as backup
        backup_name = f"{progress_file}.migrated"
        os.rename(progress_file, backup_name)

        return True

    except Exception as e:
        print(f"Migration failed: {e}")
        return False


def create_user(username: str, display_name: str = None) -> Dict[str, Any]:
    """Create a new user.

    Args:
        username: Unique username
        display_name: Optional display name

    Returns:
        User dict
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, display_name, is_active)
            VALUES (?, ?, 1)
        """, (username, display_name or username))

        # Deactivate other users
        cursor.execute("""
            UPDATE users SET is_active = 0 WHERE id != ?
        """, (cursor.lastrowid,))

        conn.commit()

        cursor.execute("""
            SELECT * FROM users WHERE id = ?
        """, (cursor.lastrowid,))

        user = dict(cursor.fetchone())
        conn.close()

        # Award first steps achievement
        award_achievement(user['id'], 'first_steps', 'First Steps', 'Started your Python journey!')

        return user

    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError(f"Username '{username}' already exists")


def get_active_user() -> Optional[Dict[str, Any]]:
    """Get currently active user.

    Returns:
        User dict or None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE is_active = 1 LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def set_active_user(user_id: int) -> bool:
    """Set a user as active.

    Args:
        user_id: User ID

    Returns:
        True if successful
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET is_active = 0")
    cursor.execute("UPDATE users SET is_active = 1, last_active = ? WHERE id = ?",
                   (datetime.now().isoformat(), user_id))

    conn.commit()
    conn.close()

    return True


def get_all_users() -> List[Dict[str, Any]]:
    """Get all users.

    Returns:
        List of user dicts
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY last_active DESC")
    users = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return users


def update_user_settings(user_id: int, settings: Dict[str, Any]) -> bool:
    """Update user settings.

    Args:
        user_id: User ID
        settings: Settings dict

    Returns:
        True if successful
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET settings_json = ?
        WHERE id = ?
    """, (json.dumps(settings), user_id))

    conn.commit()
    conn.close()

    return True


def get_user_settings(user_id: int) -> Dict[str, Any]:
    """Get user settings.

    Args:
        user_id: User ID

    Returns:
        Settings dict
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT settings_json FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row and row['settings_json']:
        return json.loads(row['settings_json'])
    return {}


def mark_exercise_complete(
    user_id: int,
    exercise_path: str,
    success: bool = True,
    time_spent: int = 0
) -> None:
    """Mark an exercise as complete (or failed).

    Args:
        user_id: User ID
        exercise_path: Full path to exercise
        success: Whether completed successfully
        time_spent: Time spent in seconds
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Extract category
    category = exercise_path.split('/')[0] if '/' in exercise_path else None
    now = datetime.now().isoformat()

    # Check if exists
    cursor.execute("""
        SELECT id, attempts, completed FROM exercise_progress
        WHERE user_id = ? AND exercise_path = ?
    """, (user_id, exercise_path))

    row = cursor.fetchone()

    if row:
        # Update existing
        cursor.execute("""
            UPDATE exercise_progress
            SET attempts = attempts + 1,
                completed = COALESCE(?, completed),
                last_attempt = ?,
                time_spent_seconds = time_spent_seconds + ?
            WHERE id = ?
        """, (success if success else None, now, time_spent, row['id']))
    else:
        # Insert new
        cursor.execute("""
            INSERT INTO exercise_progress
            (user_id, exercise_path, category, attempts, completed,
             first_attempt, last_attempt, time_spent_seconds)
            VALUES (?, ?, ?, 1, ?, ?, ?, ?)
        """, (user_id, exercise_path, category, success, now, now, time_spent))

    # Log time
    log_time(user_id, exercise_path, 'exercise', time_spent)

    conn.commit()
    conn.close()

    # Check achievements
    if success:
        check_completion_achievements(user_id)


def get_exercise_progress(user_id: int, exercise_path: str) -> Optional[Dict[str, Any]]:
    """Get progress for a specific exercise.

    Args:
        user_id: User ID
        exercise_path: Exercise path

    Returns:
        Progress dict or None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM exercise_progress
        WHERE user_id = ? AND exercise_path = ?
    """, (user_id, exercise_path))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def get_user_progress(user_id: int) -> Dict[str, Any]:
    """Get overall progress summary for user.

    Args:
        user_id: User ID

    Returns:
        Progress summary dict
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Total stats
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed,
            SUM(attempts) as total_attempts,
            SUM(time_spent_seconds) as total_time
        FROM exercise_progress
        WHERE user_id = ?
    """, (user_id,))

    stats = dict(cursor.fetchone())

    # By category
    cursor.execute("""
        SELECT
            category,
            COUNT(*) as total,
            SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed
        FROM exercise_progress
        WHERE user_id = ? AND category IS NOT NULL
        GROUP BY category
    """, (user_id,))

    by_category = {row['category']: dict(row) for row in cursor.fetchall()}

    conn.close()

    total = stats['total'] or 0
    completed = stats['completed'] or 0

    return {
        'total': total,
        'completed': completed,
        'remaining': total - completed,
        'percentage': round((completed / total * 100) if total > 0 else 0, 1),
        'total_attempts': stats['total_attempts'] or 0,
        'total_time_seconds': stats['total_time'] or 0,
        'by_category': by_category
    }


def save_quiz_result(
    user_id: int,
    quiz_type: str,
    questions_count: int,
    correct_count: int,
    time_taken: int,
    answers: List[Dict[str, Any]]
) -> int:
    """Save quiz result.

    Args:
        user_id: User ID
        quiz_type: Type of quiz
        questions_count: Number of questions
        correct_count: Number correct
        time_taken: Time in seconds
        answers: List of answer details

    Returns:
        Quiz result ID
    """
    conn = get_connection()
    cursor = conn.cursor()

    score = (correct_count / questions_count * 100) if questions_count > 0 else 0

    cursor.execute("""
        INSERT INTO quiz_results
        (user_id, quiz_type, questions_count, correct_count, score,
         time_taken_seconds, answers_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, quiz_type, questions_count, correct_count,
        score, time_taken, json.dumps(answers)
    ))

    quiz_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Check quiz achievements
    if score >= 100:
        award_achievement(user_id, 'perfect_quiz', 'Perfect Score',
                         'Got 100% on a quiz!')
    elif score >= 80:
        award_achievement(user_id, 'quiz_master', 'Quiz Master',
                         'Scored 80%+ on a quiz')

    return quiz_id


def get_quiz_history(user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
    """Get quiz history for user.

    Args:
        user_id: User ID
        limit: Max results

    Returns:
        List of quiz result dicts
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM quiz_results
        WHERE user_id = ?
        ORDER BY taken_at DESC
        LIMIT ?
    """, (user_id, limit))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return results


def award_achievement(
    user_id: int,
    achievement_type: str,
    title: str,
    description: str,
    metadata: Dict[str, Any] = None
) -> bool:
    """Award an achievement to a user.

    Args:
        user_id: User ID
        achievement_type: Unique achievement type
        title: Achievement title
        description: Description
        metadata: Optional metadata

    Returns:
        True if newly awarded, False if already had it
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if already has it
    cursor.execute("""
        SELECT id FROM achievements
        WHERE user_id = ? AND achievement_type = ?
    """, (user_id, achievement_type))

    if cursor.fetchone():
        conn.close()
        return False

    # Award it
    cursor.execute("""
        INSERT INTO achievements
        (user_id, achievement_type, title, description, metadata_json)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id, achievement_type, title, description,
        json.dumps(metadata or {})
    ))

    conn.commit()
    conn.close()

    return True


def get_user_achievements(user_id: int) -> List[Dict[str, Any]]:
    """Get all achievements for a user.

    Args:
        user_id: User ID

    Returns:
        List of achievement dicts
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM achievements
        WHERE user_id = ?
        ORDER BY earned_at DESC
    """, (user_id,))

    achievements = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return achievements


def check_completion_achievements(user_id: int) -> None:
    """Check and award completion achievements.

    Args:
        user_id: User ID
    """
    progress = get_user_progress(user_id)
    completed = progress['completed']

    # Milestone achievements
    milestones = {
        1: 'first_exercise',
        5: 'five_exercises',
        10: 'ten_exercises',
        25: 'twenty_five_exercises',
        50: 'fifty_exercises',
        100: 'hundred_exercises'
    }

    for count, achievement_type in milestones.items():
        if completed >= count:
            title = f"{count} Exercises {'Completed' if count < 100 else 'Club'}"
            award_achievement(user_id, achievement_type, title,
                           f"Completed {count} exercises!")

    # Category achievements
    for category, cat_stats in progress.get('by_category', {}).items():
        if cat_stats['completed'] >= cat_stats['total']:
            award_achievement(user_id, f"master_{category}",
                           f"{category.title()} Master",
                           f"Completed all {category} exercises!")


def log_time(
    user_id: int,
    exercise_path: str,
    activity_type: str,
    duration_seconds: int,
    metadata: Dict[str, Any] = None
) -> None:
    """Log time spent on an activity.

    Args:
        user_id: User ID
        exercise_path: Exercise path (optional)
        activity_type: Type of activity
        duration_seconds: Duration in seconds
        metadata: Optional metadata
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO time_logs
        (user_id, exercise_path, activity_type, duration_seconds, metadata_json)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id, exercise_path, activity_type,
        duration_seconds, json.dumps(metadata or {})
    ))

    conn.commit()
    conn.close()


def get_time_stats(
    user_id: int,
    days: int = 30
) -> Dict[str, Any]:
    """Get time statistics for user.

    Args:
        user_id: User ID
        days: Number of days to analyze

    Returns:
        Time stats dict
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            activity_type,
            SUM(duration_seconds) as total_seconds,
            COUNT(*) as sessions
        FROM time_logs
        WHERE user_id = ?
          AND date(logged_at) >= date('now', '-' || ? || ' days')
        GROUP BY activity_type
    """, (user_id, days))

    by_activity = {row['activity_type']: {
        'total_seconds': row['total_seconds'],
        'sessions': row['sessions']
    } for row in cursor.fetchall()}

    # Daily breakdown
    cursor.execute("""
        SELECT
            date(logged_at) as day,
            SUM(duration_seconds) as total_seconds
        FROM time_logs
        WHERE user_id = ?
          AND date(logged_at) >= date('now', '-' || ? || ' days')
        GROUP BY date(logged_at)
        ORDER BY day DESC
    """, (user_id, days))

    daily = [{**row} for row in cursor.fetchall()]

    conn.close()

    total_seconds = sum(s['total_seconds'] for s in by_activity.values())

    return {
        'total_seconds': total_seconds,
        'total_hours': round(total_seconds / 3600, 1),
        'by_activity': by_activity,
        'daily': daily,
        'period_days': days
    }


def export_user_data(user_id: int) -> Dict[str, Any]:
    """Export all user data as dict.

    Args:
        user_id: User ID

    Returns:
        Complete user data dict
    """
    conn = get_connection()
    cursor = conn.cursor()

    # User info
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = dict(cursor.fetchone())

    # Progress
    cursor.execute("""
        SELECT * FROM exercise_progress WHERE user_id = ?
    """, (user_id,))
    progress = [dict(row) for row in cursor.fetchall()]

    # Quizzes
    cursor.execute("""
        SELECT * FROM quiz_results WHERE user_id = ?
    """, (user_id,))
    quizzes = [dict(row) for row in cursor.fetchall()]

    # Achievements
    cursor.execute("""
        SELECT * FROM achievements WHERE user_id = ?
    """, (user_id,))
    achievements = [dict(row) for row in cursor.fetchall()]

    # Time logs (last 90 days)
    cursor.execute("""
        SELECT * FROM time_logs
        WHERE user_id = ?
        AND date(logged_at) >= date('now', '-90 days')
    """, (user_id,))
    time_logs = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        'exported_at': datetime.now().isoformat(),
        'user': user,
        'progress': progress,
        'quizzes': quizzes,
        'achievements': achievements,
        'time_logs': time_logs
    }


def import_user_data(data: Dict[str, Any], merge: bool = False) -> bool:
    """Import user data from export.

    Args:
        data: Export data dict
        merge: True to merge with existing, False to replace

    Returns:
        True if successful
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        user_data = data['user']

        # Insert/update user
        cursor.execute("""
            INSERT OR REPLACE INTO users
            (id, username, display_name, created_at, last_active, is_active, settings_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data['id'], user_data['username'],
            user_data.get('display_name'),
            user_data.get('created_at'),
            user_data.get('last_active'),
            user_data.get('is_active', 0),
            user_data.get('settings_json', '{}')
        ))

        if not merge:
            # Delete existing data for user
            cursor.execute("DELETE FROM exercise_progress WHERE user_id = ?", (user_data['id'],))
            cursor.execute("DELETE FROM quiz_results WHERE user_id = ?", (user_data['id'],))
            cursor.execute("DELETE FROM achievements WHERE user_id = ?", (user_data['id'],))
            cursor.execute("DELETE FROM time_logs WHERE user_id = ?", (user_data['id'],))

        # Import progress
        for prog in data.get('progress', []):
            cursor.execute("""
                INSERT OR REPLACE INTO exercise_progress
                (id, user_id, exercise_path, category, attempts, completed,
                 first_attempt, last_attempt, time_spent_seconds, notes, bookmarked)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prog['id'], prog['user_id'], prog['exercise_path'],
                prog.get('category'), prog['attempts'], prog['completed'],
                prog.get('first_attempt'), prog.get('last_attempt'),
                prog.get('time_spent_seconds', 0),
                prog.get('notes'), prog.get('bookmarked', 0)
            ))

        # Import quizzes
        for quiz in data.get('quizzes', []):
            cursor.execute("""
                INSERT OR REPLACE INTO quiz_results
                (id, user_id, quiz_type, questions_count, correct_count,
                 score, time_taken_seconds, taken_at, answers_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                quiz['id'], quiz['user_id'], quiz['quiz_type'],
                quiz['questions_count'], quiz['correct_count'],
                quiz['score'], quiz['time_taken_seconds'],
                quiz['taken_at'], quiz.get('answers_json', '[]')
            ))

        # Import achievements
        for ach in data.get('achievements', []):
            cursor.execute("""
                INSERT OR REPLACE INTO achievements
                (id, user_id, achievement_type, title, description, earned_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ach['id'], ach['user_id'], ach['achievement_type'],
                ach['title'], ach['description'],
                ach['earned_at'], ach.get('metadata_json', '{}')
            ))

        # Import time logs
        for log in data.get('time_logs', []):
            cursor.execute("""
                INSERT OR REPLACE INTO time_logs
                (id, user_id, exercise_path, activity_type, duration_seconds,
                 logged_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                log['id'], log['user_id'], log.get('exercise_path'),
                log['activity_type'], log['duration_seconds'],
                log['logged_at'], log.get('metadata_json', '{}')
            ))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"Import failed: {e}")
        return False


def backup_database() -> str:
    """Create a timestamped backup of the database.

    Returns:
        Path to backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"practice_{timestamp}.db"

    import shutil
    shutil.copy2(DB_FILE, backup_path)

    return str(backup_path)


if __name__ == '__main__':
    # Initialize and test
    init_database()
    print(f"Database initialized at: {DB_FILE}")

    # Test migration
    if migrate_from_json():
        print("Migrated data from .progress.json")
    else:
        print("No .progress.json found to migrate")

    # Show users
    users = get_all_users()
    print(f"\nUsers: {len(users)}")
    for user in users:
        print(f"  - {user['username']}: {user['display_name']}")
