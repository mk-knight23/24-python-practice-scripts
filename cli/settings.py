#!/usr/bin/env python3
"""
User settings and preferences management.

Handles difficulty, themes, and learning preferences.
"""

from __future__ import annotations

import sys
import os
import json
from typing import Dict, Any

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    init_database, get_active_user, get_all_users,
    set_active_user, update_user_settings, get_user_settings,
    create_user, export_user_data, import_user_data
)
from utils import clear, header, prompt, info, success, error, pause, line


# Default settings
DEFAULT_SETTINGS = {
    'difficulty': 'intermediate',  # beginner, intermediate, advanced
    'theme': 'dark',  # dark, light
    'show_hints': True,
    'auto_advance': False,
    'sound_enabled': False,
    'time_tracking': True,
    'daily_goal': 30,  # minutes
    'reminder_enabled': False,
    'reminder_time': '09:00'
}


def get_settings() -> Dict[str, Any]:
    """Get current user's settings with defaults.

    Returns:
        Settings dict
    """
    init_database()
    user = get_active_user()

    if not user:
        return DEFAULT_SETTINGS.copy()

    user_settings = get_user_settings(user['id'])
    return {**DEFAULT_SETTINGS, **user_settings}


def update_setting(key: str, value: Any) -> bool:
    """Update a single setting.

    Args:
        key: Setting key
        value: Setting value

    Returns:
        True if successful
    """
    init_database()
    user = get_active_user()

    if not user:
        error("No active user. Please create a profile first.")
        return False

    settings = get_settings()
    settings[key] = value

    return update_user_settings(user['id'], settings)


def settings_menu() -> None:
    """Settings configuration menu."""
    while True:
        clear()
        print(header("SETTINGS"))
        print()

        settings = get_settings()

        options = [
            ("difficulty", "Set difficulty level"),
            ("theme", "Choose theme"),
            ("show_hints", "Toggle hints"),
            ("auto_advance", "Toggle auto-advance"),
            ("daily_goal", "Set daily goal (minutes)"),
            ("profile", "Manage user profiles"),
            ("data", "Export/Import data"),
            ("reset", "Reset to defaults"),
        ]

        for i, (key, desc) in enumerate(options, 1):
            value = settings.get(key, 'N/A')
            if isinstance(value, bool):
                value = "On" if value else "Off"
            print(f"  [{i}] {desc:<30} [{value}]")

        print()
        print("  [0] Back")
        print()

        choice = prompt("Select setting: ")

        if choice == '0':
            break
        elif choice == '1':
            set_difficulty()
        elif choice == '2':
            set_theme()
        elif choice == '3':
            toggle_hints()
        elif choice == '4':
            toggle_auto_advance()
        elif choice == '5':
            set_daily_goal()
        elif choice == '6':
            profile_menu()
        elif choice == '7':
            data_menu()
        elif choice == '8':
            reset_settings()


def set_difficulty() -> None:
    """Set difficulty level."""
    clear()
    print(header("DIFFICULTY LEVEL"))
    print()

    current = get_settings().get('difficulty', 'intermediate')

    info(f"Current: {current.upper()}")
    print()
    info("  [1] Beginner     - More hints, slower pace")
    info("  [2] Intermediate - Balanced learning")
    info("  [3] Advanced     - Minimal guidance")
    print()

    choice = prompt("Select difficulty: ")

    levels = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
    if choice in levels:
        if update_setting('difficulty', levels[choice]):
            success(f"Difficulty set to {levels[choice].upper()}")
        else:
            error("Failed to update setting")

    pause()


def set_theme() -> None:
    """Set color theme."""
    clear()
    print(header("THEME"))
    print()

    current = get_settings().get('theme', 'dark')

    info(f"Current: {current.upper()}")
    print()
    info("  [1] Dark  - Easy on the eyes (recommended)")
    info("  [2] Light - Clean and bright")
    print()

    choice = prompt("Select theme: ")

    themes = {'1': 'dark', '2': 'light'}
    if choice in themes:
        if update_setting('theme', themes[choice]):
            success(f"Theme set to {themes[choice].upper()}")
        else:
            error("Failed to update setting")

    pause()


def toggle_hints() -> None:
    """Toggle hints display."""
    current = get_settings().get('show_hints', True)
    new_value = not current

    if update_setting('show_hints', new_value):
        status = "ENABLED" if new_value else "DISABLED"
        success(f"Hints {status}")
    else:
        error("Failed to update setting")

    pause()


def toggle_auto_advance() -> None:
    """Toggle auto-advance to next exercise."""
    current = get_settings().get('auto_advance', False)
    new_value = not current

    if update_setting('auto_advance', new_value):
        status = "ENABLED" if new_value else "DISABLED"
        success(f"Auto-advance {status}")
    else:
        error("Failed to update setting")

    pause()


