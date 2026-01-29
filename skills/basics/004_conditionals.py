#!/usr/bin/env python3
"""
Purpose: Make decisions with if/elif/else.

Input: A number from the user
Output: Whether it's positive, negative, or zero

Example:
    $ python 004_conditionals.py
    Enter a number: -5
    That's a negative number.

Why: Life is full of decisions. So are programs. Conditionals let 
     your code take different paths based on data.
"""

# --- your code below ---

number = float(input("Enter a number: "))

if number > 0:
    print("That's a positive number.")
    print("The glass is half full.")
elif number < 0:
    print("That's a negative number.")
    print("The glass is half empty.")
else:
    print("That's zero.")
    print("The glass is refillable.")

# --- more conditions ---
# Check if it's even or odd (using modulo %)
if number % 2 == 0:
    print("Also, it's even.")
else:
    print("Also, it's odd.")

# --- try this ---
# Add a check: is the number greater than 100?
# Print "That's a big number" if it is.
