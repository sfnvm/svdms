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