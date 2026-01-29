#!/usr/bin/env python3
"""
Purpose: Work with dictionaries - key-value pairs for structured data.

Input: None
Output: Dictionary operations demonstration

Example:
    $ python 005_dictionaries.py
    User profile:
      name: Alice
      age: 25
      city: Boston
    
    Alice is from Boston
    Keys: dict_keys(['name', 'age', 'city'])

Why: Lists are for ordered collections. Dictionaries are for labeled 
     data. Most real-world data has labels: name, value, timestamp, etc.
"""

# --- your code below ---

# Creating a dictionary
user = {
    "name": "Alice",
    "age": 25,
    "city": "Boston"
}

print("User profile:")
for key, value in user.items():
    print(f"  {key}: {value}")

print()

# Accessing values
print(f"{user['name']} is from {user['city']}")

# Safe access with .get()
print(f"Email: {user.get('email', 'Not provided')}")

# Adding/updating
user["email"] = "alice@example.com"
user["age"] = 26  # Birthday!

print("\nUpdated profile:")
print(user)

# Checking keys
if "name" in user:
    print(f"\nFound user: {user['name']}")

# Dictionary methods
print(f"\nKeys: {user.keys()}")
print(f"Values: {user.values()}")
print(f"Items: {list(user.items())[:2]}...")  # First 2 items

# Nested dictionaries
users = {
    "alice": {"age": 26, "city": "Boston"},
    "bob": {"age": 30, "city": "NYC"},
}
print(f"\nBob lives in: {users['bob']['city']}")

# Dictionary comprehension
squares = {x: x**2 for x in range(1, 6)}
print(f"\nSquares: {squares}")

# --- try this ---
# Create a dictionary of 3 favorite books with title and author
# Print them formatted nicely
