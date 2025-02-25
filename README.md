# Fitness Center Membership Management Using FastApi
  Fitness Center Membership Management web application using Django 
  
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

