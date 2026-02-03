#!/usr/bin/env python3
"""
Quiz system for testing Python knowledge.

Generates quizzes from exercise concepts and tracks results.
"""

from __future__ import annotations

import random
import sys
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    init_database, get_active_user, save_quiz_result,
    get_quiz_history, award_achievement, get_user_progress
)
from utils import clear, header, prompt, info, success, error, pause, line


# Quiz question bank
QUESTIONS = {
    'basics': [
        {
            'question': 'What is the correct way to create a variable in Python?',
            'options': [
                'A. var x = 5',
                'B. x = 5',
                'C. int x = 5',
                'D. let x = 5'
            ],
            'correct': 1,  # 0-indexed
            'explanation': 'Python uses dynamic typing. Just write the variable name and assign a value.'
        },
        {
            'question': 'Which of these is a valid Python comment?',
            'options': [
                'A. // This is a comment',
                'B. # This is a comment',
                'C. /* This is a comment */',
                'D. <!-- This is a comment -->'
            ],
            'correct': 1,
            'explanation': 'Python uses # for single-line comments.'
        },
        {
            'question': 'What does the len() function do?',
            'options': [
                'A. Calculates the length of an object',
                'B. Creates a new list',
                'C. Converts to lowercase',
                'D. Loops through items'
            ],
            'correct': 0,
            'explanation': 'len() returns the length (number of items) of strings, lists, tuples, etc.'
        },
        {
            'question': 'How do you write an if statement in Python?',
            'options': [
                'A. if x == 5:',
                'B. if (x == 5) {',
                'C. if x == 5 then',
                'D. if [x == 5]'
            ],
            'correct': 0,
            'explanation': 'Python uses colons and indentation instead of braces.'
        },
        {
            'question': 'What is the output of: print(3 ** 2)?',
            'options': [
                'A. 6',
                'B. 5',
                'C. 9',
                'D. 32'
            ],
            'correct': 2,
            'explanation': '** is the exponentiation operator in Python, so 3 ** 2 = 9.'
        },
        {
            'question': 'Which loop is used to iterate over a sequence?',
            'options': [
                'A. for loop',
                'B. while loop',
                'C. do-while loop',
                'D. repeat-until loop'
            ],
            'correct': 0,
            'explanation': 'The for loop in Python iterates over sequences like lists, strings, tuples.'
        },
        {
            'question': 'How do you create a list in Python?',
            'options': [
                'A. list = (1, 2, 3)',
                'B. list = [1, 2, 3]',
                'C. list = {1, 2, 3}',
                'D. list = <1, 2, 3>'
            ],
            'correct': 1,
            'explanation': 'Python uses square brackets [] for lists.'
        },
        {
            'question': 'What is list slicing?',
            'options': [
                'A. Creating new lists from existing lists',
                'B. Splitting strings into characters',
                'C. Sorting a list',
                'D. Removing items from a list'
            ],
            'correct': 0,
            'explanation': 'Slicing creates a new list by extracting a portion: list[1:4]'
        }
    ],
    'core': [
        {
            'question': 'How do you define a function in Python?',
            'options': [
                'A. function myFunc():',
                'B. def myFunc():',
                'C. func myFunc():',
                'D. define myFunc():'
            ],
            'correct': 1,
            'explanation': 'Python uses the def keyword to define functions.'
        },
        {
            'question': 'What is a default argument value?',
            'options': [
                'A. A value that cannot be changed',
                'B. A value used if no argument is provided',
                'C. The first argument in a function',
                'D. A global variable'
            ],
            'correct': 1,
            'explanation': 'Default arguments are used when the caller doesn\'t provide a value.'
        },
        {
            'question': 'How do you open a file for reading in Python?',
            'options': [
                'A. file = open("file.txt", "r")',
                'B. file = read("file.txt")',
                'C. file = fopen("file.txt")',
                'D. file = load("file.txt")'
            ],
            'correct': 0,
            'explanation': 'The open() function opens files, with "r" for read mode.'
        },
        {
            'question': 'What is the purpose of a context manager (with statement)?',
            'options': [
                'A. To make code run faster',
                'B. To automatically close files',
                'C. To create variables',
                'D. To catch errors'
            ],
            'correct': 1,
            'explanation': 'Context managers automatically handle resource cleanup like closing files.'
        },
        {
            'question': 'How do you handle exceptions in Python?',
            'options': [
                'A. try/catch',
                'B. try/except',
                'C. try/error',
                'D. do/catch'
            ],
            'correct': 1,
            'explanation': 'Python uses try/except blocks for exception handling.'
        },
        {
            'question': 'What is the purpose of else in a try/except block?',
            'options': [
                'A. Runs if an exception occurs',
                'B. Runs if no exception occurs',
                'C. Runs regardless of exceptions',
                'D. Catches specific exceptions'
            ],
            'correct': 1,
            'explanation': 'The else block runs only if no exceptions were raised in the try block.'
        },
        {
            'question': 'What is a dictionary in Python?',
            'options': [
                'A. A book of Python terms',
                'B. A collection of key-value pairs',
                'C. A sorted list',
                'D. A text file'
            ],
            'correct': 1,
            'explanation': 'Dictionaries store data in key-value pairs: {"key": "value"}'
        },
        {
            'question': 'How do you check if a key exists in a dictionary?',
            'options': [
                'A. key in dict',
                'B. dict.has(key)',
                'C. dict.contains(key)',
                'D. exists(dict, key)'
            ],
            'correct': 0,
            'explanation': 'Use the "in" operator to check if a key exists in a dictionary.'
        }
    ],
    'advanced': [
        {
            'question': 'How do you define a class in Python?',
            'options': [
                'A. class MyClass:',
                'B. def MyClass:',
                'C. object MyClass:',
                'D. struct MyClass:'
            ],
            'correct': 0,
            'explanation': 'Python uses the "class" keyword to define classes.'
        },
        {
            'question': 'What is the __init__ method?',
            'options': [
                'A. A class destructor',
                'B. A constructor method',
                'C. A static method',
                'D. A class variable'
            ],
            'correct': 1,
            'explanation': '__init__ is the constructor that initializes new object instances.'
        },
        {
            'question': 'What is inheritance in Python?',
            'options': [
                'A. Copying code from one class to another',
                'B. Creating a new class from an existing class',
                'C. Importing modules',
                'D. Using global variables'
            ],
            'correct': 1,
            'explanation': 'Inheritance allows a class to acquire attributes and methods from another class.'
        },
        {
            'question': 'What is a decorator in Python?',
            'options': [
                'A. A design pattern for colors',
                'B. A function that modifies another function',
                'C. A class method',
                'D. A type of variable'
            ],
            'correct': 1,
            'explanation': 'Decorators modify or enhance functions without changing their code directly.'
        },
        {
            'question': 'What symbol is used for decorators?',
            'options': [
                'A. @',
                'B. #',
                'C. *',
                'D. &'
            ],
            'correct': 0,
            'explanation': 'The @ symbol is placed above a function to apply a decorator.'
        },
        {
            'question': 'What is a generator in Python?',
            'options': [
                'A. A function that creates classes',
                'B. A function that yields values one at a time',
                'C. A random number generator',
                'D. A list comprehension'
            ],
            'correct': 1,
            'explanation': 'Generators use "yield" to produce values lazily, one at a time.'
        },
        {
            'question': 'What is the benefit of using generators?',
            'options': [
                'A. They run faster',
                'B. They use less memory',
                'C. They are easier to write',
                'D. They support multi-threading'
            ],
            'correct': 1,
            'explanation': 'Generators are memory-efficient because they yield one item at a time.'
        },
        {
            'question': 'What does the yield keyword do?',
            'options': [
                'A. Returns a value and ends the function',
                'B. Pauses the function and returns a value',
                'C. Creates a new variable',
                'D. Imports a module'
            ],
            'correct': 1,
            'explanation': 'yield pauses the function and returns a value, resuming on the next call.'
        }
    ]
}


