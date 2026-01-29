#!/usr/bin/env python3
"""
Terminal utilities for the Python practice CLI.
No dependencies outside stdlib. Keep it simple.
"""

import os
import shutil
from typing import List, Tuple


# Colors? No. Just ANSI grayscale.
# These work in most terminals, degrade gracefully to plain text.
ANSI = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'white': '\033[37m',
    'gray': '\033[90m',
    'light_gray': '\033[37m',
    'bg_white': '\033[47m',
    'bg_gray': '\033[100m',
}


def term_width() -> int:
    """Get terminal width, fallback to 80."""
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


def clear():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def line(char: str = "-", width: int = None) -> str:
    """Draw a horizontal line."""
    w = width or term_width()
    return char * w


def box(text: str, width: int = None) -> str:
    """Draw text in a simple box."""
    w = width or min(60, term_width() - 4)
    lines = text.split('\n')
    result = []
    result.append('+' + '-' * (w - 2) + '+')
    for ln in lines:
        # Truncate if too long
        if len(ln) > w - 4:
            ln = ln[:w-7] + '...'
        result.append('| ' + ln.ljust(w - 4) + ' |')
    result.append('+' + '-' * (w - 2) + '+')
    return '\n'.join(result)


def header(title: str) -> str:
    """Format a section header."""
    w = term_width()
    # Simple centered header
    pad = (w - len(title) - 4) // 2
    return ' ' * pad + f"[ {title} ]"


def code_block(code: str, filename: str = None) -> str:
    """Format code for terminal display."""
    lines = code.strip().split('\n')
    result = []
    
    if filename:
        result.append(f"--- {filename} ---")
    
    for ln in lines:
        result.append(f"    {ln}")
    
    if filename:
        result.append("-" * (len(filename) + 8))
    
    return '\n'.join(result)


def menu(options: List[Tuple[str, str]], title: str = None) -> str:
    """Format a numbered menu."""
    result = []
    
    if title:
        result.append('')
        result.append(header(title))
        result.append('')
    
    for i, (key, desc) in enumerate(options, 1):
        result.append(f"  [{i}] {key:<15} {desc}")
    
    result.append('')
    result.append("  [0] Exit")
    
    return '\n'.join(result)


def prompt(text: str = ">>> ") -> str:
    """Show a prompt and get input."""
    try:
        return input(f"{text}")
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def success(msg: str):
    """Print a success message. No green checkmarks, just text."""
    print(f"  [ok] {msg}")


def error(msg: str):
    """Print an error message."""
    print(f"  [err] {msg}")


def info(msg: str):
    """Print an info message."""
    print(f"  {msg}")


def pause(msg: str = "Press Enter to continue..."):
    """Pause for user input."""
    input(f"\n  {msg}")


def ascii_header() -> str:
    """The main ASCII art header."""
    return r"""
    ____        _   _                 ____                _     
   |  _ \ _   _| |_| |__   ___ _ __  |  _ \ _   _ _______| | ___
   | |_) | | | | __| '_ \ / _ \ '__| | |_) | | | |_  /_  / |/ _ \
   |  __/| |_| | |_| | | |  __/ |    |  __/| |_| |/ / / /| |  __/
   |_|    \__, |\__|_| |_|\___|_|    |_|    \__,_/___/___|_|\___|
          |___/                                                  

    +----------------------------------------------------------+
    |  A terminal-based Python learning system. No frills.     |
    |  Just code, explained by a human who learned the hard way.|
    +----------------------------------------------------------+
"""


def list_exercises(skills_dir: str = "skills") -> List[Tuple[str, str, str]]:
    """
    List all available exercises.
    Returns: [(category, filename, full_path), ...]
    """
    exercises = []
    
    if not os.path.exists(skills_dir):
        return exercises
    
    categories = ['basics', 'core', 'advanced']
    
    for cat in categories:
        cat_path = os.path.join(skills_dir, cat)
        if not os.path.exists(cat_path):
            continue
        
        files = sorted([f for f in os.listdir(cat_path) if f.endswith('.py')])
        for f in files:
            full_path = os.path.join(cat_path, f)
            exercises.append((cat, f, full_path))
    
    return exercises


def read_exercise_info(filepath: str) -> dict:
    """
    Extract metadata from a Python exercise file.
    Looks for:
    - Purpose: in comments
    - Input/Output: examples
    - Why: explanation
    """
    info_dict = {
        'purpose': 'No description available.',
        'examples': [],
        'why': '',
        'code': ''
    }
    
    if not os.path.exists(filepath):
        return info_dict
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    info_dict['code'] = content
    lines = content.split('\n')
    
    # Look for structured comments
    in_example = False
    example_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Purpose
        if stripped.startswith('# Purpose:'):
            info_dict['purpose'] = stripped[10:].strip()
        
        # Why it matters
        elif stripped.startswith('# Why:'):
            info_dict['why'] = stripped[6:].strip()
        
        # Example block
        elif stripped.startswith('# Example') or stripped.startswith('# Input:'):
            in_example = True
            example_lines = []
        
        elif in_example:
            if stripped.startswith('#') and not stripped.startswith('# Output:'):
                example_lines.append(stripped[1:].strip())
            elif stripped.startswith('# Output:'):
                example_lines.append(f"Output: {stripped[9:].strip()}")
            elif not stripped.startswith('#'):
                in_example = False
                if example_lines:
                    info_dict['examples'].append('\n'.join(example_lines))
    
    return info_dict


def run_python_file(filepath: str) -> Tuple[bool, str]:
    """
    Run a Python file and capture output.
    Returns: (success, output)
    """
    import subprocess
    
    # Try python3 first, fall back to python
    python_cmd = 'python3' if subprocess.run(['which', 'python3'], capture_output=True).returncode == 0 else 'python'
    try:
        result = subprocess.run(
            [python_cmd, filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout
        if result.stderr:
            output += '\n[stderr]: ' + result.stderr
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Execution timed out (10s limit)"
    except Exception as e:
        return False, f"Error running file: {str(e)}"


if __name__ == '__main__':
    # Quick test
    print(ascii_header())
    print(box("Testing the box function\nWith multiple lines\nAnd one more"))
