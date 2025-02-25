# Fitness Center Membership Management Using Django
  Fitness Center Membership Management web application using Django-rest 
  
# Features Added 

* Implemented protected routes and role-based access control(Admin/User)

Admin Endpoints (To make an admin, go to the database and change 0 to 1)

1) Add a member
2) Update member details
3) Remove a member
4) View all members
5) View membership records

User Endpoints

1) View membership status
2) Renew membership
3) View payment & renewal history

 
# Folder Structure
```
└── 📁fitness_center
    └── 📁apps
        └── 📁authentication
            └── __init__.py
            └── admin.py
            └── apps.py
            └── 📁migrations
            └── models.py
            └── serializers.py
            └── tests.py
            └── urls.py
            └── views.py
        └── 📁members
            └── __init__.py
            └── admin.py
            └── apps.py
            └── 📁migrations
            └── models.py
            └── permissions.py
            └── serializers.py
            └── tests.py
            └── urls.py
            └── views.py
        └── conftest.py
    └── 📁fitness_center
        └── __init__.py
        └── asgi.py
        └── settings.py
        └── urls.py
        └── wsgi.py
    └── manage.py
    └── pytest.ini
    └── requirements.txt
```


#  To Setup

1. To clone the repository:

```bash
https://github.com/rajatk3566/Fitness_Center_Django.git
```

2. To create a virtual environment and activate:

```bash
python -m venv env
source .env/bin/activate
```

3. To Install dependencies:

```bash
pip install -r requirements.txt
```

4. To migrate

```bash
python manage.py makemigrations 
python manage.py migrate  
```       

5. To run the application:

```bash
python manage.py runserver   
```


# Test Suite for Fitness Center Membership Management (Django)

## Overview
This test suite ensures the correctness of the Fitness Center Membership Management system built with Django-rest. It covers authentication, database interactions, and API responses.

# To Setup 

1) Install dependencies

 ```bash
pip install -r requirements.txt
```

2) To run all Tests

```bash
pytest -v
```



