# Python Flask Boilerplate


## Set up

```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
sqlite3 app.db < schema.sql
FLASK_APP=app.py FLASK_DEBUG=1 flask run --host=0.0.0.0
```
