#!/usr/bin/env python3
"""
Purpose: Introduction to Object-Oriented Programming with classes.

Input: None
Output: Demonstrates class definition and object creation

Example:
    $ python 001_classes.py
    Creating books...
    
    '1984' by George Orwell (1949)
    Available: Yes
    
    '1984' has been borrowed.
    Available: No

Why: Functions organize code. Classes organize data AND code together. 
     When your data has behavior (a book can be borrowed), use classes.
"""

# --- your code below ---

class Book:
    """A simple Book class."""
    
    # Class attribute (shared by all instances)
    library_name = "City Library"
    
    def __init__(self, title, author, year):
        """Initialize a new Book. Called when you create an instance."""
        self.title = title
        self.author = author
        self.year = year
        self.is_borrowed = False
    
    def borrow(self):
        """Mark the book as borrowed."""
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False
    
    def return_book(self):
        """Mark the book as returned."""
        self.is_borrowed = False
    
    def info(self):
        """Return book information as a string."""
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"'{self.title}' by {self.author} ({self.year}) - {status}"
    
    def __str__(self):
        """String representation of the book."""
        return f"'{self.title}' by {self.author}"


# Using the class
print("Creating books...")
print()

book1 = Book("1984", "George Orwell", 1949)
book2 = Book("To Kill a Mockingbird", "Harper Lee", 1960)

print(book1.info())
print(f"Available: {'No' if book1.is_borrowed else 'Yes'}")
print()

# Borrow the book
print(f"{book1} has been borrowed.")
book1.borrow()
print(f"Available: {'No' if book1.is_borrowed else 'Yes'}")
print()

# Check library name (class attribute)
print(f"Library: {Book.library_name}")
print()

# Print all books
print("Catalog:")
for book in [book1, book2]:
    print(f"  - {book}")

# --- try this ---
# Add a method 'age()' that returns how old the book is
# Hint: import datetime and use datetime.date.today().year
