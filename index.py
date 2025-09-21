import json
import os
import random
import sqlite3

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from config import config
from enhanced_roadmap_generator import enhanced_roadmap_generator
from roadmap_generator import roadmap_generator

# Import PostgreSQL adapter for Vercel
try:
    import psycopg
    from psycopg.rows import dict_row
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# --- Database Functions ---
def get_db():
    """Get database connection with proper error handling"""
    try:
        if app.config.get('USE_SQLITE', True):
            # SQLite for local development
            conn = sqlite3.connect(app.config['DATABASE_PATH'])
            conn.row_factory = sqlite3.Row
            return conn
        else:
            # PostgreSQL for Vercel
            if not POSTGRES_AVAILABLE:
                print("PostgreSQL adapter not available")
                return None
            
            conn = psycopg.connect(
                app.config['DATABASE_URL'],
                row_factory=dict_row
            )
            return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database with proper error handling for both SQLite and PostgreSQL"""
    try:
        if app.config.get('USE_SQLITE', True):
            # SQLite initialization for local development
            conn = sqlite3.connect(app.config['DATABASE_PATH'])
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY, 
                   username TEXT NOT NULL, 
                   email TEXT UNIQUE NOT NULL, 
                   password TEXT NOT NULL
                )
            ''')
            
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
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_roadmaps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    roadmap_data TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("SQLite database initialized successfully")
            
        else:
            # PostgreSQL initialization for Vercel
            if not POSTGRES_AVAILABLE or not app.config.get('DATABASE_URL'):
                print("PostgreSQL not available or DATABASE_URL not set")
                return
                
            conn = psycopg.connect(app.config['DATABASE_URL'])
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                   id SERIAL PRIMARY KEY, 
                   username VARCHAR(255) NOT NULL, 
                   email VARCHAR(255) UNIQUE NOT NULL, 
                   password VARCHAR(255) NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    user_name VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL,
                    target_company VARCHAR(255) NOT NULL,
                    position VARCHAR(255) NOT NULL,
                    previous_skills TEXT NOT NULL,
                    specialization VARCHAR(255) NOT NULL,
                    skill_focus VARCHAR(255) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    user_name VARCHAR(255) NOT NULL,
                    python_score INTEGER DEFAULT 0,
                    cpp_score INTEGER DEFAULT 0,
                    total_score INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_roadmaps (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    roadmap_data TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("PostgreSQL database initialized successfully")
        
    except Exception as e:
        print(f"Database initialization error: {e}")

# --- Helper Functions ---
def calculate_profile_completion(user_id):
    """Calculate user profile completion percentage"""
    db = get_db()
    if not db:
        return 0
        
    try:
        user_prefs = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
        if not user_prefs:
            return 0
        
        fields = ['role', 'target_company', 'position', 'previous_skills', 'specialization', 'skill_focus']
        filled_fields = sum(1 for field in fields if user_prefs[field])
        return int((filled_fields / len(fields)) * 100)
    except sqlite3.Error as e:
        print(f"Error calculating profile completion: {e}")
        return 0
    finally:
        db.close()

def get_latest_test_result(user_id):
    """Get user's latest test result"""
    db = get_db()
    if not db:
        return None
        
    try:
        result = db.execute('SELECT * FROM test_results WHERE user_id = ? ORDER BY test_date DESC LIMIT 1', (user_id,)).fetchone()
        return result
    except sqlite3.Error as e:
        print(f"Error getting latest test result: {e}")
        return None
    finally:
        db.close()

def get_all_test_results(user_id):
    """Get all test results for a user"""
    db = get_db()
    if not db:
        return []
        
    try:
        results = db.execute('SELECT * FROM test_results WHERE user_id = ? ORDER BY test_date DESC', (user_id,)).fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Error getting test results: {e}")
        return []
    finally:
        db.close()

def get_user_roadmap(user_id):
    """Get user's personalized roadmap"""
    db = get_db()
    if not db:
        return None
        
    try:
        result = db.execute('SELECT roadmap_data FROM user_roadmaps WHERE user_id = ? ORDER BY updated_date DESC LIMIT 1', (user_id,)).fetchone()
        if result:
            return json.loads(result['roadmap_data'])
        return None
    except (sqlite3.Error, json.JSONDecodeError) as e:
        print(f"Error getting user roadmap: {e}")
        return None
    finally:
        db.close()

