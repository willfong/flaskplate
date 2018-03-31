# Getting Started

```
git init
heroku create
pipenv --python 3.6 shell
pipenv install
heroku config:set SESSION_KEY=`openssl rand -base64 32`
heroku config:get SESSION_KEY -s  >> .env
heroku addons:create heroku-postgresql:hobby-dev
heroku config:get DATABASE_URL -s  >> .env
heroku pg:psql < schema.sql
heroku local
git add .
git commit -am "boilerplate push"
git push heroku master
heroku ps:scale web=1
heroku logs --tail
```
