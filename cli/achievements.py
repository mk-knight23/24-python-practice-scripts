#!/usr/bin/env python3
"""
Achievements and badges system for gamification.

Tracks milestones and awards badges for accomplishments.
"""

from __future__ import annotations

import sys
import os
from typing import Dict, List
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    init_database, get_active_user, get_user_achievements,
    get_user_progress, award_achievement
)
from utils import clear, header, info, pause, line


# Achievement definitions (for reference and display)
ACHIEVEMENT_DEFINITIONS = {
    # First steps
    'first_steps': {
        'title': 'First Steps',
        'description': 'Started your Python journey!',
        'icon': '🚀',
        'category': 'milestone'
    },

    # Exercise completion milestones
    'first_exercise': {
        'title': 'Hello World',
        'description': 'Completed your first exercise',
        'icon': '👋',
        'category': 'completion'
    },
    'five_exercises': {
        'title': 'Getting Started',
        'description': 'Completed 5 exercises',
        'icon': '📝',
        'category': 'completion'
    },
    'ten_exercises': {
        'title': ' Dedicated Learner',
        'description': 'Completed 10 exercises',
        'icon': '🎯',
        'category': 'completion'
    },
    'twenty_five_exercises': {
        'title': 'Quarter Century',
        'description': 'Completed 25 exercises',
        'icon': '💪',
        'category': 'completion'
    },
    'fifty_exercises': {
        'title': 'Half Century',
        'description': 'Completed 50 exercises',
        'icon': '⭐',
        'category': 'completion'
    },
    'hundred_exercises': {
        'title': 'Century Club',
        'description': 'Completed 100 exercises!',
        'icon': '🏆',
        'category': 'completion'
    },

    # Category mastery
    'master_basics': {
        'title': 'Basics Master',
        'description': 'Completed all basics exercises',
        'icon': '🎓',
        'category': 'mastery'
    },
    'master_core': {
        'title': 'Core Master',
        'description': 'Completed all core exercises',
        'icon': '🔧',
        'category': 'mastery'
    },
    'master_advanced': {
        'title': 'Advanced Master',
        'description': 'Completed all advanced exercises',
        'icon': '🧠',
        'category': 'mastery'
    },

    # Quiz achievements
    'perfect_quiz': {
        'title': 'Perfect Score',
        'description': 'Got 100% on a quiz',
        'icon': '💯',
        'category': 'quiz'
    },
    'quiz_master': {
        'title': 'Quiz Master',
        'description': 'Scored 80%+ on a quiz',
        'icon': '🧩',
        'category': 'quiz'
    },

    # Time-based
    'first_hour': {
        'title': 'Time Well Spent',
        'description': 'Spent 1 hour learning',
        'icon': '⏰',
        'category': 'time'
    },
    'five_hours': {
        'title': 'Dedicated Student',
        'description': 'Spent 5 hours learning',
        'icon': '📚',
        'category': 'time'
    },
    'ten_hours': {
        'title': 'Python Enthusiast',
        'description': 'Spent 10 hours learning',
        'icon': '🔥',
        'category': 'time'
    }
}


def show_achievements() -> None:
    """Display user's achievements."""
    init_database()
    user = get_active_user()

    if not user:
        clear()
        print(header("ACHIEVEMENTS"))
        print()
        info("No active user. Create a profile first.")
        print()
        pause()
        return

    clear()
    print(header("ACHIEVEMENTS"))
    print()

    earned = get_user_achievements(user['id'])
    earned_types = {a['achievement_type'] for a in earned}

    print(f"  {user['display_name']}")
    print(f"  Earned: {len(earned)}/{len(ACHIEVEMENT_DEFINITIONS)}")
    print()
    print(line('=', 60))
    print()

    # Group by category
    categories = {
        'milestone': '🎖️  MILESTONES',
        'completion': '✅ COMPLETION',
        'mastery': '🎓MASTERY',
        'quiz': '🧩 QUIZZES',
        'time': '⏰ TIME'
    }

    for cat_key, cat_title in categories.items():
        # Get achievements in this category
        cat_achievements = {
            k: v for k, v in ACHIEVEMENT_DEFINITIONS.items()
            if v['category'] == cat_key
        }

        if not cat_achievements:
            continue

        print(f"  {cat_title}")
        print(line('-', 60))

        for ach_type, ach_def in cat_achievements.items():
            is_earned = ach_type in earned_types
            status = "✓" if is_earned else " "
            icon = ach_def['icon'] if is_earned else "🔒"

            print(f"  [{status}] {icon} {ach_def['title']}")
            print(f"       {ach_def['description']}")
            print()

    print(line('=', 60))
    print()

    # Time-based achievements check
    progress = get_user_progress(user['id'])
    total_hours = progress['total_time_seconds'] / 3600

    info(f"Total time learning: {total_hours:.1f} hours")
    info(f"Exercises completed: {progress['completed']}")
    print()

    pause()


