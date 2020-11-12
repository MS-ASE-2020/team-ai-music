# How to run backend

Now, the backend only depends on Django and corsheaders:

```bash
pip3 install django corsheaders
```

After the installation, run the following commands to update the database (We are currently using sqlite):

**NOTE that every time you pull this repo, you need to do migration!**

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Finally, you should be able to run this project:

```
python3 manage.py runserver
```

