# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

from flask import request, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Database path setup
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')

# connext to database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # So I can access dictionary items using their column name instead of indexing
    return conn

# Creates new user in the database
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Create users table if it doesn't exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                );
            ''')
            # Insert new user into the database
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            flash('Registration successful!', 'success')
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
        finally:
            conn.close()

# Logs in user if username and password match
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        # Retrieve hashed password for the given username
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user_password_hash = cur.fetchone()
        conn.close()

        # Checks hashed user password against database
        if user_password_hash and check_password_hash(user_password_hash['password_hash'], password):
            session['username'] = username
            flash('Login successful!', 'success')
        else:
            flash('Invalid username or password!', 'error')

# Logs out user
def logout_user():
    session.pop('username', None)
    flash('You have been logged out.', 'success')

#  Create a new story if the user is logged in
def create_story():
    if 'username' in session:
        username = session['username']
        title = request.form['title']
        edit = request.form['edit']

        conn = get_db_connection()
        cur = conn.cursor()

        # Retrieve the user ID for the current session's username
        user_id = cur.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()[0]
        
        # Create stories table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                story_id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_title TEXT NOT NULL UNIQUE,
                completed BOOLEAN DEFAULT False
            );
        ''')

        # Check if the story title already exists
        result = cur.execute("SELECT story_title FROM stories").fetchall()
        all_stories = [row['story_title'] for row in result]

        if title in all_stories:
            flash('Choose a different title, a story with this title already exists!', 'error')
            return False
        else:
            # Insert new story and commit changes
            cur.execute("INSERT INTO stories (story_title) VALUES(?)", (title,))
            conn.commit()
            create_edit(user_id, title, edit)
            flash('Story creation successful!', 'success')
        conn.close()
        return True
    else:
        flash('You must be logged in to create a story!', 'error')

# Create a new edit for a story
def create_edit(user_id, title, edit):
    conn = get_db_connection()
    cur = conn.cursor()

    # Retrieve story ID for the given title
    story_id = cur.execute("SELECT story_id FROM stories WHERE story_title = ?", (title,)).fetchone()[0]

    # Create story_edits table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS story_edits (
            edit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            story_id INTEGER NOT NULL,
            edit TEXT NOT NULL
        );
    ''')
    # Insert the new edit
    cur.execute("INSERT INTO story_edits (user_id, story_id, edit) VALUES (?, ?, ?)", (user_id, story_id, edit))
    conn.commit()
    conn.close()

# Validate the user's login credentials
def validate_login(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    # Retrieve the hashed password from the database
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user_password_hash = cur.fetchone()
    conn.close()

    if user_password_hash and check_password_hash(user_password_hash['password_hash'], password):
        return True
    else:
        return False

# Credit for everything above so far: P00, Indigo

