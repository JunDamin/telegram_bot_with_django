rm db.sqlite3
python3.8 manage.py makemigrations
python3.8 manage.py migrate
ptyhon3.8 manage.py createsuperuser