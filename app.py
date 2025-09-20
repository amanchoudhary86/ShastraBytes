from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
import sqlite3, os, json, random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkeynew'

# Create a Blueprint for roadmap related routes
roadmap_bp = Blueprint('roadmap_bp', __name__)

@roadmap_bp.route('/roadmap/<roadmap_name>')
def show_roadmap(roadmap_name):
    # Construct the path to the roadmap JSON file
    # Assuming roadmap_repo is cloned at the project root
    roadmap_file_path = f'/run/media/pranav/New Volume/projects/ShastraBytes/roadmap_repo/src/data/roadmaps/{roadmap_name}/{roadmap_name}.json'
    
    roadmap_data = None
    try:
        with open(roadmap_file_path, 'r') as f:
            roadmap_data = json.load(f)
                
    except FileNotFoundError:
        print(f"Roadmap file not found: {roadmap_file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from: {roadmap_file_path}")
        
    return render_template('roadmap.html', roadmap_name=roadmap_name, roadmap_data=roadmap_data)

# Register the blueprint with the main Flask app instance
app.register_blueprint(roadmap_bp)

# --- Database Functions ---
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            python_score INTEGER DEFAULT 0,
            cpp_score INTEGER DEFAULT 0,
            total_score INTEGER NOT NULL,
            percentage REAL NOT NULL,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    db.commit()
    db.close()

# --- Helper Functions ---
def calculate_profile_completion(user_id):
    db = get_db()
    user_prefs = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
    db.close()
    if not user_prefs: return 0
    
    fields = ['role', 'target_company', 'position', 'previous_skills', 'specialization', 'skill_focus']
    filled_fields = sum(1 for field in fields if user_prefs[field])
    return int((filled_fields / len(fields)) * 100)

def get_latest_test_result(user_id):
    db = get_db()
    result = db.execute('SELECT * FROM test_results WHERE user_id = ? ORDER BY test_date DESC LIMIT 1', (user_id,)).fetchone()
    db.close()
    return result

def get_all_test_results(user_id):
    db = get_db()
    results = db.execute('SELECT * FROM test_results WHERE user_id = ? ORDER BY test_date DESC', (user_id,)).fetchall()
    db.close()
    return results

