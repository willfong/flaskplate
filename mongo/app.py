import os
import hashlib
import string
import random
import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient, ASCENDING, ReturnDocument
from functools import wraps
from flask import Flask, session, redirect, url_for, render_template, flash, g, request

app = Flask(__name__)

MONGODB_DBNAME = 'flaskplate_mongo_example'

db = MongoClient()[MONGODB_DBNAME]

DB_USERS = db.users
DB_USERS.create_index([('username', ASCENDING)], unique=True)


def passwd(password):
    return hashlib.sha256(password).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user_id' in session:
            flash('Please login first', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
@login_required
def main():
    users = DB_USERS.find()
    return render_template('main.html', users=users)

@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        if request.form['action'] == 'changepassword':
            DB_USERS.update_one(
                {'_id': ObjectId(session['user_id'])},
                {'$set': {'password': passwd(request.form['password'])}}
                )
            flash('Successfully updated password', 'success')
    return render_template('settings.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['action'] == 'login':
            user = DB_USERS.find_one_and_update(
                {'username': request.form['username'],'password': passwd(request.form['password'])},
                {'$inc': {'count': 1}},
                return_document=ReturnDocument.AFTER)
            if user is None:
                flash('Username/Password not found!', 'danger')
            else:
                session['user_id'] = str(user['_id'])
                return redirect(url_for('main'))

        if request.form['action'] == 'create':
            try:
                userinfo = {
                    'username': request.form['username'],
                    'password': passwd(request.form['password']),
                    'count': 1
                    }
                session['user_id'] = str(DB_USERS.insert_one(userinfo).inserted_id)
                return redirect(url_for('main'))
            except:
                flash('Username already exists! Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
