pip install -r requirements.txt

python3 manage.py collectstatic --no-input
python manage.py makemigrations
python3 manage.py migrate