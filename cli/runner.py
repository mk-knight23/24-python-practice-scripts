#!/usr/bin/env python3
"""
Main CLI interface for the Python practice system.

Run with: python cli/runner.py
Or: ./cli/runner.py (if executable)
"""

from __future__ import annotations

import os
import sys
from typing import List, Tuple, Optional
from datetime import datetime

# Add parent dir to path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    clear, ascii_header, menu, prompt, box, code_block,
    list_exercises, read_exercise_info, run_python_file,
    success, error, info, pause, header, line
)
from progress import (
    mark_exercise_complete, format_summary, get_summary,
    get_exercise_progress
)

# Import new features
try:
    from database import init_database, get_active_user
    from quiz import quiz_menu
    from achievements import achievements_menu
    from settings import settings_menu, get_settings
    from analytics import analytics_menu
    HAS_FEATURES = True
except ImportError:
    HAS_FEATURES = False


def show_welcome():
    """Display the welcome screen."""
    clear()
    print(ascii_header())
    print()
    info("This is a hands-on Python learning system.")
    info("Each exercise is a real .py file you can edit.")
    info("")
    info("Structure:")
    info("  basics    - Variables, types, loops, conditionals")
    info("  core      - Functions, files, error handling")
    info("  advanced  - OOP, decorators, generators")
    print()
    pause()


def show_exercise_menu(exercises: List[Tuple[str, str, str]], category: Optional[str] = None) -> Optional[Tuple[str, str, str]]:
    """Show exercises as a menu.

    Args:
        exercises: List of (category, filename, path) tuples
        category: Optional category to filter by

    Returns:
        Selected exercise tuple, or None if cancelled
    """
    clear()
    
    if category:
        print(header(f"{category.upper()} EXERCISES"))
    else:
        print(header("ALL EXERCISES"))
    
    print()
    
    # Filter by category if specified
    filtered = [e for e in exercises if not category or e[0] == category]
    
    if not filtered:
        error("No exercises found.")
        pause()
        return None
    
    # Show numbered list
    for i, (cat, filename, path) in enumerate(filtered, 1):
        # Get short description
        info_dict = read_exercise_info(path)
        desc = info_dict['purpose'][:40] + '...' if len(info_dict['purpose']) > 40 else info_dict['purpose']
        cat_label = f"[{cat[:3]}]"
        print(f"  {i:2}. {cat_label} {filename:<25} {desc}")
    
    print()
    print(f"  0. Back")
    print()
    
    choice = prompt("Select exercise (number): ")
    
    if choice == '0':
        return None
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(filtered):
            return filtered[idx]
    except ValueError:
        pass
    
    error("Invalid selection.")
    pause()
    return None


def show_exercise_detail(category: str, filename: str, filepath: str) -> None:
    """Show full details of an exercise.

    Args:
        category: Exercise category (basics, core, advanced)
        filename: Exercise filename
        filepath: Full path to exercise file
    """
    while True:
        clear()
        info_dict = read_exercise_info(filepath)
        
        # Header
        print(header(f"EXERCISE: {filename}"))
        print()
        print(f"  Category: {category}")
        print(f"  Path:     {filepath}")
        print()
        
        # Purpose
        print(line('-', 60))
        print("  PURPOSE")
        print(line('-', 60))
        print(f"  {info_dict['purpose']}")
        print()
        
        # Why
        if info_dict['why']:
            print(line('-', 60))
            print("  WHY IT MATTERS")
            print(line('-', 60))
            print(f"  {info_dict['why']}")
            print()
        
        # Examples
        if info_dict['examples']:
            print(line('-', 60))
            print("  EXAMPLES")
            print(line('-', 60))
            for ex in info_dict['examples']:
                print(f"  {ex}")
            print()
        
        # Menu
        print(line('-', 60))
        print("  [1] View source code")
        print("  [2] Run exercise")
        print("  [3] Edit file (opens in $EDITOR)")
        print("  [0] Back")
        print(line('-', 60))
        
        choice = prompt(">>> ")
        
        if choice == '1':
            show_source(info_dict['code'], filename)
        elif choice == '2':
            run_exercise(filepath)
        elif choice == '3':
            edit_file(filepath)
        elif choice == '0':
            break


def show_source(code: str, filename: str) -> None:
    """Display the source code.

    Args:
        code: Source code content
        filename: Name of file being displayed
    """
    clear()
    print(header(f"SOURCE: {filename}"))
    print()
    print(code_block(code))
    print()
    pause()


