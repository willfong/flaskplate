# Flaskplate - Boilerplate for Python/Flask

Technology should make our lives easier.


## The problem

There should be a way to get app ideas from our heads into a web site quickly. From there, the app can be tested and improved. Stop planning, and start implementing and iterating!


## The goal

Flaskplate is for putting ideas onto a web application easily and quickly without needing to be a full-time programmer.


## Why Flaskplate

Flaskplate uses the Python programming language because it is clean and easy to read. Python is also easily available on most platforms.

Flaskplate uses the Python web framework Flask. It is a minimal framework that handles the backend web site stuff. We wanted to use a minimal framework so you spend less time debugging the framework and more time putting logic into your application.


## Who this is for

Non-programmers
CRUD (Create, Read, Update, Delete) ideas


## Requirements




## Set up

```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
sqlite3 app.db < schema.sql
FLASK_APP=app.py FLASK_DEBUG=1 flask run --host=0.0.0.0
```
