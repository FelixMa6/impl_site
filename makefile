run:
	#python3 manage.py runserver 10.29.244.51:15800
	python3 manage.py runserver 10.10.0.70:15600

run_felix:
	python3 manage.py runserver 127.0.0.1:15600

01:
	python3 manage.py makemigrations

02:
	python3 manage.py migrate

add_app:
	python3 manage.py startapp release_check

setup:
	python3 django-admin.py startproject impl_site

admin:
	python3 manage.py createsuperuser
    
