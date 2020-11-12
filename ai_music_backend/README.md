# How to run backend

Now, the backend only depends on Django:

```bash
pip3 install django
```

After the installation, run the following commands to update the database (We are currently using sqlite):

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Finally, you should be able to run this project:

```
python3 manage.py runserver
```

