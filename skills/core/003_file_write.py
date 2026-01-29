#!/usr/bin/env python3
"""
Purpose: Write data to files. Make your data persist.

Input: None (creates its own data)
Output: Creates output.txt with formatted data

Example:
    $ python 003_file_write.py
    Writing to output.txt...
    Done! File contents:
    ========================================
    USER REPORT
    Generated: 2026-01-29
    ========================================
    User: Alice
    Score: 95
    ...

Why: Programs that can't save are toys. File I/O turns scripts into 
     tools that remember, report, and integrate with other systems.
"""

import datetime

# --- your code below ---

output_file = "output.txt"

# Sample data
data = [
    {"name": "Alice", "score": 95},
    {"name": "Bob", "score": 87},
    {"name": "Carol", "score": 92},
]

print(f"Writing to {output_file}...")

# Write mode ('w' overwrites, 'a' appends)
with open(output_file, 'w') as f:
    # Header
    f.write("=" * 40 + "\n")
    f.write("USER REPORT\n")
    f.write(f"Generated: {datetime.date.today()}\n")
    f.write("=" * 40 + "\n\n")
    
    # Data rows
    for user in data:
        f.write(f"User: {user['name']}\n")
        f.write(f"Score: {user['score']}\n")
        f.write(f"Grade: {'A' if user['score'] >= 90 else 'B'}\n")
        f.write("-" * 20 + "\n")
    
    # Footer
    avg = sum(u['score'] for u in data) / len(data)
    f.write(f"\nAverage score: {avg:.1f}\n")

# Verify by reading back
print("Done! File contents:")
print("=" * 40)
with open(output_file, 'r') as f:
    print(f.read())

# Cleanup
import os
os.remove(output_file)

# --- try this ---
# Add a timestamp to the filename so each run creates a new file
