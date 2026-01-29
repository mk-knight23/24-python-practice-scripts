#!/usr/bin/env python3
"""
Purpose: Learn to write reusable code with functions.

Input: None
Output: Demonstrates function definition and calling

Example:
    $ python 001_functions.py
    Hello, Alice!
    5 + 3 = 8
    Area of circle (r=5): 78.54

Why: Functions are the building blocks of clean code. They let you 
     write once, use many times, and organize complexity into manageable pieces.
"""

import math

# --- your code below ---

# Simple function, no parameters
def say_hello():
    print("Hello, world!")

# Function with parameters
def greet(name):
    print(f"Hello, {name}!")

# Function with return value
def add(a, b):
    return a + b

# Function with default parameter
def greet_formal(name, title="Mr./Ms."):
    print(f"Hello, {title} {name}.")

# Function with multiple returns (actually returns a tuple)
def circle_stats(radius):
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference

# --- using the functions ---

say_hello()
greet("Alice")

result = add(5, 3)
print(f"5 + 3 = {result}")

greet_formal("Smith")
greet_formal("Jones", "Dr.")

area, circ = circle_stats(5)
print(f"Area of circle (r=5): {area:.2f}")

# --- try this ---
# Write a function that converts Celsius to Fahrenheit
# Formula: (C × 9/5) + 32 = F
