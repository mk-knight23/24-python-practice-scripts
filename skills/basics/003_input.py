#!/usr/bin/env python3
"""
Purpose: Get input from the user. Make your programs interactive.

Input: User types their name and age
Output: Personalized greeting

Example:
    $ python 003_input.py
    What is your name? Alice
    How old are you? 25
    Hello Alice, you will be 26 next year.

Why: Programs without input are just scripts. Programs with input 
     become tools. This is where you start making things useful.
"""

# --- your code below ---

# Get user input (input() always returns a string)
name = input("What is your name? ")

# Convert string to integer for math
age_str = input("How old are you? ")
age = int(age_str)

# Do something with the data
next_year = age + 1

# Output the result
print("Hello " + name + ", you will be " + str(next_year) + " next year.")

# Alternative: f-strings (cleaner)
print(f"Hello {name}, you will be {next_year} next year.")

# --- watch out for ---
# If the user types "twenty-five" instead of "25", int() will crash.
# We'll learn to handle that in the error handling section.
