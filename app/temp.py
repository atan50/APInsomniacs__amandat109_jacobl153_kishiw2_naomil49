from flask import Flask             
from flask import render_template   
from flask import request           
from flask import session

import testmod0
import os


app = Flask(__name__)   



@app.route("/")
def home():
    return render_template('home.html')


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
