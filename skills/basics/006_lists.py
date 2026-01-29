#!/usr/bin/env python3
"""
Purpose: Work with lists - ordered collections of items.

Input: None
Output: List operations demonstration

Example:
    $ python 006_lists.py
    Original: ['red', 'green', 'blue']
    After append: ['red', 'green', 'blue', 'yellow']
    First item: red
    Last item: yellow

Why: Most data comes in sets, not singles. Lists are Python's 
     workhorse for handling collections. You'll use them constantly.
"""

# --- your code below ---

# Creating a list
colors = ["red", "green", "blue"]
print("Original:", colors)

# Adding items
colors.append("yellow")
print("After append:", colors)

# Inserting at position
colors.insert(1, "orange")
print("After insert:", colors)

# Accessing by index
print("First item:", colors[0])
print("Last item:", colors[-1])

# Slicing (getting a subset)
print("Middle two:", colors[1:3])

# Removing items
colors.remove("green")
print("After remove:", colors)

# Checking membership
if "blue" in colors:
    print("Blue is still in the list.")

# List length
print(f"The list has {len(colors)} items.")

# Sorting
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print("Sorted numbers:", numbers)

# --- try this ---
# Create a list of your favorite foods and print them numbered
