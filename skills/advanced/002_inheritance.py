#!/usr/bin/env python3
"""
Purpose: Learn inheritance - classes that build on other classes.

Input: None
Output: Shows base class and derived classes in action

Example:
    $ python 002_inheritance.py
    Creating animals...
    
    Buddy says: Woof!
    Buddy can run.
    
    Whiskers says: Meow!
    Whiskers can climb.

Why: Inheritance lets you write common code once, then specialize. 
     "A dog IS AN animal" - it has everything an animal has, plus more.
"""

# --- your code below ---

class Animal:
    """Base class for all animals."""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        """Default sound. Override in subclasses."""
        return "Some sound"
    
    def info(self):
        return f"{self.name}, age {self.age}"
    
    def __str__(self):
        return f"{self.name} says: {self.speak()}"


class Dog(Animal):
    """A dog is an animal that barks."""
    
    def __init__(self, name, age, breed):
        # Call parent class constructor
        super().__init__(name, age)
        self.breed = breed
    
    def speak(self):
        return "Woof!"
    
    def fetch(self):
        return f"{self.name} is fetching the ball."


class Cat(Animal):
    """A cat is an animal that meows."""
    
    def speak(self):
        return "Meow!"
    
    def climb(self):
        return f"{self.name} is climbing the curtain."


# Using the classes
print("Creating animals...")
print()

dog = Dog("Buddy", 3, "Golden Retriever")
cat = Cat("Whiskers", 2)

print(dog)
print(dog.fetch())
print()

print(cat)
print(cat.climb())
print()

# Polymorphism - treat different objects the same way
print("Animal chorus:")
animals = [dog, cat, Animal("Generic", 1)]
for animal in animals:
    print(f"  {animal.name}: {animal.speak()}")

# isinstance checks
print()
print(f"Is dog an Animal? {isinstance(dog, Animal)}")
print(f"Is dog a Cat? {isinstance(dog, Cat)}")

# --- try this ---
# Create a Bird class that inherits from Animal
# Add a method 'fly()' and override 'speak()' to return "Tweet!"
