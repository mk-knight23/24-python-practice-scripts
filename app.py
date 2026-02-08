#!/usr/bin/env python3
"""
Python Practice Web Dashboard
A Flask-based web interface for the Python Practice CLI system
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import sqlite3
from datetime import datetime
import sys

# Add the project root to the path so we can import CLI modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'python-practice-secret-key'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect('python_practice.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/skills')
def get_skills():
    """Get all skills organized by category"""
    skills = {
        'basics': [],
        'core': [],
        'advanced': []
    }

    # Read skills from the skills directory
    categories = ['basics', 'core', 'advanced']
    for category in categories:
        skills_dir = os.path.join('skills', category)
        if os.path.exists(skills_dir):
            for filename in sorted(os.listdir(skills_dir)):
                if filename.endswith('.py'):
                    filepath = os.path.join(skills_dir, filename)
                    with open(filepath, 'r') as f:
                        content = f.read()

                    # Extract basic info
                    skill_info = {
                        'id': f"{category}/{filename.replace('.py', '')}",
                        'name': filename.replace('.py', '').replace('_', ' ').title(),
                        'category': category,
                        'content': content
                    }
                    skills[category].append(skill_info)

    return jsonify(skills)

@app.route('/api/progress/<username>')
def get_progress(username):
    """Get user progress data"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get completion data
    cursor.execute('SELECT exercise_id, completed_at, score FROM completions WHERE username = ?', (username,))
    completions = cursor.fetchall()

    progress = {
        'username': username,
        'total_exercises': 15,
        'completed_exercises': len(completions),
        'completions': []
    }

    for completion in completions:
        progress['completions'].append({
            'exercise_id': completion['exercise_id'],
            'completed_at': completion['completed_at'],
            'score': completion['score']
        })

    conn.close()
    return jsonify(progress)

@app.route('/api/complete', methods=['POST'])
def complete_exercise():
    """Mark an exercise as completed"""
    data = request.json
    username = data.get('username')
    exercise_id = data.get('exercise_id')
    score = data.get('score', 0)

    if not username or not exercise_id:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO completions (username, exercise_id, score, completed_at)
            VALUES (?, ?, ?, ?)
        ''', (username, exercise_id, score, datetime.now()))
        conn.commit()

        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Exercise already completed'}), 400
    finally:
        conn.close()

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/dashboard.html')
def dashboard():
    """Redirect to the main dashboard"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)