def save_user_roadmap(user_id, roadmap_data):
    """Save or update user's roadmap"""
    db = get_db()
    if not db:
        return False
        
    try:
        # Check if roadmap exists
        existing = db.execute('SELECT id FROM user_roadmaps WHERE user_id = ?', (user_id,)).fetchone()
        
        if existing:
            # Update existing roadmap
            db.execute('''
                UPDATE user_roadmaps 
                SET roadmap_data = ?, updated_date = CURRENT_TIMESTAMP 
                WHERE user_id = ?
            ''', (json.dumps(roadmap_data), user_id))
        else:
            # Create new roadmap
            db.execute('''
                INSERT INTO user_roadmaps (user_id, roadmap_data) 
                VALUES (?, ?)
            ''', (user_id, json.dumps(roadmap_data)))
        
        db.commit()
        return True
    except (sqlite3.Error, json.JSONEncodeError) as e:
        print(f"Error saving user roadmap: {e}")
        return False
    finally:
        db.close()

def generate_user_roadmap(user_id):
    """Generate a new roadmap for user based on their preferences"""
    db = get_db()
    if not db:
        return None
        
    try:
        # Get user preferences
        prefs = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
        if not prefs:
            return None
        
        # Convert preferences to dict
        preferences = dict(prefs)
        
        # Generate enhanced roadmap
        roadmap = enhanced_roadmap_generator.generate_enhanced_roadmap(preferences)
        
        # Save roadmap
        if save_user_roadmap(user_id, roadmap):
            return roadmap
        return None
        
    except sqlite3.Error as e:
        print(f"Error generating user roadmap: {e}")
        return None
    finally:
        db.close()

def validate_form_data(form_data, required_fields):
    """Validate form data"""
    errors = []
    for field in required_fields:
        if not form_data.get(field) or not form_data.get(field).strip():
            errors.append(f"{field.replace('_', ' ').title()} is required")
    return errors

# --- Routes ---
@app.route('/')
@app.route('/home')
def home():
    """Home page route"""
    return render_template('home.html', user_name=session.get('user_name'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route with improved error handling"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Basic validation
        if not email or not password:
            flash('Please fill in all fields', 'danger')
            return render_template('login.html')
        
        db = get_db()
        if not db:
            flash('Database connection error. Please try again.', 'danger')
            return render_template('login.html')
            
        try:
            user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials', 'danger')
        except sqlite3.Error as e:
            print(f"Login database error: {e}")
            flash('Database error. Please try again.', 'danger')
        finally:
            db.close()
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup route with improved validation"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        errors = validate_form_data(request.form, ['username', 'email', 'password'])
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('signup.html')
        
        db = get_db()
        if not db:
            flash('Database connection error. Please try again.', 'danger')
            return render_template('signup.html')
            
        try:
            hashed_password = generate_password_hash(password)
            cursor = db.cursor()
            
            if app.config.get('USE_SQLITE', True):
                # SQLite syntax
                cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                             (username, email, hashed_password))
                new_user_id = cursor.lastrowid
            else:
                # PostgreSQL syntax
                cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id', 
                             (username, email, hashed_password))
                new_user_id = cursor.fetchone()['id']
                
            db.commit()
            
            # Get the new user's ID and log them in
            session['user_id'] = new_user_id
            session['user_name'] = username
            
            flash('Welcome! Please complete your profile.', 'success')
            return redirect(url_for('questionnaire'))
            
        except Exception as e:
            # Handle both SQLite IntegrityError and PostgreSQL UniqueViolation
            if 'UNIQUE constraint failed' in str(e) or 'duplicate key' in str(e):
                flash('Email already registered.', 'warning')
            else:
                print(f"Signup database error: {e}")
                flash('Database error. Please try again.', 'danger')
        finally:
            db.close()
            
    return render_template('signup.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html', user_name=session.get('user_name'))

