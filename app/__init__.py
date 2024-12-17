# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from databases import login_user, init_db, create_user, logout_user, add_favorite, delete_favorite, check_favorite, get_recipes, get_news, get_recipe_content, get_breweries, get_favorites, get_nearest, get_all_favorites
# from database import create_user, login_user, logout_user, create_story, create_edit, get_stories, can_add_to_story, add_to_story, get_contributors

init_db()
# print('\n\nget_recipes():', get_recipes())
# print('\n\nget_news():', get_news())
# print('\n\nget_breweries():', get_breweries())
# print("\n\nget_all_favorites:",get_all_favorites())

# Secret key/setup
app = Flask(__name__)
app.secret_key = os.urandom(32)

# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    print("\n\nget_all_favorites:",get_all_favorites())
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

# General routing

# News page
@app.route('/news')
def news():
    news = get_news()
    return render_template('news.html', news = news)

# Catalog page
@app.route('/catalog')
def catalog():
    print("\n\nget_all_favorites:",get_all_favorites())
    recipes = get_recipes()
    return render_template('catalog.html', recipes = recipes)

# Recipes page
@app.route('/catalog/<id>', methods=['GET', 'POST'])
def view(id):
    user = session.get('username')

    # Handle info
    if request.method == 'POST':
        if request.form.get('comment'):
            comment = request.form.get('content')
            add_comment(id, comment)
        if request.form.get('favorite'):
            fav = request.form.get('favorite')
            print("\n\nfav:", fav)
            if fav == 'false':
                print('rem')
                delete_favorite(id, user)
            if fav == 'true':
                print('add')
                add_favorite(id, user)  
        else:
            print("rem_2")
            delete_favorite(id, user)          
    
    # Access info
    info = get_recipe_content(id)
    # print("info: ",info)
    id = info[0]
    ingredients = databases.make_ingredients_list(info[3])
    steps = info[2]
    name = info[3]
    image = info[4]
    favorite = check_favorite(id,user)
    # print("\n\nfavorite:", favorite)
    print("\nget_all_favorites:",get_all_favorites())
    # print("\nfavorite:", favorite)
    if(len(info)>5):
        comment = info[5]
        return render_template('recipe.html', id=id, ingredients = ingredients, steps = steps, name = name, image=image, favorite = favorite, comment=comment)
    return render_template('recipe.html', id=id, ingredients = ingredients, steps = steps, name = name, image=image, favorite = favorite)

# @app.route('/favorite_item/<id>', methods=['GET', 'POST'])
# def favorite_item(id):
#     user = session.get('username')
#     add_favorite(id, user)
#     return redirect("/catalog/id")
#
# @app.route('/unfavorite_item/<id>', methods=['GET', 'POST'])
# def unfavorite_item(id):
#     user = session.get('username')
#     add_favorite(id, user)
#     return redirect("/catalog/id")

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
