#!/usr/bin/env python3
"""
Purpose: Learn decorators - functions that modify functions.

Input: None
Output: Shows timing and logging decorators

Example:
    $ python 003_decorators.py
    Calling: slow_function
    Args: (), KWargs: {}
    slow_function took 1.002 seconds
    Done!
    
    [LOG] Entering: greet
    Hello, Alice!
    [LOG] Exiting: greet

Why: Decorators add behavior to functions without changing their code. 
     Timing, logging, caching, authentication - all reusable via decorators.
"""

import time
import functools

# --- your code below ---

# A simple decorator that logs function calls
def logger(func):
    """Prints before and after calling a function."""
    @functools.wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        print(f"[LOG] Entering: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Exiting: {func.__name__}")
        return result
    return wrapper


# A decorator that times function execution
def timer(func):
    """Times how long a function takes to run."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.3f} seconds")
        return result
    return wrapper


# A decorator with parameters
def repeat(times):
    """Repeat the function call multiple times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# Using decorators

@timer
def slow_function():
    """A deliberately slow function."""
    time.sleep(0.5)
    print("Done!")


@logger
def greet(name):
    print(f"Hello, {name}!")


@repeat(3)
def count():
    print("Counting...")


# Run the decorated functions
print("Example 1: Timing decorator")
slow_function()

print()
print("Example 2: Logging decorator")
greet("Alice")

print()
print("Example 3: Parameterized decorator")
count()

# --- manual decoration (without @ syntax) ---
print()
print("Manual decoration:")
def plain_function():
    print("I am plain.")

# Apply decorator manually
decorated = timer(plain_function)
decorated()

# --- try this ---
# Write a decorator 'cache' that stores function results
# and returns the cached value on subsequent calls with the same arguments
# Hint: use a dictionary to store results