def check_time_achievements(user_id: int, total_seconds: int) -> None:
    """Check and award time-based achievements.

    Args:
        user_id: User ID
        total_seconds: Total time in seconds
    """
    hours = total_seconds / 3600

    if hours >= 1:
        award_achievement(user_id, 'first_hour',
                         ACHIEVEMENT_DEFINITIONS['first_hour']['title'],
                         ACHIEVEMENT_DEFINITIONS['first_hour']['description'])

    if hours >= 5:
        award_achievement(user_id, 'five_hours',
                         ACHIEVEMENT_DEFINITIONS['five_hours']['title'],
                         ACHIEVEMENT_DEFINITIONS['five_hours']['description'])

    if hours >= 10:
        award_achievement(user_id, 'ten_hours',
                         ACHIEVEMENT_DEFINITIONS['ten_hours']['title'],
                         ACHIEVEMENT_DEFINITIONS['ten_hours']['description'])


def show_progress_achievements() -> None:
    """Show progress toward next achievements."""
    init_database()
    user = get_active_user()

    if not user:
        error("No active user found.")
        return

    clear()
    print(header("ACHIEVEMENT PROGRESS"))
    print()

    progress = get_user_progress(user['id'])
    earned = get_user_achievements(user['id'])
    earned_types = {a['achievement_type'] for a in earned}

    info(f"Exercises completed: {progress['completed']}")
    print()

    # Next completion milestones
    print("  Next Milestones:")
    print()

    milestones = [
        (1, 'first_exercise', '👋'),
        (5, 'five_exercises', '📝'),
        (10, 'ten_exercises', '🎯'),
        (25, 'twenty_five_exercises', '💪'),
        (50, 'fifty_exercises', '⭐'),
        (100, 'hundred_exercises', '🏆')
    ]

    for count, ach_type, icon in milestones:
        if ach_type not in earned_types:
            remaining = max(0, count - progress['completed'])
            percent = min(100, int((progress['completed'] / count) * 100))
            bar = "█" * (percent // 5) + "░" * (20 - percent // 5)
            print(f"    {icon} {count} exercises: {bar} {percent}%")
            print(f"       {remaining} more to go")
            print()

    # Category progress
    print("  Category Mastery:")
    print()

    for category, cat_stats in progress.get('by_category', {}).items():
        ach_type = f"master_{category}"
        if ach_type not in earned_types:
            cat_total = cat_stats['total']
            cat_completed = cat_stats['completed']
            cat_percent = int((cat_completed / cat_total) * 100) if cat_total > 0 else 0
            bar = "█" * (cat_percent // 5) + "░" * (20 - cat_percent // 5)
            print(f"    {category.title()}: {bar} {cat_percent}%")
            print(f"       {cat_total - cat_completed} remaining")
            print()

    # Time progress
    total_hours = progress['total_time_seconds'] / 3600
    print("  Time Achievements:")
    print()

    time_milestones = [
        (1, 'first_hour', '⏰'),
        (5, 'five_hours', '📚'),
        (10, 'ten_hours', '🔥')
    ]

    for hours, ach_type, icon in time_milestones:
        if ach_type not in earned_types:
            hours_remaining = max(0, hours - total_hours)
            percent = min(100, int((total_hours / hours) * 100))
            bar = "█" * (percent // 5) + "░" * (20 - percent // 5)
            print(f"    {icon} {hours} hour: {bar} {percent}%")
            print(f"       {hours_remaining:.1f}h more")
            print()

    print(line('=', 60))
    print()

    pause()


def achievements_menu() -> None:
    """Achievements menu."""
    while True:
        clear()
        print(header("ACHIEVEMENTS"))
        print()

        options = [
            ("view", "View your achievements"),
            ("progress", "Track progress to next achievements"),
        ]

        for i, (key, desc) in enumerate(options, 1):
            print(f"  [{i}] {desc}")

        print()
        print("  [0] Back")
        print()

        choice = prompt("Select option: ")

        if choice == '0':
            break
        elif choice == '1':
            show_achievements()
        elif choice == '2':
            show_progress_achievements()


if __name__ == '__main__':
    achievements_menu()
