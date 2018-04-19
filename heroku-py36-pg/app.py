import os
import psycopg2
import psycopg2.extras
import hashlib
import string
import random
from functools import wraps
from flask import Flask, session, redirect, url_for, render_template, flash, g, request

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(DATABASE_URL, sslmode='require')
    return db

def read_db(query, params=(), one=False):
    if isinstance(params, tuple):
        args = params
    else:
        args = (params,)
    try:
        cur = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except psycopg2.Error as err:
        # TODO: need a way to determine operational error vs unique error
        # Don't log operational errors like unique key violations
        # This one logs everything.
        print("Database Error: {}".format(err))

def write_db(query, params=(), last_id=False):
    if isinstance(params, tuple):
        args = params
    else:
        args = (params,)
    if last_id:
        query = '{} RETURNING {}'.format(query, last_id)
    try:
        cur = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, args)
        get_db().commit()
    except psycopg2.Error as err:
        # TODO: need a way to determine operational error
        print("Database Error: {}".format(err))
        return False
    if last_id:
        return cur.fetchone()[0]
    else:
        return True

def safe_password(p):
    return hashlib.sha256(p.encode('utf-8')).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user_id' in session:
            flash('Please login first', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

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
@login_required
def main():
    query = ("SELECT id, name, created FROM lists WHERE users_id = %s")
    params = (session['user_id'])
    lists = read_db(query, params)
    return render_template('main.html', lists=lists)

@app.route('/list/new', methods=['POST'])
@login_required
def newlist():
    if len(request.form['name']) == 0:
        return redirect(url_for('main'))
    query = ("INSERT INTO lists (users_id, name) VALUES (%s, %s)")
    params = (session['user_id'], request.form['name'])
    list_id = write_db(query, params, 'id')
    if list_id:
        return redirect(url_for('list', id=list_id))
    else:
        flash('Something went wrong. Sorry.', 'warning')
        return redirect(url_for('main'))

@app.route('/list/<int:id>')
@login_required
def list(id):
    query = ("SELECT id, name, created FROM lists WHERE id = %s AND users_id = %s")
    params = (id, session['user_id'])
    list = read_db(query, params, one=True)
    if not list:
        flash('List not found!', 'danger')
        return redirect(url_for('main'))
    query = ("SELECT id, name FROM list_items WHERE lists_id = %s")
    params = (id)
    items = read_db(query, params)
    return render_template('list.html', list=list, items=items)

@app.route('/list/<int:id>/delete')
@login_required
def list_delete(id):
    query = ("SELECT id, name, created FROM lists WHERE id = %s AND users_id = %s")
    params = (id, session['user_id'])
    list = read_db(query, params, one=True)
    if not list:
        flash('List not found!', 'danger')
        return redirect(url_for('main'))
    query = ("DELETE FROM lists WHERE id = %s")
    params = (id)
    write_db(query, params)
    query = ("DELETE FROM list_items WHERE lists_id = %s")
    params = (id)
    write_db(query, params)
    return redirect(url_for('main'))

@app.route('/list/<int:id>/add', methods=['POST'])
@login_required
def list_additem(id):
    query = ("SELECT 1 FROM lists WHERE id = %s AND users_id = %s")
    params = (id, session['user_id'])
    list = read_db(query, params, one=True)
    if not list:
        flash('List not found!', 'danger')
        return redirect(url_for('main'))
    query = ("INSERT INTO list_items (lists_id, name) VALUES (%s, %s)")
    params = (id, request.form['name'])
    item = write_db(query, params)
    return redirect(url_for('list', id=id))

@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        if request.form['action'] == 'changepassword':
            query = ("UPDATE users SET password = %s WHERE id = %s")
            params = (safe_password(request.form['password']), session['user_id'])
            write_db(query, params)
            flash('Successfully updated password', 'success')
    return render_template('settings.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['action'] == 'create':
            query = ("INSERT INTO users (username, password) VALUES (%s, %s)")
            params = (request.form['username'], safe_password(request.form['password']))
            users_id = write_db(query, params, 'id')
            if users_id:
                flash('Welcome!', 'success')
                session['user_id'] = users_id
                return redirect(url_for('main'))
            else:
                flash('Something went wrong!', 'danger')
        else:
            query = ("SELECT id FROM users WHERE username = %s AND password = %s")
            params = (request.form['username'], safe_password(request.form['password']))
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

app.secret_key = os.environ['SESSION_KEY']

if __name__ == "__main__":
	app.run()
