from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import time
import subprocess
import os
from datetime import datetime, timedelta
import resource

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Hardcoded user credentials (user1/password123 & user2/password321)
USERS = {
    'user1': generate_password_hash('password123'),
    'user2': generate_password_hash('password321')
}

# Initialize database
def init_db():
    conn = sqlite3.connect('coding_contest.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT NOT NULL,
                  difficulty TEXT NOT NULL,
                  time_limit INTEGER NOT NULL)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS test_cases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question_id INTEGER NOT NULL,
                  input TEXT NOT NULL,
                  expected_output TEXT NOT NULL,
                  is_hidden BOOLEAN NOT NULL,
                  FOREIGN KEY(question_id) REFERENCES questions(id))''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT NOT NULL,
                  question_id INTEGER NOT NULL,
                  code TEXT NOT NULL,
                  execution_time REAL,
                  memory_usage REAL,
                  result TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(question_id) REFERENCES questions(id))''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('contest_dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and check_password_hash(USERS[username], password):
            session['username'] = username
            return redirect(url_for('contest_dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

# Question data structure
QUESTIONS = [
    {'id': 1, 'title': 'Reverse String', 'description': 'Write a function that reverses a string.', 'difficulty': 'Easy', 'time_limit': 10},
    {'id': 2, 'title': 'Two Sum', 'description': 'Find two numbers that add up to a target value.', 'difficulty': 'Medium', 'time_limit': 20},
    {'id': 3, 'title': 'Binary Search', 'description': 'Implement binary search algorithm.', 'difficulty': 'Easy', 'time_limit': 15},
    {'id': 4, 'title': 'Linked List Cycle', 'description': 'Detect if a linked list has a cycle.', 'difficulty': 'Medium', 'time_limit': 25},
    {'id': 5, 'title': 'Word Break', 'description': 'Determine if a string can be segmented into dictionary words.', 'difficulty': 'Hard', 'time_limit': 30}
]

@app.route('/contest')
def contest_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('contest_dashboard.html', questions=QUESTIONS)

@app.route('/question/<int:id>')
def question(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    question = next((q for q in QUESTIONS if q['id'] == id), None)
    if not question:
        abort(404)
    
    # Add example test cases
    question['example_input'] = 'Sample input'
    question['example_output'] = 'Sample output'
    
    return render_template('question.html', question=question)

@app.route('/submit/<int:question_id>', methods=['POST'])
def submit_code(question_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    code = request.form.get('code', '')
    # TODO: Implement actual code execution
    # For now, return mock response
    return jsonify({
        'success': True,
        'execution_time': 0.5,
        'memory_usage': 1024,
        'output': 'Test output'
    })

@app.route('/summary')
def summary():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Mock data for summary
    users = [
        {'username': 'user1', 'solved_count': 3, 'avg_time': 12.5},
        {'username': 'user2', 'solved_count': 2, 'avg_time': 18.3}
    ]
    
    questions = [
        {'id': 1, 'title': 'Reverse String', 'solved_count': 2, 'avg_time': 8.5},
        {'id': 2, 'title': 'Two Sum', 'solved_count': 1, 'avg_time': 15.2}
    ]
    
    submissions = [
        {'question_id': 1, 'timestamp': datetime.now(), 'result': 'success', 'execution_time': 120, 'memory_usage': 1024000},
        {'question_id': 2, 'timestamp': datetime.now(), 'result': 'error', 'execution_time': 250, 'memory_usage': 1536000}
    ]
    
    return render_template('summary.html', 
                         users=users,
                         questions=questions,
                         submissions=submissions,
                         total_questions=len(QUESTIONS),
                         user_count=2)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)