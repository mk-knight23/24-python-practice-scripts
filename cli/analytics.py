#!/usr/bin/env python3
"""
Analytics dashboard for progress tracking and insights.

Provides charts, statistics, and time tracking analysis.
"""

from __future__ import annotations

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    init_database, get_active_user, get_user_progress,
    get_time_stats, get_quiz_history, get_user_achievements
)
from utils import clear, header, info, pause, line


def format_duration(seconds: int) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        mins = seconds // 60
        return f"{mins}m"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours}h {mins}m" if mins > 0 else f"{hours}h"


def draw_bar_chart(values: List[int], labels: List[str], width: int = 40) -> str:
    """Draw a simple text-based bar chart.

    Args:
        values: List of values
        labels: List of labels
        width: Max width of bars

    Returns:
        Formatted chart string
    """
    if not values:
        return "No data available"

    max_val = max(values)
    lines = []

    for value, label in zip(values, labels):
        bar_len = int((value / max_val) * width) if max_val > 0 else 0
        bar = "█" * bar_len
        lines.append(f"  {label:<15} {bar} {value}")

    return "\n".join(lines)


def show_dashboard() -> None:
    """Show main analytics dashboard."""
    init_database()
    user = get_active_user()

    if not user:
        clear()
        print(header("ANALYTICS"))
        print()
        info("No active user. Create a profile first.")
        print()
        pause()
        return

    clear()
    print(header("ANALYTICS DASHBOARD"))
    print()

    info(f"User: {user['display_name']}")
    print()

    # Overall progress
    progress = get_user_progress(user['id'])

    print(line('=', 60))
    print("  OVERALL PROGRESS")
    print(line('=', 60))
    print()

    # Progress bar
    percent = progress['percentage']
    bar_len = int(percent / 5)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    print(f"  Total Progress:  {bar} {percent}%")
    print()
    print(f"  Completed:       {progress['completed']} exercises")
    print(f"  Remaining:       {progress['remaining']} exercises")
    print(f"  Total Attempts:  {progress['total_attempts']}")
    print(f"  Time Spent:      {format_duration(progress['total_time_seconds'])}")
    print()

    # Category breakdown
    if progress.get('by_category'):
        print(line('=', 60))
        print("  BY CATEGORY")
        print(line('=', 60))
        print()

        for category, cat_stats in progress['by_category'].items():
            cat_total = cat_stats['total']
            cat_completed = cat_stats['completed']
            cat_percent = int((cat_completed / cat_total) * 100) if cat_total > 0 else 0
            cat_bar = "█" * (cat_percent // 5) + "░" * (20 - cat_percent // 5)
            print(f"  {category.title():<12} {cat_bar} {cat_percent}% ({cat_completed}/{cat_total})")
        print()

    # Time stats
    time_stats = get_time_stats(user['id'], days=30)

    print(line('=', 60))
    print(f"  TIME SPENT (Last {time_stats['period_days']} days)")
    print(line('=', 60))
    print()

    print(f"  Total: {time_stats['total_hours']} hours")
    print()

    if time_stats['by_activity']:
        print("  By Activity:")
        for activity, stats in time_stats['by_activity'].items():
            print(f"    {activity.title():<15} {format_duration(stats['total_seconds'])} "
                  f"({stats['sessions']} sessions)")
        print()

    # Quiz performance
    quizzes = get_quiz_history(user['id'], limit=10)

    if quizzes:
        print(line('=', 60))
        print("  RECENT QUIZ PERFORMANCE")
        print(line('=', 60))
        print()

        # Calculate average
        avg_score = sum(q['score'] for q in quizzes) / len(quizzes)

        print(f"  Quizzes Taken:   {len(quizzes)}")
        print(f"  Average Score:   {avg_score:.1f}%")
        print(f"  Best Score:      {max(q['score'] for q in quizzes):.0f}%")
        print()

        # Last 5 quiz scores
        recent = quizzes[:5]
        scores = [int(q['score']) for q in recent]
        labels = [q['taken_at'][5:10] for q in recent]

        print("  Recent Scores:")
        print(draw_bar_chart(scores, labels))
        print()

    # Achievements
    achievements = get_user_achievements(user['id'])

    if achievements:
        print(line('=', 60))
        print("  ACHIEVEMENTS")
        print(line('=', 60))
        print()

        print(f"  Total Earned: {len(achievements)}")

        # Recent achievements
        recent = achievements[:5]
        for ach in recent:
            print(f"  ✓ {ach['title']} - {ach['description']}")
        print()

    print(line('=', 60))
    print()

    pause()


def show_time_analysis() -> None:
    """Show detailed time analysis."""
    init_database()
    user = get_active_user()

    if not user:
        error("No active user found.")
        return

    clear()
    print(header("TIME ANALYSIS"))
    print()

    # Different time periods
    periods = [7, 14, 30, 90]

    for days in periods:
        stats = get_time_stats(user['id'], days=days)
        print(f"  Last {days} days: {format_duration(stats['total_seconds'])}")

    print()

    # Daily breakdown (last 7 days)
    stats = get_time_stats(user['id'], days=7)

    print(line('=', 60))
    print("  DAILY BREAKDOWN (Last 7 days)")
    print(line('=', 60))
    print()

    if stats['daily']:
        # Reverse to show most recent first
        daily = list(reversed(stats['daily']))

        for day in daily:
            date_str = day['day']
            seconds = day['total_seconds']
            hours = seconds / 3600

            bar_len = min(40, int(hours / 2 * 40))  # Scale: 2h = full bar
            bar = "█" * bar_len
            print(f"  {date_str:<12} {bar} {hours:.1f}h")

        print()

        # Calculate average
        avg_hours = stats['total_seconds'] / 3600 / 7
        info(f"Average: {avg_hours:.1f} hours/day")

        # Daily goal check
        from settings import get_settings
        settings = get_settings()
        daily_goal_minutes = settings.get('daily_goal', 30)
        daily_goal_hours = daily_goal_minutes / 60

        if avg_hours >= daily_goal_hours:
            success(f"✓ Meeting daily goal of {daily_goal_minutes} minutes!")
        else:
            remaining = (daily_goal_hours - avg_hours) * 60
            info(f"Target: {daily_goal_minutes} min/day ({remaining:.0f} min more)")

        print()

    print(line('=', 60))
    print()

    pause()


def show_category_analysis() -> None:
    """Show category-wise analysis."""
    init_database()
    user = get_active_user()

    if not user:
        error("No active user found.")
        return

    clear()
    print(header("CATEGORY ANALYSIS"))
    print()

    progress = get_user_progress(user['id'])

    if not progress.get('by_category'):
        info("No category data available yet.")
        print()
        pause()
        return

    for category, cat_stats in progress['by_category'].items():
        print(line('=', 60))
        print(f"  {category.upper()}")
        print(line('=', 60))
        print()

        total = cat_stats['total']
        completed = cat_stats['completed']
        remaining = total - completed
        percent = int((completed / total) * 100) if total > 0 else 0

        print(f"  Progress:     {percent}%")
        print(f"  Completed:    {completed}/{total}")
        print(f"  Remaining:    {remaining}")
        print()

        # Progress bar
        bar_len = int(percent / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {bar}")
        print()

        if remaining == 0:
            success(f"✓ All {category} exercises completed!")
        elif percent >= 50:
            success(f"✓ Over halfway through {category}!")
        else:
            info(f"→ Keep working on {category} exercises")

        print()

    pause()


def show_streaks() -> None:
    """Show learning streaks."""
    init_database()
    user = get_active_user()

    if not user:
        error("No active user found.")
        return

    clear()
    print(header("LEARNING STREAKS"))
    print()

    # Calculate streaks from time logs
    from database import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    # Get activity by date
    cursor.execute("""
        SELECT
            date(logged_at) as day,
            SUM(duration_seconds) as total_seconds
        FROM time_logs
        WHERE user_id = ?
        GROUP BY date(logged_at)
        ORDER BY day DESC
        LIMIT 90
    """, (user['id'],))

    days = cursor.fetchall()
    conn.close()

    if not days:
        info("No activity recorded yet.")
        print()
        pause()
        return

    # Calculate current streak
    today = datetime.now().date()
    current_streak = 0

    for i, day in enumerate(days):
        day_date = datetime.strptime(day['day'], '%Y-%m-%d').date()
        expected_date = today - timedelta(days=i)

        if day_date == expected_date and day['total_seconds'] >= 300:  # At least 5 min
            current_streak += 1
        else:
            break

    # Calculate longest streak
    longest_streak = 1
    temp_streak = 1

    for i in range(1, len(days)):
        prev_date = datetime.strptime(days[i-1]['day'], '%Y-%m-%d').date()
        curr_date = datetime.strptime(days[i]['day'], '%Y-%m-%d').date()

        if (prev_date - curr_date).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    print(line('=', 60))
    print("  STREAK STATS")
    print(line('=', 60))
    print()

    print(f"  Current Streak:  {current_streak} days")
    print(f"  Longest Streak:  {longest_streak} days")
    print()

    if current_streak >= 7:
        success(f"🔥 {current_streak} day streak! Keep it up!")
    elif current_streak >= 3:
        success(f"✓ {current_streak} day streak - building momentum!")
    elif current_streak == 1:
        info("→ Start your streak today!")
    else:
        info("→ No active streak - start learning today!")

    print()

    # Recent activity
    print(line('=', 60))
    print("  RECENT ACTIVITY")
    print(line('=', 60))
    print()

    for day in days[:7]:
        date_str = day['day']
        duration = format_duration(day['total_seconds'])
        print(f"  {date_str}: {duration}")

    print()
    print(line('=', 60))
    print()

    pause()


def analytics_menu() -> None:
    """Analytics menu."""
    while True:
        clear()
        print(header("ANALYTICS"))
        print()

        options = [
            ("dashboard", "View analytics dashboard"),
            ("time", "Time analysis"),
            ("category", "Category breakdown"),
            ("streaks", "Learning streaks"),
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
            show_dashboard()
        elif choice == '2':
            show_time_analysis()
        elif choice == '3':
            show_category_analysis()
        elif choice == '4':
            show_streaks()


if __name__ == '__main__':
    analytics_menu()
