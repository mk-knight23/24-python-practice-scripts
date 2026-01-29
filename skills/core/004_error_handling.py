#!/usr/bin/env python3
"""
Purpose: Handle errors gracefully. Don't let your program crash.

Input: User input that might be invalid
Output: Error messages instead of crashes

Example:
    $ python 004_error_handling.py
    Enter a number: abc
    Oops! That's not a valid number.
    Let's try again...
    
    Enter a number: 42
    Success! You entered: 42
    Half of that is: 21.0

Why: Errors happen. Good programs anticipate them. Exception handling 
     separates "what could go wrong" from "what should happen."
"""

# --- your code below ---

# Basic try/except
print("Example 1: Basic error handling")
try:
    number = int(input("Enter a number: "))
    print(f"Success! You entered: {number}")
    print(f"Half of that is: {number / 2}")
except ValueError:
    print("Oops! That's not a valid number.")

print()

# Multiple exception types
print("Example 2: Different errors, different handling")
def divide_numbers():
    try:
        a = float(input("Enter numerator: "))
        b = float(input("Enter denominator: "))
        result = a / b
        print(f"{a} / {b} = {result}")
    except ValueError:
        print("Please enter valid numbers.")
    except ZeroDivisionError:
        print("Can't divide by zero. Math doesn't work that way.")
    except Exception as e:
        print(f"Unexpected error: {e}")

divide_numbers()

print()

# Try/except/else/finally
print("Example 3: Full structure")
try:
    file = open("temp_file.txt", 'w')
    file.write("Test data")
except IOError:
    print("Couldn't write to file.")
else:
    # Runs only if no exception
    print("File written successfully.")
finally:
    # Always runs
    file.close()
    print("File closed (cleanup complete).")

# Cleanup
import os
os.remove("temp_file.txt")

# --- try this ---
# Write a function that asks for a filename and prints its contents.
# Handle the case where the file doesn't exist.
