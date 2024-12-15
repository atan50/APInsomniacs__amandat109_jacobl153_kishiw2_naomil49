# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from databases import login_user, init_db, create_user, logout_user, get_recipes, get_news, get_recipe_content, get_breweries, get_favorites, get_nearest
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

# User routing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return create_user()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        return login_user()
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        return logout_user()
    return redirect('/')

# User-specific routing
@app.route('/profile')
def profile():
    if 'username' in session:
        user = session['username']
        info = get_favorites(user)
        return render_template('profile.html', username = session['username'])
    return redirect('/')

# Add comment
# @app.route('/catalog/<name>/comment', methods = ['GET', 'POST'])
# def comment():
#     if 'username' not in session:
#         flash('You must be logged in to add comments!')
#         return redirect(url_for('home'))
#     if request.method == 'POST':        

# General routing

# News page
@app.route('/news')
def news():
    news = get_news()
    return render_template('news.html', news = news)

# Catalog page
@app.route('/catalog')
def catalog():
    recipes = get_recipes()
    return render_template('catalog.html', recipes = recipes)

# Recipes page
@app.route('/catalog/<id>', methods=['GET', 'POST'])
def view(id):
    if request.method == 'POST':
        comment = request.form.get('content')
        add_comment(id, comment)
    info = get_recipe_content(id)
    # print("info: ",info)    
    id = info[0]
    ingredients = info[1]
    steps = info[2]
    name = info[3]
    image = info[4]
    print(len(info))
    if(len(info)>5):
        comment = info[5]
        return render_template('recipe.html', id=id, ingredients = ingredients, steps = steps, name = name, image=image, comment=comment)
    return render_template('recipe.html', id=id, ingredients = ingredients, steps = steps, name = name, image=image)

# Brewery route
@app.route('/brewery', methods = ['GET', 'POST'])
def brewery():
    if 'username' not in session:
        flash("You must be logged in!")
        return redirect('/')
    if request.method == 'POST':
        # print(2)
        info = get_breweries()
        nearest_id = get_nearest(info)
        nearest = info[nearest_id-1]
        return render_template('brewery.html', breweries=info, nearest=nearest)
    return render_template('brewery.html')

# Run
if __name__ == "__main__":
    app.debug = True
    app.run()
