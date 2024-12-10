# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

def init_db():
    """initialize db if none exists"""
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    # User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('api_info.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredients TEXT NOT NULL
            content TEXT NOT NULL
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            image BLOB
            recipes REFERENCES recipes(name)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL
            content TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorite_recipes (
            user INTEGER PRIMARY KEY AUTOINCREMENT,
            recipes REFERENCES recipes(id)
        )
    ''')
    conn.commit()
    conn.close()

# init_db()

def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    # check if fields filled out
    if not username or not password:
        flash('Please fill out all fields.')
        return redirect('/login')

    with sqlite3.connect('user_info.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        users_pass = cursor.fetchone()

        if users_pass:
            if users_pass[0] == password:
                session['username'] = username
                flash('Successfully logged in.')
                return redirect('/')
        else:
            flash('Invalid username or password.')
    return redirect('/login')

def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_pass')

    # check if fields filled out
    if not username or not password or not confirm_pass:
        flash('Please fill out all fields.')

    elif password != confirm_pass:
        flash('Passwords do not match.')

    else:
        try:
            with sqlite3.connect('user_info.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                flash('User registered. Please log in.')
                return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username already exists.')
    return redirect('/register')

def logout_user():
    flash('Successfully logged out.')
    session.pop('username',)
    return redirect('/')
