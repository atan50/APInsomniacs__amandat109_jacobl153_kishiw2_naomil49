# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
# from database import create_user, login_user, logout_user, create_story, create_edit, get_stories, can_add_to_story, add_to_story, get_contributors

# Secret key/setup
app = Flask(__name__)
app.secret_key = os.urandom(32)

# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return render_template('home.html')
    # If user is logged in, display specific content
    return render_template('home.html', username = session['username'])

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/')
    return render_template('login.html')

# Register new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()