def get_questions(category: str, count: int = 5) -> List[Dict[str, Any]]:
    """Get random questions for a quiz.

    Args:
        category: Category (basics, core, advanced, mixed)
        count: Number of questions

    Returns:
        List of question dicts
    """
    if category == 'mixed':
        # Get questions from all categories
        all_questions = []
        for cat in ['basics', 'core', 'advanced']:
            all_questions.extend(QUESTIONS.get(cat, []))
        questions = random.sample(all_questions, min(count, len(all_questions)))
    else:
        available = QUESTIONS.get(category, [])
        questions = random.sample(available, min(count, len(available)))

    # Add indices to options
    for q in questions:
        for i, opt in enumerate(q['options']):
            q['options'][i] = f"{chr(65 + i)}. {opt[3:]}"  # A, B, C, D

    return questions


def run_quiz(category: str = 'mixed', count: int = 5) -> Dict[str, Any]:
    """Run an interactive quiz.

    Args:
        category: Quiz category
        count: Number of questions

    Returns:
        Quiz results dict
    """
    # Initialize database
    init_database()
    user = get_active_user()
    if not user:
        error("No active user. Please create a user profile first.")
        return {}

    questions = get_questions(category, count)
    if not questions:
        error("No questions available for this category.")
        return {}

    clear()
    print(header("QUIZ MODE"))
    print()
    info(f"Category: {category.upper()}")
    info(f"Questions: {len(questions)}")
    info(f"Each question has 4 options. Enter A, B, C, or D.")
    print()
    pause()

    answers = []
    correct_count = 0
    start_time = datetime.now()

    for i, question in enumerate(questions, 1):
        clear()
        print(header(f"QUESTION {i}/{len(questions)}"))
        print()
        print(f"  {question['question']}")
        print()

        for opt in question['options']:
            info(opt)

        print()
        choice = prompt("Your answer (A-D): ").strip().upper()

        # Convert choice to index
        choice_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        choice_idx = choice_map.get(choice, -1)

        is_correct = choice_idx == question['correct']
        if is_correct:
            correct_count += 1

        answers.append({
            'question': question['question'],
            'your_answer': choice,
            'correct_answer': chr(65 + question['correct']),
            'is_correct': is_correct,
            'explanation': question['explanation']
        })

    end_time = datetime.now()
    time_taken = int((end_time - start_time).total_seconds())

    # Show results
    clear()
    print(header("QUIZ RESULTS"))
    print()

    score = (correct_count / len(questions)) * 100
    info(f"Score: {correct_count}/{len(questions)} ({score:.0f}%)")
    info(f"Time: {time_taken // 60}m {time_taken % 60}s")
    print()

    if score >= 80:
        success("Excellent work! 🎉")
    elif score >= 60:
        success("Good job! Keep practicing.")
    else:
        info("Keep learning and try again!")

    print()
    pause()

    # Show review
    clear()
    print(header("REVIEW"))
    print()

    for i, answer in enumerate(answers, 1):
        status = "✓" if answer['is_correct'] else "✗"
        print(f"  {i}. {status} {answer['question'][:50]}...")
        if not answer['is_correct']:
            info(f"     Your answer: {answer['your_answer']}")
            info(f"     Correct: {answer['correct_answer']}")
            info(f"     {answer['explanation']}")
        print()

    pause()

    # Save results
    quiz_id = save_quiz_result(
        user['id'],
        category,
        len(questions),
        correct_count,
        time_taken,
        answers
    )

    return {
        'quiz_id': quiz_id,
        'score': score,
        'correct_count': correct_count,
        'total_questions': len(questions),
        'time_taken': time_taken
    }


