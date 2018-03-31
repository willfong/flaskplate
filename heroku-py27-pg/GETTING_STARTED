# Getting Started


# Heroku Setup

```
heroku create
pipenv --python 2.7 shell
pipenv install
heroku config:set SESSION_KEY=`openssl rand -base64 32`
heroku config:get SESSION_KEY -s  >> .env
FLASK_APP=app.py flask run --port=5000
heroku ps:scale web=1
heroku logs --tail

```

# DATABASE

```
heroku addons:create heroku-postgresql:hobby-dev
heroku config:get DATABASE_URL -s  >> .env
heroku pg:psql < schema.sql
```
