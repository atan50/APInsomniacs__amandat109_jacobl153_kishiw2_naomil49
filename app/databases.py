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

def init_db():
    """initialize db if none exists"""
    if not os.path.exists('user_info.db'):
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorite_recipes (
                table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                recipe_id TEXT NOT NULL,
                deleted TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe_comments (
                table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                recipe_id TEXT NOT NULL,
                comment TEXT NOT NULL,
                deleted TEXT
            )
        ''')
        conn.commit()
        conn.close()
    if not os.path.exists('api_info.db'):
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

        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS favorite_recipes (
        #         user INTEGER PRIMARY KEY AUTOINCREMENT,
        #         recipes REFERENCES recipes(id)
        #     )
        # ''')
        conn.commit()
        setup_brewery_table()
        setup_articles_table()
        setup_recipes_table()
        conn.close()

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

#return favorite_recipes row length
def favorite_rows():
    try:
        with sqlite3.connect('user_info.db') as conn:
            cursor = conn.cursor()
            query = "SELECT COUNT(1) FROM favorite_recipes"
            cursor.execute(query)
            result = cursor.fetchone()
            row_count = result[0]
            return row_count
    except sqlite3.IntegrityError:
        print('Database Error')

# adding recipe to favorite_recipes database
def add_favorite(id, user):
    try:
        with sqlite3.connect('user_info.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO favorite_recipes (username, recipe_id) VALUES (?, ?)',
                           (user, id))
            conn.commit()
    except sqli            results = cursor.execute("SELECT * FROM favorite_recipes".fetchone()te3.IntegrityError:
        print('Database Error')

# deleting recipe from favorites list
def delete_favorite(id, user):
    try:
        with sqlite3.connect('user_info.db') as conn:
            cursor = conn.cursor()
            for i in range(1, favorite_rows()+1):
                results = cursor.execute("SELECT * FROM favorite_recipes WHERE table_id = ?", (i)).fetchone()
                temp_user = results[1]
                temp_recipe = results[2]
                if(temp_user == user and temp_recipe == id):
                    cursor.excute('UPDATE favorite_recipes SET deleted = ? WHERE table_id = ?', ('deleted'), (i))
            conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')

#checks if current viewing recipes is on user's favorites list
def check_favorite(id, user):
    try:
        with sqlite3.connect('user_info.db') as conn:
            for i in range(1, favorite_rows()+1):
                results = cursor.execute("SELECT * FROM favorite_recipes WHERE table_id = ?", (i)).fetchone()
                temp_user = results[1]
                temp_recipe = results[2]
                if(temp_user == user and temp_recipe == id):
                    return True
            return False
    except sqlite3.IntegrityError:
        print('Database Error')

#return recipe_comments row length
def comment_rows():
    try:
        with sqlite3.connect('user_info.db') as conn:
            cursor = conn.cursor()
            query = "SELECT COUNT(1) FROM recipe_comments"
            cursor.execute(query)
            result = cursor.fetchone()
            row_count = result[0]
            return row_count
    except sqlite3.IntegrityError:
        print('Database Error')

#adds comments
def add_comment(id, user, comment):
    try:
        with sqlite3.connect('user_info.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO recipe_comments (username, recipe_id, comment) VALUES (?, ?, ?)',
                           (user, id, comment))
            conn.commit()
    except sqlite3.IntegrityError:
        print('Database Error')

# checking contents of tables
def make_ingredients_list(name):
	try:
    	with sqlite3.connect('api_info.db') as conn:
        	cursor = conn.cursor()
        	cursor.execute("SELECT ingredients FROM recipes where name = ?", (name,))
        	ingredients = str(cursor.fetchall())[3:-4]
        	ingred_list = ingredients.split(" + ")
        	return ingred_list
	except sqlite3.IntegrityError:
    		print('Database Error')


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

# Accessing databases
def get_recipes():
    with sqlite3.connect('api_info.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM recipes").fetchall()
        # print("get_reciptes():\n",result)
        return result

def get_news():
    with sqlite3.connect('api_info.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM news").fetchall()
        # print("get_news():\n",result)
        return result

def get_recipe_content(id):
    with sqlite3.connect('api_info.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM recipes WHERE id = ?", (id,)).fetchone()
        if not result:
            # flash("No recipe found")
            print("no recipe")
            return redirect(url_for('home'))
        # print("get_recipe_content():\n",result)
        return result

def get_breweries():
    with sqlite3.connect('api_info.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM brewery").fetchall()
        # if not result:
        #     # flash("No recipe found")
        #     print("no recipe")
        #     return redirect(url_for('home'))
        # print("get_brewery_content():\n",result)
        return result

def get_nearest(info):
    return 1

# showing recipes on favorites/profile page
def get_favorites():
    try:
        with sqlite3.connect('user_info.db') as conn:
            cursor = conn.cursor()
            data = []
            for i in range(1, favorite_rows()+1):
                results = cursor.execute("SELECT * FROM favorite_recipes WHERE table_id = ?", (i)).fetchone()
                if(results[3] == NULL):
                    temp_id = results[2]
                    conn.close()
                    with sqlite3.connect('api_info.db') as conn:
                        cursor = conn.cursor()
                        result = cursor.execute("SELECT * FROM recipes WHERE id = ?", (temp_id)).fetchone()
                        data.append(result)
            # Function not finished: add access favorites column, which does not exist yet

            # print("get_user_favorites():\n",result)
            return data
    except sqlite3.IntegrityError:
        print('Database Error')
