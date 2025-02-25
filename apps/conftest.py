import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.members.models import Member

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username="testuser", email="test@example.com", password="TestPassword123!", **kwargs):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        return user
    return _create_user

@pytest.fixture
def regular_user(create_user):
    return create_user(
        username="regularuser",
        email="regular@example.com",
        first_name="Regular",
        last_name="User"
    )

@pytest.fixture
def admin_user(create_user):
    return create_user(
        username="adminuser",
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        is_admin=True,
        is_staff=True
    )

@pytest.fixture
def authenticated_client(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def member(regular_user):
    return Member.objects.create(
        user=regular_user,
        first_name=regular_user.first_name
    )

@pytest.fixture
def user_registration_data():
    return {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'NewUserPass123!',
        'password2': 'NewUserPass123!',
        'first_name': 'New',
        'last_name': 'User'
    }

@pytest.fixture
def user_login_data(regular_user):
    return {
        'username': 'regularuser',
        'password': 'TestPassword123!'
    }

@pytest.fixture
def invalid_login_data():
    return {
        'username': 'nonexistentuser',
        'password': 'WrongPassword123!'
    }