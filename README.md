# UniExplore

## Introduction

UniExplore is an application designed to help students explore their university and connect with their peers. Students can complete challenges at various locations across campus, see what their classmates did for those challenges, and like the responses of others.

## Prerequisites:

- pip install django 
- pip install django-axes
- pip install python-decouple
- pip install msal
- pip install PyYAML
- pip install python-dateutil
- pip install coverage
- pip install flake8

## Getting Started

Make sure you are in the UniExplore directory:

    cd UniExplore
    
Then run:

    python manage.py makemigrations
    
Then run:

    python manage.py migrate
    
Then, to run the application:

    python manage.py runserver
    
If you lock yourself out, do:

    python manage.py axes_reset
    
To create an admin account:

    python manage.py createsuperuser
    
## Authors

- Conor Behard Roberts
- Kate Belson
- Michael Hills
- Tomas Premoli
- Jack Purkiss
- Lucas Smith

## Handle

https://github.com/ExeterTeam25/group-software-project

## Publish Date

- Version 0.0.1 is currently in development.

## License

[MIT](https://choosealicense.com/licenses/mit/)

Please look in the LICENSE file for more information.
