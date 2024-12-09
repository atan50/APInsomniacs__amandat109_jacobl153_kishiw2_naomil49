# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from databases import login_user, init_db, create_user, logout_user, get_recipes, get_news
# from database import create_user, login_user, logout_user, create_story, create_edit, get_stories, can_add_to_story, add_to_story, get_contributors

init_db()

# Secret key/setup
app = Flask(__name__)
app.secret_key = os.urandom(32)

# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return render_template('home.html')
    return render_template('home.html', username = session['username'])

# Register new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return create_user()
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        return login_user()
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    if 'username' in session:
        return logout_user()
    return redirect('/')
    # return render_template('logout.html')

# Profile route

# News page
@app.route('/news')
def news():
    news = get_news()
    return render_template('news.html', news = news)

# Catalog page

# Recipe page
@app.route('/recipes')
def recipes():
    recipes = get_recipes()
    return render_template('catalog.html', recipes = recipes)

# Add note

# Food page

# Brewery route
@app.route('/brewery', methods = ['GET', 'POST'])
def brewery():
    # if request.method == 'POST':
    #     return brewery_API()
    return redirect('/')


# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