# --- Routes ---
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', user_name=session.get('user_name'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            db.commit()
            
            # Get the new user's ID and log them in
            new_user_id = cursor.lastrowid
            session['user_id'] = new_user_id
            session['user_name'] = username
            
            flash('Welcome! Please complete your profile.', 'success')
            return redirect(url_for('questionnaire'))
            
        except sqlite3.IntegrityError:
            flash('Email already registered.', 'warning')
            return redirect(url_for('signup'))
        finally:
            db.close()
            
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html', user_name=session.get('user_name'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    profile_completion = calculate_profile_completion(user_id)
    latest_test_result = get_latest_test_result(user_id)
    
    db = get_db()
    user_prefs = db.execute('SELECT specialization FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
    db.close()
    
    user_specialization_roadmap_name = None
    if user_prefs:
        user_specialization = user_prefs['specialization']
        roadmap_mapping = {
            "Machine Learning": "machine-learning",
            "Data Science": "ai-data-scientist",
            "CyberSecurity": "cyber-security",
            "Web Development": "frontend",
            "Cloud Computing": "aws"
        }
        user_specialization_roadmap_name = roadmap_mapping.get(user_specialization)

    roadmap_data = {}
    if user_specialization_roadmap_name:
        roadmap_file_path = os.path.join('roadmap_repo', 'src', 'data', 'roadmaps', user_specialization_roadmap_name, f"{user_specialization_roadmap_name}.json")
        try:
            with open(roadmap_file_path, 'r') as f:
                roadmap_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle cases where the roadmap file is missing or invalid
            pass

    return render_template('DefaultDashboard.html',
                           user_name=session['user_name'],
                           profile_completion=profile_completion,
                           latest_test_result=latest_test_result,
                           user_specialization_roadmap_name=user_specialization_roadmap_name,
                           roadmap_data=roadmap_data)

@app.route('/test_history')
def test_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    results = get_all_test_results(session['user_id'])
    return render_template('test_history.html', 
                           user_name=session['user_name'], 
                           results=results)

@app.route('/test')
def test():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        # Load Python questions
        with open('python_mcqs.json', 'r', encoding='utf-8') as f:
            python_questions = json.load(f)
            for q in python_questions:
                q['topic'] = 'python'
        
        # Load C++ questions
        with open('cpp_mcqs.json', 'r', encoding='utf-8') as f:
            cpp_questions = json.load(f)
            for q in cpp_questions:
                q['topic'] = 'cpp'

        # Select 10 random questions from each topic
        selected_python = random.sample(python_questions, 10)
        selected_cpp = random.sample(cpp_questions, 10)
        
        # Combine and shuffle
        final_questions = selected_python + selected_cpp
        random.shuffle(final_questions)
        
        # Store questions in session for submission validation
        session['test_questions'] = final_questions
        
    except FileNotFoundError as e:
        flash(f"Error: {e.filename} not found.", 'danger')
        return redirect(url_for('dashboard'))
    except (json.JSONDecodeError, ValueError) as e:
        flash("Error reading or sampling questions. Please check the JSON files.", 'danger')
        return redirect(url_for('dashboard'))

    return render_template('test.html', 
                           questions=final_questions,
                           user_name=session.get('user_name'))

@app.route('/submit_test', methods=['POST'])
def submit_test():
    if 'user_id' not in session or 'test_questions' not in session:
        flash('Your session has expired. Please start the test again.', 'warning')
        return redirect(url_for('test'))
    
    questions = session.get('test_questions', [])
    if not questions:
        flash('No questions found in your session. Please start the test again.', 'warning')
        return redirect(url_for('test'))

    python_score = 0
    cpp_score = 0
    
    for i, question in enumerate(questions):
        user_answer = request.form.get(f'q{i}')
        if user_answer and user_answer == question['answer']:
            if question['topic'] == 'python':
                python_score += 1
            elif question['topic'] == 'cpp':
                cpp_score += 1
    
    total_score = python_score + cpp_score
    total_questions = len(questions)
    percentage = (total_score / total_questions) * 100 if total_questions > 0 else 0
    
    try:
        db = get_db()
        db.execute('''
            INSERT INTO test_results (user_id, user_name, python_score, cpp_score, total_score, percentage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], session['user_name'], python_score, cpp_score, total_score, percentage))
        db.commit()
    except sqlite3.Error as e:
        flash(f"Database error: {e}", 'danger')
    finally:
        if db:
            db.close()
    
    session.pop('test_questions', None)
    
    flash('Test submitted successfully!', 'success')
    return redirect(url_for('test_result', 
                           python_score=python_score,
                           cpp_score=cpp_score,
                           total_score=total_score,
                           percentage=round(percentage, 2)))

@app.route('/test_result')
def test_result():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        python_score = request.args.get('python_score', 0, type=int)
        cpp_score = request.args.get('cpp_score', 0, type=int)
        total_score = request.args.get('total_score', 0, type=int)
        percentage = request.args.get('percentage', 0, type=float)
    except (ValueError, TypeError):
        flash('Invalid test result data.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('test_result.html',
                           user_name=session.get('user_name'),
                           python_score=python_score,
                           cpp_score=cpp_score,
                           total_score=total_score,
                           percentage=percentage)

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    
    if request.method == 'POST':
        # Data from the form
        role = request.form.get('role')
        target_company = request.form.get('company')
        position = request.form.get('position')
        previous_skills = ','.join(request.form.getlist('skills'))
        specialization = request.form.get('specialization')
        skill_focus = request.form.get('skill_focus')

        # Check if preferences already exist
        existing_prefs = db.execute('SELECT id FROM user_preferences WHERE user_id = ?', (session['user_id'],)).fetchone()

        if existing_prefs:
            # Update existing preferences
            db.execute('''
                UPDATE user_preferences
                SET role = ?, target_company = ?, position = ?, previous_skills = ?, specialization = ?, skill_focus = ?
                WHERE user_id = ?
            ''', (role, target_company, position, previous_skills, specialization, skill_focus, session['user_id']))
            flash('Profile updated successfully!', 'success')
        else:
            # Insert new preferences
            db.execute('''
                INSERT INTO user_preferences 
                (user_id, user_name, role, target_company, position, previous_skills, specialization, skill_focus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], session['user_name'], role, target_company, position, previous_skills, specialization, skill_focus))
            flash('Profile saved successfully!', 'success')
        
        db.commit()
        db.close()
        return redirect(url_for('dashboard'))

    # For GET request, fetch existing preferences
    prefs = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (session['user_id'],)).fetchone()
    db.close()
    
    # The 'previous_skills' are stored as a comma-separated string, so we split it for the template
    if prefs and prefs['previous_skills']:
        # Create a mutable copy of the row object
        prefs_dict = dict(prefs)
        prefs_dict['previous_skills'] = prefs_dict['previous_skills'].split(',')
        prefs = prefs_dict

    return render_template('questionnaire.html', user_name=session['user_name'], preferences=prefs)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    