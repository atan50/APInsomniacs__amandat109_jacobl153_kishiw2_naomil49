# Amanda Tan, Jacob Lukose, Naomi Lai, Kishi Wijaya
# APInsomniacs
# SoftDev
# P01: ArRESTed Development
# 2024-12-04
# Time spent: ___

from flask import request, flash, session
import sqlite3
import os

app = Flask(__name__, template_folder='/templates', static_folder='/static')
app.secret_key = os.urandom(32)

def init_db():
    """initialize db if none exists""""
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

init_db()
