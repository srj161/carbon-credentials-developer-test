init:
	python manage.py makemigrations carbon_credentials
	python manage.py migrate

run:
	python manage.py runserver

test:
	python manage.py test
