# NerdsWay


## Setup
### Installation
 - `pip install pipenv`
 - `pipenv shell`
 - `pipenv install`
 - Also don't forget to configure environment vars in production

### DB table creation
 - `python manage.py makemigrations`
 - `python manage.py migrate`

### Run
 - `python manage.py runserver`


## TODOs
 - edit post feature
 - add tag search dropdown
 - add pills css to tags
 - subscriber email add in maling list
 - RSS feed for every user

 Advanced TODOs:
 - create a recommendation system
 - Recommendation system - https://django-recommends.readthedocs.io/en/latest/
 - Push notifications - https://fcm-django.readthedocs.io/en/latest/
 - Jinja Templating - https://jinja.palletsprojects.com/en/3.0.x/switching/#django

 Optional TODOs:
 - move email functionality outside of view, maybe in models/signals
 - send email on signup
 - send email on login
 - create custom contact model and functionality
 - reduce (or if necessary then increase) font size, spacing, in pages like search and others