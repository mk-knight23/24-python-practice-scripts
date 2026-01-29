#!/usr/bin/env python3
"""
Purpose: Read data from files.

Input: A text file (we'll create one)
Output: Contents of the file

Example:
    $ python 002_file_read.py
    Creating sample file...
    
    Reading entire file:
    Line 1: Hello from the file!
    Line 2: This is line two.
    Line 3: Files are just persistent storage.
    
    Reading line by line:
    1: Hello from the file!
    2: This is line two.
    3: Files are just persistent storage.

Why: RAM forgets when power goes off. Files don't. Reading files 
     connects your programs to the real world of data persistence.
"""

# --- your code below ---

filename = "sample_data.txt"

# First, let's create a file to read from
print("Creating sample file...")
with open(filename, 'w') as f:
    f.write("Hello from the file!\n")
    f.write("This is line two.\n")
    f.write("Files are just persistent storage.\n")

# Method 1: Read entire file at once
print("\nReading entire file:")
with open(filename, 'r') as f:
    content = f.read()
    print(content)

# Method 2: Read line by line
print("Reading line by line:")
with open(filename, 'r') as f:
    for num, line in enumerate(f, 1):
        print(f"{num}: {line.strip()}")

# Method 3: Read into a list
print("Reading into list:")
with open(filename, 'r') as f:
    lines = f.readlines()
    print(f"File has {len(lines)} lines")
    print("Second line:", lines[1].strip())

# Cleanup
import os
os.remove(filename)
print(f"\nCleaned up {filename}")

# --- try this ---
# Modify to count how many words are in the file
