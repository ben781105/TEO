set -o errexit
pip install -r requirements.txt

python manage.py collectstatic --no-input
<<<<<<< HEAD
pyhon manage.py migrate
=======
python manage.py migrate
>>>>>>> 7fb9ae95a59be0e8a03441a62c0edbc1016af45b
