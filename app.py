from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3, os, json, random
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkeynew'

# Initialize the database
def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists("users.db"):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE users (
                       id INTEGER PRIMARY KEY, 
                       username TEXT NOT NULL, 
                       email TEXT UNIQUE NOT NULL, 
                       password TEXT NOT NULL
                    )
                ''')
        conn.commit()
        conn.close()

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                role TEXT NOT NULL,
                target_company TEXT NOT NULL,
                position TEXT NOT NULL,
                previous_skills TEXT NOT NULL,
                specialization TEXT NOT NULL,
                skill_focus TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    
    # Create test_results table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                python_score INTEGER NOT NULL,
                cpp_score INTEGER NOT NULL,
                total_score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    
    db.commit()
    db.close()

# Home page (default route)
@app.route('/')
@app.route('/home')
def home():
    user_name = session.get('user_name')
    return render_template('home.html', user_name=user_name)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            flash('Signup successful. Please login.', 'success')
        except sqlite3.IntegrityError:
            flash('Email already registered. Please login.', 'warning')
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

# About page
@app.route('/about')
def about():
    user_name = session.get('user_name')
    return render_template('about.html', user_name=user_name)

# Updated Dashboard route (Protected)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Calculate profile completion percentage
    profile_completion = calculate_profile_completion(session['user_id'])
    
    # Get latest test result
    latest_test_result = get_latest_test_result(session['user_id'])
    
    return render_template('DefaultDashboard.html', 
                         user_name=session['user_name'],
                         profile_completion=profile_completion,
                         latest_test_result=latest_test_result)

def calculate_profile_completion(user_id):
    """Calculate the profile completion percentage based on user_preferences data"""
    db = get_db()
    cursor = db.cursor()
    
    # Check if user has filled the questionnaire
    cursor.execute("""
        SELECT role, target_company, position, previous_skills, specialization, skill_focus 
        FROM user_preferences 
        WHERE user_id = ? 
        ORDER BY id DESC 
        LIMIT 1
    """, (user_id,))
    
    user_prefs = cursor.fetchone()
    db.close()
    
    if not user_prefs:
        return 0  # No questionnaire data found
    
    # Define completion criteria
    completion_fields = {
        'role': user_prefs[0],
        'target_company': user_prefs[1], 
        'position': user_prefs[2],
        'previous_skills': user_prefs[3],
        'specialization': user_prefs[4],
        'skill_focus': user_prefs[5]
    }
    
    # Calculate completion percentage
    filled_fields = 0
    total_fields = len(completion_fields)
    
    for field_name, field_value in completion_fields.items():
        if field_value and field_value.strip():  # Check if field is not empty
            filled_fields += 1
    
    # Calculate percentage
    completion_percentage = int((filled_fields / total_fields) * 100)
    
    return completion_percentage

def get_latest_test_result(user_id):
    """Get the latest test result for a user"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT python_score, cpp_score, total_score, percentage, test_date 
        FROM test_results 
        WHERE user_id = ? 
        ORDER BY test_date DESC 
        LIMIT 1
    """, (user_id,))
    
    result = cursor.fetchone()
    db.close()
    
    if result:
        return {
            'python_score': result[0],
            'cpp_score': result[1],
            'total_score': result[2],
            'percentage': result[3],
            'test_date': result[4]
        }
    return None

def get_user_skills(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT previous_skills FROM user_preferences WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    skills = cursor.fetchone()
    db.close()
    if skills:
        return [skill.strip() for skill in skills[0].split(',')]
    return []

def get_questions_by_skill_and_difficulty(skill, difficulty):
    filename = f"{skill.lower()}_mcqs.json"
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        questions = json.load(f)
    return [q for q in questions if q['difficulty'] == difficulty]

@app.route('/test')
def test():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with open('python_mcqs.json', 'r') as f:
        python_questions = json.load(f)

    with open('cpp_mcqs.json', 'r') as f:
        cpp_questions = json.load(f)

    questions = python_questions + cpp_questions
    random.shuffle(questions)
    session['questions'] = questions

    return render_template('test.html', user_name=session['user_name'], questions=questions)

# Test result page
@app.route('/test_result', methods=['POST'])
def test_result():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    score = 0
    questions = session.get('questions', [])
    total = len(questions)
    answer_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

    for i, question in enumerate(questions):
        user_answer = request.form.get(f'question_{i+1}')
        correct_answer_index = answer_map.get(question['answer'])
        if user_answer and int(user_answer) == correct_answer_index:
            score += 1
    
    # Clear questions from session
    session.pop('questions', None)

    return render_template('test_result.html',
                         score=score,
                         total=total,
                         user_name=session['user_name'])

# Questionnaire (protected)
@app.route('/questionnaire',methods=['GET','POST'])
def questionnaire():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
     
    user_name = session.get('user_name')   

    if request.method == 'POST':    
        role = request.form.get('role')
        company = request.form.get('company')
        position = request.form.get('position')
        skills = request.form.getlist('skills')
        specialization = request.form.get('specialization')
        skill_focus = request.form.get('skill_focus')

        db = get_db()
        try:
            db.execute('''
                INSERT INTO user_preferences 
                (user_id, user_name, role, target_company, position, previous_skills, specialization, skill_focus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], user_name, role, company, position, ','.join(skills), specialization, skill_focus))
            db.commit()
            flash('Preferences saved successfully!', 'success')
            return redirect(url_for('dashboard'))
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # For debugging
            flash('An error occurred while saving your preferences', 'error')
            return redirect(url_for('questionnaire'))
    
    return render_template('questionnaire.html', user_name=session['user_name'])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)