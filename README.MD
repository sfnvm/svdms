# Setup
- Install **PostgreSQL || version ^v12**
- Install **python3 version ^v3.7.7**
- Install **virtualenv** with pip
```console
pip install virtualenv
```
- Clone this repo to your hard drive
- Open terminal, cd into repo folder
```console
$ cd svdms
```
- Setup virtual environment
```console
$ virtualenv .env
```
- Install requirements
```console
$ pip install -r requirements.txt
```
- Create database with name **django_quickstart**
- Create user with username == **trungpt** && **password == 0812**
- Grant full permissions on this db to user trungpt
- Go to project folder create **.env.dev** file, put this line below into .env.dev
```text
DATABASE_URL=postgres://trungpt:0812@localhost:5432/django_quickstart
```
- Get into virtual environment
```console
$ source .env/bin/activate
```
- Migrate db
```console
$ python manage.py makemigrations
$ python manage.py migrate
```
- Run server locally
```console
$ python manage.py runserver
```

# Export DB img
```console
$ python manage.py graph_models -a -g -o db.png  
$ python manage.py graph_models -a -o db.png  
```

# Create Superusers
```console
$ python manage.py createsuperuser --email trungpt.dev@gmail.com --username trungpt  
```
/* my password: 0812 */  

# Run Server locally
```console
$ python manage.py runserver  
```

# File '.env.dev'
```text
DATABASE_URL=postgres://trungpt:0812@localhost:5432/django_quickstart  
```

# Fix Errors
MacOS (*unix systems): pygraphviz path error  
```console
$ pip install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz
```
  
Static files error when deploy heroku: [source](https://stackoverflow.com/questions/36665889/collectstatic-error-while-deploying-django-app-to-heroku)
```console
$ heroku config:set DISABLE_COLLECTSTATIC=1
$ git push heroku master
$ heroku run python manage.py makemigration
$ heroku run python manage.py migrate
$ heroku run python manage.py collectstatic --noinput
$ heroku config:unset DISABLE_COLLECTSTATIC
$ heroku run python manage.py collectstatic
```