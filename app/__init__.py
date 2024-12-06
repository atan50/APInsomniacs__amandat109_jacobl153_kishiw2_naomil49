# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from databases import login_user, init_db
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
    # If user is logged in, display specific content
    return render_template('home.html', username = session['username'])

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        # username = request.form.get('username')
        # password = request.form.get('password')

        # #  If fields not filled out
        # if not username or not password:
        #     redirect('/login', messaages="Please fill out both fields")

        # Validate credentials (to be inserted from databases.py)
        login_user()
        return redirect("/")


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
