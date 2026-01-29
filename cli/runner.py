#!/usr/bin/env python3
"""
Main CLI interface for the Python practice system.

Run with: python cli/runner.py
Or: ./cli/runner.py (if executable)
"""

import os
import sys

# Add parent dir to path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    clear, ascii_header, menu, prompt, box, code_block,
    list_exercises, read_exercise_info, run_python_file,
    success, error, info, pause, header, line
)


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


def show_exercise_menu(exercises: list, category: str = None):
    """Show exercises as a menu."""
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


def show_exercise_detail(category: str, filename: str, filepath: str):
    """Show full details of an exercise."""
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


def show_source(code: str, filename: str):
    """Display the source code."""
    clear()
    print(header(f"SOURCE: {filename}"))
    print()
    print(code_block(code))
    print()
    pause()


def run_exercise(filepath: str):
    """Run the exercise and show output."""
    clear()
    print(header("RUNNING EXERCISE"))
    print()
    info(f"File: {filepath}")
    print()
    print(line('=', 60))
    
    success_flag, output = run_python_file(filepath)
    
    print(output)
    print(line('=', 60))
    print()
    
    if success_flag:
        success("Exercise completed successfully.")
    else:
        error("Exercise encountered an error.")
    
    pause()


def edit_file(filepath: str):
    """Open file in default editor."""
    editor = os.environ.get('EDITOR', 'nano')
    print(f"Opening {filepath} in {editor}...")
    print("(Save and exit to return to this menu)")
    os.system(f"{editor} {filepath}")


def main_menu():
    """Main menu loop."""
    exercises = list_exercises()
    
    if not exercises:
        error("No exercises found in skills/ directory.")
        error("Make sure you're running from the project root.")
        sys.exit(1)
    
    while True:
        clear()
        print(ascii_header())
        print()
        
        options = [
            ("basics", "Variables, types, loops, conditionals"),
            ("core", "Functions, file handling, error handling"),
            ("advanced", "OOP, decorators, generators"),
            ("all", "Browse all exercises"),
        ]
        
        print(menu(options, "SELECT A CATEGORY"))
        print()
        
        choice = prompt(">>> ")
        
        if choice == '0':
            print()
            info("Happy coding. Come back when you're stuck.")
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


def main():
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