@app.route('/dashboard')
def dashboard():
    """Dashboard route with improved error handling"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        profile_completion = calculate_profile_completion(user_id)
        latest_test_result = get_latest_test_result(user_id)
        
        # Get or generate user roadmap
        user_roadmap = get_user_roadmap(user_id)
        if not user_roadmap and profile_completion > 0:
            # Generate roadmap if user has completed profile but no roadmap exists
            user_roadmap = generate_user_roadmap(user_id)
        
        return render_template('DefaultDashboard_fixed.html',
                               user_name=session['user_name'],
                               profile_completion=profile_completion,
                               latest_test_result=latest_test_result,
                               user_roadmap=user_roadmap)
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash('Error loading dashboard. Please try again.', 'danger')
        return redirect(url_for('home'))

@app.route('/test_history')
def test_history():
    """Test history route"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        results = get_all_test_results(session['user_id'])
        return render_template('test_history.html', 
                               user_name=session['user_name'], 
                               results=results)
    except Exception as e:
        print(f"Test history error: {e}")
        flash('Error loading test history.', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/test')
def test():
    """Test route with improved error handling"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        # Check if question files exist
        python_file = 'python_mcqs.json'
        cpp_file = 'cpp_mcqs.json'
        
        if not os.path.exists(python_file) or not os.path.exists(cpp_file):
            flash('Test questions not available. Please contact administrator.', 'danger')
            return redirect(url_for('dashboard'))
        
        # Load Python questions
        with open(python_file, 'r', encoding='utf-8') as f:
            python_questions = json.load(f)
            for q in python_questions:
                q['topic'] = 'python'
        
        # Load C++ questions
        with open(cpp_file, 'r', encoding='utf-8') as f:
            cpp_questions = json.load(f)
            for q in cpp_questions:
                q['topic'] = 'cpp'

        # Validate we have enough questions
        if len(python_questions) < 10 or len(cpp_questions) < 10:
            flash('Not enough questions available for testing.', 'danger')
            return redirect(url_for('dashboard'))

        # Select 10 random questions from each topic
        selected_python = random.sample(python_questions, 10)
        selected_cpp = random.sample(cpp_questions, 10)
        
        # Combine and shuffle
        final_questions = selected_python + selected_cpp
        random.shuffle(final_questions)
        
        # Store questions in session for submission validation
        session['test_questions'] = final_questions
        
    except FileNotFoundError as e:
        flash(f"Test file not found: {e.filename}", 'danger')
        return redirect(url_for('dashboard'))
    except json.JSONDecodeError as e:
        flash("Error reading test questions. Please contact administrator.", 'danger')
        return redirect(url_for('dashboard'))
    except ValueError as e:
        flash("Not enough questions available for testing.", 'danger')
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Test loading error: {e}")
        flash("Error loading test. Please try again.", 'danger')
        return redirect(url_for('dashboard'))

    return render_template('test.html', 
                           questions=final_questions,
                           user_name=session.get('user_name'))

@app.route('/submit_test', methods=['POST'])
def submit_test():
    """Submit test route with improved error handling"""
    if 'user_id' not in session or 'test_questions' not in session:
        flash('Your session has expired. Please start the test again.', 'warning')
        return redirect(url_for('test'))
    
    questions = session.get('test_questions', [])
    if not questions:
        flash('No questions found in your session. Please start the test again.', 'warning')
        return redirect(url_for('test'))

    try:
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
        
        # Save to database
        db = get_db()
        if db:
            try:
                db.execute('''
                    INSERT INTO test_results (user_id, user_name, python_score, cpp_score, total_score, percentage)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (session['user_id'], session['user_name'], python_score, cpp_score, total_score, percentage))
                db.commit()
            except sqlite3.Error as e:
                print(f"Database error saving test result: {e}")
                flash('Error saving test result.', 'danger')
            finally:
                db.close()
        
        session.pop('test_questions', None)
        
        flash('Test submitted successfully!', 'success')
        return redirect(url_for('test_result', 
                               python_score=python_score,
                               cpp_score=cpp_score,
                               total_score=total_score,
                               percentage=round(percentage, 2)))
                               
    except Exception as e:
        print(f"Test submission error: {e}")
        flash('Error submitting test. Please try again.', 'danger')
        return redirect(url_for('test'))

@app.route('/test_result')
def test_result():
    """Test result route with improved validation"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        python_score = request.args.get('python_score', 0, type=int)
        cpp_score = request.args.get('cpp_score', 0, type=int)
        total_score = request.args.get('total_score', 0, type=int)
        percentage = request.args.get('percentage', 0, type=float)
        
        # Validate scores
        if python_score < 0 or cpp_score < 0 or total_score < 0 or percentage < 0:
            flash('Invalid test result data.', 'danger')
            return redirect(url_for('dashboard'))
            
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
    """Questionnaire route with improved validation"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    if not db:
        flash('Database connection error. Please try again.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        if request.method == 'POST':
            # Get and validate form data
            role = request.form.get('role', '').strip()
            target_company = request.form.get('company', '').strip()
            position = request.form.get('position', '').strip()
            previous_skills = ','.join(request.form.getlist('skills'))
            specialization = request.form.get('specialization', '').strip()
            skill_focus = request.form.get('skill_focus', '').strip()

            # Validate required fields
            required_fields = ['role', 'company', 'position', 'specialization', 'skill_focus']
            errors = validate_form_data(request.form, required_fields)
            
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('questionnaire.html', 
                                     user_name=session['user_name'], 
                                     preferences=None)

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
            return redirect(url_for('dashboard'))

        # For GET request, fetch existing preferences
        prefs = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (session['user_id'],)).fetchone()
        
        # The 'previous_skills' are stored as a comma-separated string, so we split it for the template
        if prefs and prefs['previous_skills']:
            # Create a mutable copy of the row object
            prefs_dict = dict(prefs)
            prefs_dict['previous_skills'] = prefs_dict['previous_skills'].split(',')
            prefs = prefs_dict

        return render_template('questionnaire.html', 
                             user_name=session['user_name'], 
                             preferences=prefs)
                             
    except sqlite3.Error as e:
        print(f"Questionnaire database error: {e}")
        flash('Database error. Please try again.', 'danger')
        return redirect(url_for('dashboard'))
    finally:
        db.close()

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/guidelines')
def guidelines():
    """Community guidelines page"""
    return render_template('guidelines.html', user_name=session.get('user_name'))

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html', user_name=session.get('user_name'))

@app.route('/copyright')
def copyright():
    """Copyright page"""
    return render_template('copyright.html', user_name=session.get('user_name'))

@app.route('/terms')
def terms():
    """Terms and conditions page"""
    return render_template('terms.html', user_name=session.get('user_name'))

@app.route('/how-it-works')
def how_it_works():
    """How it works page"""
    return render_template('how_it_works.html', user_name=session.get('user_name'))

@app.route('/roadmap')
def roadmap_page():
    """Dedicated roadmap page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        # Get user preferences
        db = get_db()
        if not db:
            flash('Database connection error. Please try again.', 'danger')
            return redirect(url_for('dashboard'))
        
        user_prefs = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
        db.close()
        
        if not user_prefs:
            flash('Please complete your profile first to access the roadmap.', 'warning')
            return redirect(url_for('questionnaire'))
        
        # Convert to dict for template
        preferences = dict(user_prefs)
        
        return render_template('roadmap_page.html', 
                             user_name=session['user_name'],
                             user_preferences=preferences)
                             
    except Exception as e:
        print(f"Roadmap page error: {e}")
        flash('Error loading roadmap page. Please try again.', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/generate-roadmap', methods=['POST'])
def generate_roadmap_api():
    """API endpoint to generate roadmap based on user input"""
    if 'user_id' not in session:
        return {'error': 'Not authenticated'}, 401
    
    user_id = session['user_id']
    
    try:
        # Get form data
        skill_level = request.form.get('skill_level')
        duration = int(request.form.get('duration', 8))
        focus_area = request.form.get('focus_area')
        learning_goals = request.form.get('learning_goals', '')
        
        # Get user preferences
        db = get_db()
        if not db:
            return {'error': 'Database connection error'}, 500
        
        user_prefs = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
        db.close()
        
        if not user_prefs:
            return {'error': 'User preferences not found'}, 400
        
        # Update preferences with new data
        preferences = dict(user_prefs)
        preferences['skill_focus'] = skill_level
        preferences['learning_duration'] = duration
        preferences['focus_area'] = focus_area
        preferences['learning_goals'] = learning_goals
        
        # Generate enhanced roadmap
        roadmap = enhanced_roadmap_generator.generate_enhanced_roadmap(preferences)
        
        # Save roadmap
        if save_user_roadmap(user_id, roadmap):
            return {'success': True, 'roadmap': roadmap}
        else:
            return {'error': 'Failed to save roadmap'}, 500
            
    except Exception as e:
        print(f"Roadmap generation error: {e}")
        return {'error': 'Internal server error'}, 500

@app.route('/regenerate-roadmap', methods=['POST'])
def regenerate_roadmap():
    """Regenerate user's roadmap"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        # Generate new roadmap
        new_roadmap = generate_user_roadmap(user_id)
        if new_roadmap:
            flash('Your personalized roadmap has been updated!', 'success')
        else:
            flash('Error generating roadmap. Please complete your profile first.', 'warning')
    except Exception as e:
        print(f"Roadmap regeneration error: {e}")
        flash('Error regenerating roadmap. Please try again.', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/accept-roadmap', methods=['POST'])
def accept_roadmap():
    """Accept a roadmap and make it active"""
    if 'user_id' not in session:
        return {'error': 'Not authenticated'}, 401
    
    user_id = session['user_id']
    
    try:
        data = request.get_json()
        roadmap_data = data.get('roadmap')
        status = data.get('status', 'accepted')
        
        if not roadmap_data:
            return {'error': 'No roadmap data provided'}, 400
        
        # Save the accepted roadmap
        if save_user_roadmap(user_id, roadmap_data):
            # Update roadmap status in database
            db = get_db()
            if db:
                try:
                    db.execute('''
                        UPDATE user_roadmaps 
                        SET roadmap_data = ?, updated_date = CURRENT_TIMESTAMP 
                        WHERE user_id = ?
                    ''', (json.dumps(roadmap_data), user_id))
                    db.commit()
                except sqlite3.Error as e:
                    print(f"Error updating roadmap status: {e}")
                finally:
                    db.close()
            
            return {'success': True, 'message': 'Roadmap accepted successfully'}
        else:
            return {'error': 'Failed to save roadmap'}, 500
            
    except Exception as e:
        print(f"Accept roadmap error: {e}")
        return {'error': 'Internal server error'}, 500

@app.route('/save-roadmap-draft', methods=['POST'])
def save_roadmap_draft():
    """Save a roadmap as draft"""
    if 'user_id' not in session:
        return {'error': 'Not authenticated'}, 401
    
    user_id = session['user_id']
    
    try:
        data = request.get_json()
        roadmap_data = data.get('roadmap')
        status = data.get('status', 'draft')
        
        if not roadmap_data:
            return {'error': 'No roadmap data provided'}, 400
        
        # Save the draft roadmap
        if save_user_roadmap(user_id, roadmap_data):
            return {'success': True, 'message': 'Roadmap saved as draft'}
        else:
            return {'error': 'Failed to save roadmap'}, 500
            
    except Exception as e:
        print(f"Save roadmap draft error: {e}")
        return {'error': 'Internal server error'}, 500

@app.route('/update-roadmap-progress', methods=['POST'])
def update_roadmap_progress():
    """Update roadmap progress by marking topics as completed"""
    if 'user_id' not in session:
        return {'error': 'Not authenticated'}, 401
    
    user_id = session['user_id']
    
    try:
        data = request.get_json()
        completed_topic_id = data.get('topic_id')
        
        if not completed_topic_id:
            return {'error': 'No topic ID provided'}, 400
        
        # Get current roadmap
        roadmap = get_user_roadmap(user_id)
        if not roadmap:
            return {'error': 'No roadmap found'}, 404
        
        # Update roadmap progress
        updated_roadmap = enhanced_roadmap_generator.update_progress(roadmap, [completed_topic_id])
        
        # Save updated roadmap
        if save_user_roadmap(user_id, updated_roadmap):
            return {'success': True, 'roadmap': updated_roadmap}
        else:
            return {'error': 'Failed to update roadmap'}, 500
            
    except Exception as e:
        print(f"Update roadmap progress error: {e}")
        return {'error': 'Internal server error'}, 500

@app.route('/get-roadmap-details', methods=['GET'])
def get_roadmap_details():
    """Get detailed roadmap information for a specific phase"""
    if 'user_id' not in session:
        return {'error': 'Not authenticated'}, 401
    
    user_id = session['user_id']
    phase_id = request.args.get('phase_id', type=int)
    
    try:
        roadmap = get_user_roadmap(user_id)
        if not roadmap:
            return {'error': 'No roadmap found'}, 404
        
        if phase_id:
            # Return specific phase details
            phase = next((p for p in roadmap['phases'] if p['id'] == phase_id), None)
            if phase:
                return {'success': True, 'phase': phase}
            else:
                return {'error': 'Phase not found'}, 404
        else:
            # Return full roadmap
            return {'success': True, 'roadmap': roadmap}
            
    except Exception as e:
        print(f"Get roadmap details error: {e}")
        return {'error': 'Internal server error'}, 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Only initialize database for local development
    if app.config.get('USE_SQLITE', True):
        init_db()
    app.run(debug=True, use_reloader=False, threaded=True, port=5001)
