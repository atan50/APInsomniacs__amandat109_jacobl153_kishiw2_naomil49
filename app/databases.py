# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

import sqlite3, os
from flask import Flask, request, render_template, redirect, url_for, flash, session
import API

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
            ingredients TEXT NOT NULL,
            content TEXT NOT NULL,
            name TEXT NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brewery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            longitude REAL NOT NULL,
            latitude REAL NOT NULL
        )
    ''')
    cursor.execute('''
    	CREATE TABLE IF NOT EXISTS news (
        	id INTEGER PRIMARY KEY AUTOINCREMENT,
        	title TEXT UNIQUE NOT NULL,
        	content TEXT NOT NULL,
        	link TEXT NOT NULL
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

def setup_brewery_table(): # Only run once because API.getBrews() contains all articles.
    try:
            with sqlite3.connect('api_info.db') as conn:
                all_info = API.getBrews()
                cursor = conn.cursor()
                for info in all_info:
                    name = info[0]
                    long = info[1]
                    lat = info[2]
                    if long is not None and lat is not None:
                        cursor.execute('INSERT INTO brewery (name, longitude, latitude) VALUES (?, ?, ?)', (name, long, lat))
                conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')

def setup_articles_table(): # Only run once because API.getArticles() contains all articles.
	try:
            with sqlite3.connect('api_info.db') as conn:
                all_info = API.getArticles()
                cursor = conn.cursor()
                for info in all_info:
                    title = info[2]
                    content = info[1]
                    link = info[0]
                    cursor.execute('INSERT INTO news (title, content, link) VALUES (?, ?, ?)', (title, content, link))
                conn.commit()
	except sqlite3.IntegrityError:
    		flash('Database Error')

def setup_recipes_table():
    try:
            with sqlite3.connect('api_info.db') as conn:
                total_recipes = 12 # total recipes added to database. Don't make too high because lack of quotas.
                cursor = conn.cursor()
                while(total_recipes > 0):
                    info = API.getRecipes()
                    ingredients = info[1]
                    content = info[2]
                    name = info[0]
                    image = info[3]
                    cursor.execute('INSERT INTO recipes (ingredients, content, name, image) VALUES (?, ?, ?, ?)', (ingredients, content, name, image))
                    total_recipes -= 1
                conn.commit()
    except sqlite3.IntegrityError:
        flash('Database Error')

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

# checking contents of tables
def print_table():
    try:
        with sqlite3.connect('api_info.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes")
            print("recipes:\n", cursor.fetchall(), "\n")
            cursor.execute("SELECT * FROM brewery")
            print("brewery:\n", cursor.fetchall(), "\n")
            cursor.execute("SELECT * FROM news")
            print("news:\n", cursor.fetchall(),"\n")
    except sqlite3.IntegrityError:
        print('Database Error')

# print_table()

# List of recipes from recipes table
def get_recipes():
    with sqlite3.connect('api_info.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT ingredients, content, name FROM recipes").fetchall()
        # print("get_reciptes():\n",result)
        return result

def get_news():
    with sqlite3.connect('api_info.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT title, content, link FROM news").fetchall()
        # print("get_news():\n",result)
        return result
