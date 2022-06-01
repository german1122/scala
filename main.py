########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, flash, Flask, redirect, url_for, request, session, json
from flask_login import login_required, current_user
from Scala.__init__ import create_app, db


########################################################################################
# our main blueprint
main = Blueprint('main', __name__)
#app = Flask(__name__)
#@main.route('/') # home page that return 'index'
#def secret():
#    return render_template('secret.html')
@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)




app = create_app() # we initialize our flask app using the __init__.py function

if __name__ == '__main__':
    app.config['DEBUG'] = True
    db.create_all(app=create_app()) # create the SQLite database
    app.run(host="0.0.0.0", port=int("5000"), debug=True) # run the flask app on debug mode
