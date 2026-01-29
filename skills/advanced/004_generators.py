#!/usr/bin/env python3
"""
Purpose: Learn generators - memory-efficient iteration.

Input: None
Output: Shows generator functions and expressions

Example:
    $ python 004_generators.py
    Counting to 5:
    1 2 3 4 5
    
    Fibonacci (first 10):
    0 1 1 2 3 5 8 13 21 34
    
    Generator expression sum: 2550

Why: Lists store everything in memory. Generators produce values on-demand. 
     For large datasets, generators can be the difference between "works" 
     and "out of memory error."
"""

# --- your code below ---

# Generator function using 'yield'
def count_to(n):
    """Count from 1 to n, one at a time."""
    i = 1
    while i <= n:
        yield i  # Pause here, return value
        i += 1


# Generator for Fibonacci sequence
def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


# Generator for reading large files line by line
def read_lines(filename):
    """Read a file line by line (memory efficient)."""
    # Note: This is a demonstration. File won't exist.
    # In real code, you'd have the file.
    pass  # Placeholder


# Using generators

print("Example 1: Count generator")
counter = count_to(5)
print("Counting to 5:")
for num in counter:
    print(num, end=" ")
print()

print()
print("Example 2: Fibonacci generator")
print("Fibonacci (first 10):")
for num in fibonacci(10):
    print(num, end=" ")
print()

# Generators are single-use
print()
print("Generators are single-use:")
counter = count_to(3)
print("First loop:", list(counter))
print("Second loop:", list(counter))  # Empty - already exhausted

# Generator expressions (like list comprehensions but lazy)
print()
print("Example 3: Generator expressions")

# List comprehension - creates entire list in memory
squares_list = [x**2 for x in range(1000)]
print(f"List size: {len(squares_list)} items")

# Generator expression - creates iterator, computes on demand
squares_gen = (x**2 for x in range(1000))
print(f"Generator object: {squares_gen}")

# Sum without storing all values
result = sum(x**2 for x in range(100))
print(f"Sum of squares 0-99: {result}")

# Finding first match without scanning everything
first_big = next((x for x in range(10000) if x**2 > 5000), None)
print(f"First number whose square > 5000: {first_big}")

# --- try this ---
# Write a generator that yields even numbers up to n
# Use it to print even numbers from 2 to 20
