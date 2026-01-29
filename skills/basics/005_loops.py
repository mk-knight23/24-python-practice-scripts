#!/usr/bin/env python3
"""
Purpose: Repeat code with for and while loops.

Input: None
Output: Counting, iterating over lists

Example:
    $ python 005_loops.py
    Counting to 5:
    1 2 3 4 5
    
    Fruits in my list:
    - apple
    - banana

Why: Computers excel at repetition. Loops let you process thousands 
     of items without writing thousands of lines of code.
"""

# --- your code below ---

# FOR loop - when you know how many times
print("Counting to 5:")
for i in range(1, 6):
    print(i, end=" ")
print()  # newline
print()

# FOR loop - iterating over a list
fruits = ["apple", "banana", "cherry", "date"]
print("Fruits in my list:")
for fruit in fruits:
    print(f"- {fruit}")
print()

# WHILE loop - when you don't know how many times
print("Countdown:")
count = 3
while count > 0:
    print(count, "...")
    count = count - 1
print("Blast off!")

# --- common pattern ---
# Loop with index
print()
print("With index:")
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

# --- try this ---
# Print all even numbers from 2 to 20 using a loop
