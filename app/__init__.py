# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

# Imports
import os
from flask import Flask, request, render_template, redirect, url_for, flash, session
from databases import login_user, init_db, create_user, logout_user
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

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        return login_user()
    return render_template('login.html')

# Register new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return create_user()
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    if 'username' in session:
        return logout_user()
    return redirect('/')
    # return render_template('logout.html')

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
