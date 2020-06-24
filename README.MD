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
```console
$ pip install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz
```