def set_daily_goal() -> None:
    """Set daily learning goal in minutes."""
    clear()
    print(header("DAILY GOAL"))
    print()

    current = get_settings().get('daily_goal', 30)
    info(f"Current goal: {current} minutes/day")
    print()

    choice = prompt("Set new goal (minutes): ")

    try:
        minutes = int(choice)
        if 5 <= minutes <= 240:
            if update_setting('daily_goal', minutes):
                success(f"Daily goal set to {minutes} minutes")
            else:
                error("Failed to update setting")
        else:
            error("Goal must be between 5 and 240 minutes")
    except ValueError:
        error("Invalid number")

    pause()


def reset_settings() -> None:
    """Reset settings to defaults."""
    clear()
    print(header("RESET SETTINGS"))
    print()
    info("This will reset all settings to default values.")
    print()

    confirm = prompt("Are you sure? (yes/no): ").strip().lower()

    if confirm == 'yes':
        init_database()
        user = get_active_user()
        if user and update_user_settings(user['id'], DEFAULT_SETTINGS):
            success("Settings reset to defaults")
        else:
            error("Failed to reset settings")
    else:
        info("Cancelled")

    pause()


def profile_menu() -> None:
    """User profile management menu."""
    while True:
        clear()
        print(header("USER PROFILES"))
        print()

        users = get_all_users()
        active = get_active_user()

        for i, user in enumerate(users):
            is_active = "✓" if user['id'] == active['id'] else " "
            print(f"  [{is_active}] {user['display_name']} (@{user['username']})")
            print(f"       Created: {user['created_at'][:10]}")
            print()

        print("  [1] Create new profile")
        print("  [2] Switch profile")
        print("  [0] Back")
        print()

        choice = prompt("Select option: ")

        if choice == '0':
            break
        elif choice == '1':
            create_new_profile()
        elif choice == '2':
            switch_profile()


def create_new_profile() -> None:
    """Create a new user profile."""
    clear()
    print(header("CREATE PROFILE"))
    print()

    username = prompt("Username: ").strip()
    if not username:
        error("Username cannot be empty")
        pause()
        return

    display_name = prompt("Display name (optional): ").strip() or username

    try:
        user = create_user(username, display_name)
        success(f"Profile created: {display_name}")
        info("You are now logged in as this profile.")
    except ValueError as e:
        error(str(e))

    pause()


def switch_profile() -> None:
    """Switch to a different profile."""
    users = get_all_users()

    if len(users) < 2:
        error("You need at least 2 profiles to switch.")
        pause()
        return

    clear()
    print(header("SWITCH PROFILE"))
    print()

    for i, user in enumerate(users, 1):
        print(f"  [{i}] {user['display_name']} (@{user['username']})")

    print()
    choice = prompt("Select profile: ")

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(users):
            user = users[idx]
            set_active_user(user['id'])
            success(f"Switched to {user['display_name']}")
        else:
            error("Invalid selection")
    except ValueError:
        error("Invalid input")

    pause()


def data_menu() -> None:
    """Data export/import menu."""
    while True:
        clear()
        print(header("DATA MANAGEMENT"))
        print()

        options = [
            ("export", "Export all data to JSON"),
            ("import", "Import data from JSON"),
            ("backup", "Create database backup"),
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
            export_data()
        elif choice == '2':
            import_data()
        elif choice == '3':
            backup_database()


def export_data() -> None:
    """Export user data to JSON file."""
    init_database()
    user = get_active_user()

    if not user:
        error("No active user found.")
        pause()
        return

    clear()
    print(header("EXPORT DATA"))
    print()

    data = export_user_data(user['id'])
    filename = f"python_practice_export_{user['username']}_{data['exported_at'][:10]}.json"

    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        success(f"Data exported to: {filename}")
        info(f"File size: {os.path.getsize(filename)} bytes")
    except Exception as e:
        error(f"Export failed: {e}")

    pause()


def import_data() -> None:
    """Import user data from JSON file."""
    clear()
    print(header("IMPORT DATA"))
    print()

    filename = prompt("Enter filename: ").strip()

    if not os.path.exists(filename):
        error(f"File not found: {filename}")
        pause()
        return

    print()
    info("Import options:")
    info("  [1] Merge with existing data")
    info("  [2] Replace existing data")
    print()

    choice = prompt("Select option: ")

    merge = choice == '1'

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        if import_user_data(data, merge=merge):
            success("Data imported successfully")
            if merge:
                info("Merged with existing data")
            else:
                info("Replaced existing data")
        else:
            error("Import failed")
    except json.JSONDecodeError:
        error("Invalid JSON file")
    except Exception as e:
        error(f"Import failed: {e}")

    pause()


def backup_database() -> None:
    """Create a database backup."""
    from database import backup_database

    clear()
    print(header("BACKUP DATABASE"))
    print()

    try:
        backup_path = backup_database()
        success(f"Backup created: {backup_path}")
        info(f"Size: {os.path.getsize(backup_path)} bytes")
    except Exception as e:
        error(f"Backup failed: {e}")

    pause()


if __name__ == '__main__':
    settings_menu()