def show_quiz_history(limit: int = 10) -> None:
    """Display quiz history.

    Args:
        limit: Number of recent quizzes to show
    """
    init_database()
    user = get_active_user()
    if not user:
        error("No active user found.")
        return

    clear()
    print(header("QUIZ HISTORY"))
    print()

    history = get_quiz_history(user['id'], limit)

    if not history:
        info("No quizzes taken yet.")
        print()
        pause()
        return

    for quiz in history:
        print(f"  Date: {quiz['taken_at'][:10]}")
        print(f"  Type: {quiz['quiz_type']}")
        print(f"  Score: {quiz['correct_count']}/{quiz['questions_count']} ({quiz['score']:.0f}%)")
        print(f"  Time: {quiz['time_taken_seconds'] // 60}m {quiz['time_taken_seconds'] % 60}s")
        print(line('-', 60))
        print()

    pause()


def quiz_menu() -> None:
    """Quiz selection menu."""
    while True:
        clear()
        print(header("QUIZ MODE"))
        print()

        options = [
            ("basics", "Variables, types, loops, conditionals (5 questions)"),
            ("core", "Functions, files, error handling (5 questions)"),
            ("advanced", "OOP, decorators, generators (5 questions)"),
            ("mixed", "Mixed difficulty (10 questions)"),
            ("history", "View quiz history"),
        ]

        for i, (key, desc) in enumerate(options, 1):
            print(f"  [{i}] {key:<12} {desc}")

        print()
        print("  [0] Back")
        print()

        choice = prompt("Select quiz type: ")

        if choice == '0':
            break
        elif choice == '1':
            run_quiz('basics', 5)
        elif choice == '2':
            run_quiz('core', 5)
        elif choice == '3':
            run_quiz('advanced', 5)
        elif choice == '4':
            run_quiz('mixed', 10)
        elif choice == '5':
            show_quiz_history()


if __name__ == '__main__':
    quiz_menu()
