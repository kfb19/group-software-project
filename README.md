# group-software-project
Prerequisites:
  
  pip install django

  pip install django-axes

  pip install python-decouple

  pip install msal
  
  pip install PyYAML

  pip install python-dateutil

For testing:

  pip install coverage

  pip install flake8

In group_project1 folder 

run:
    
    python manage.py makemigrations

then:
    
    python manage.py migrate


To run app:
   
    python manage.py runserver

If you lock yourself out, do:
    
    python manage.py axes_reset
