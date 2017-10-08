import os
import sqlite3
import string
import random
from flask import Flask, session, redirect, url_for, render_template, flash, g, request

app = Flask(__name__)

DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def read_db(query, args=(), one=False):
    # TODO: maybe add a check if args only has one, make it a tuple
    try:
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.OperationalError as err:
        print "Database Error: {}".format(err)

def write_db(query, args=()):
    # TODO: maybe add a check if args only has one, make it a tuple
    try:
        get_db().cursor().execute(query, args)
        get_db().commit()
    except sqlite3.OperationalError as err:
        print "Database Error: {}".format(err)

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print "Testing initial users..."
        query = ("SELECT * FROM users")
        print read_db(query)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/main')
def main():
    if not 'user_id' in session:
        return redirect(url_for('login'))
    query = ("SELECT id, username FROM users")
    users = read_db(query)
    return render_template('main.html', users=users)

@app.route('/settings', methods=['GET','POST'])
def settings():
    if not 'user_id' in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['action'] == 'changepassword':
            query = ("UPDATE users SET password = ? WHERE id = ?")
            params = (request.form['password'], session['user_id'])
            write_db(query, params)
            flash('Successfully updated password', 'success')
        elif request.form['action'] == 'createuser':
            query = ("INSERT INTO users (username, password) VALUES (?, ?)")
            params = (request.form['username'], request.form['password'])
            write_db(query, params)
            flash('Successfully added user', 'success')
    return render_template('settings.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        query = ("SELECT id FROM users WHERE username = ? AND password = ?")
        params = (request.form['username'], request.form['password'])
        user = read_db(query, params, one=True)
        if user is None:
            flash('Username/Password not found!', 'danger')
        else:
            session['user_id'] = user['id']
            return redirect(url_for('main'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