def run_exercise(filepath: str) -> None:
    """Run the exercise and show output.

    Args:
        filepath: Full path to exercise file
    """
    clear()
    print(header("RUNNING EXERCISE"))
    print()
    info(f"File: {filepath}")
    print()

    # Show current progress if available
    prog = get_exercise_progress(filepath)
    if prog:
        attempts = prog.get('attempts', 0)
        if attempts > 0:
            info(f"Previous attempts: {attempts}")
        if prog.get('completed'):
            success("Previously completed ✓")
    print()

    print(line('=', 60))

    start_time = datetime.now()
    success_flag, output = run_python_file(filepath)
    end_time = datetime.now()

    print(output)
    print(line('=', 60))
    print()

    # Calculate time spent
    time_spent = int((end_time - start_time).total_seconds())

    # Mark progress
    mark_exercise_complete(filepath, success_flag, time_spent)

    if success_flag:
        success("Exercise completed successfully.")
        # Show updated summary
        summary = get_summary()
        info(f"Total progress: {summary['completed']}/{summary['total']} exercises ({summary['percentage']}%)")
    else:
        error("Exercise encountered an error.")

    pause()


def edit_file(filepath: str) -> None:
    """Open file in default editor.

    Args:
        filepath: Full path to file to edit
    """
    editor = os.environ.get('EDITOR', 'nano')
    print(f"Opening {filepath} in {editor}...")
    print("(Save and exit to return to this menu)")
    os.system(f"{editor} {filepath}")


def show_progress_screen() -> None:
    """Display detailed progress information."""
    clear()
    print(header("PROGRESS TRACKING"))
    print()
    print(format_summary())
    print()
    pause()


def main_menu() -> None:
    """Main menu loop."""
    # Initialize database if available
    if HAS_FEATURES:
        init_database()

    exercises = list_exercises()

    if not exercises:
        error("No exercises found in skills/ directory.")
        error("Make sure you're running from the project root.")
        sys.exit(1)

    while True:
        clear()
        print(ascii_header())
        print()

        # Show user if logged in
        if HAS_FEATURES:
            user = get_active_user()
            if user:
                info(f"User: {user['display_name']}")
            else:
                info("Guest mode (Create profile to track progress)")
            print()

        # Show progress summary if available
        summary = get_summary()
        if summary['total'] > 0:
            info(f"Progress: {summary['completed']}/{summary['total']} exercises ({summary['percentage']}%)")
            print()

        options = [
            ("basics", "Variables, types, loops, conditionals"),
            ("core", "Functions, file handling, error handling"),
            ("advanced", "OOP, decorators, generators"),
            ("all", "Browse all exercises"),
            ("progress", "View detailed progress"),
        ]

        # Add new features if available
        if HAS_FEATURES:
            options.extend([
                ("quiz", "Test your knowledge with quizzes"),
                ("achievements", "View achievements and badges"),
                ("analytics", "Progress analytics and insights"),
                ("settings", "User settings and preferences"),
            ])

        print(menu(options, "SELECT A CATEGORY"))
        print()

        choice = prompt(">>> ")

        if choice == '0':
            print()
            info("Happy coding. Come back when you're stuck.")
            # Show final progress
            if summary['total'] > 0:
                print()
                print(format_summary())
            print()
            break
        elif choice == '1':
            result = show_exercise_menu(exercises, 'basics')
            if result:
                show_exercise_detail(*result)
        elif choice == '2':
            result = show_exercise_menu(exercises, 'core')
            if result:
                show_exercise_detail(*result)
        elif choice == '3':
            result = show_exercise_menu(exercises, 'advanced')
            if result:
                show_exercise_detail(*result)
        elif choice == '4':
            result = show_exercise_menu(exercises)
            if result:
                show_exercise_detail(*result)
        elif choice == '5':
            show_progress_screen()
        elif HAS_FEATURES:
            if choice == '6':
                quiz_menu()
            elif choice == '7':
                achievements_menu()
            elif choice == '8':
                analytics_menu()
            elif choice == '9':
                settings_menu()


def main() -> None:
    """Entry point."""
    # Check if running for first time
    if len(sys.argv) > 1 and sys.argv[1] == '--welcome':
        show_welcome()
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print()
        print()
        info("Interrupted. Progress saved (it's just files on disk).")
        sys.exit(0)


if __name__ == '__main__':
    main()
