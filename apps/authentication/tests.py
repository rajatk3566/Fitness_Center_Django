import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db  

class TestAuthentication:
    def test_register_valid_user(self, api_client, user_registration_data):
        """Test user registration with valid data"""
        url = reverse('register')
        response = api_client.post(url, user_registration_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        assert 'user' in response.data
        assert 'message' in response.data
        
        assert response.data['user']['username'] == user_registration_data['username']
        assert response.data['user']['email'] == user_registration_data['email']
        assert response.data['user']['first_name'] == user_registration_data['first_name']
        
        from django.contrib.auth import get_user_model
        from apps.members.models import Member
        
        User = get_user_model()
        user = User.objects.get(username=user_registration_data['username'])
        member = Member.objects.filter(user=user).first()
        
        assert member is not None
        assert member.first_name == user_registration_data['first_name']
    
    def test_register_password_mismatch(self, api_client):
        """Test registration fails when passwords don't match"""
        url = reverse('register')
        invalid_data = {
            'username': 'failuser',
            'email': 'fail@example.com',
            'password': 'Password123!',
            'password2': 'DifferentPassword123!',
            'first_name': 'Fail',
            'last_name': 'User'
        }
        
        response = api_client.post(url, invalid_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        assert 'password' in response.data
    
    def test_login_valid_user(self, api_client, create_user):
        """Test user can log in and receive JWT tokens"""
        user = create_user(
            username='loginuser',
            email='login@example.com',
            password='LoginPass123!'
        )
        
        url = reverse('login')
        login_data = {
            'username': 'loginuser',
            'password': 'LoginPass123!'
        }
        
        response = api_client.post(url, login_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self, api_client):
        """Test login fails with invalid credentials"""
        url = reverse('login')
        login_data = {
            'username': 'nonexistentuser',
            'password': 'WrongPassword123!'
        }
        
        response = api_client.post(url, login_data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_refresh(self, api_client, create_user):
        """Test refresh token can be used to get a new access token"""
        user = create_user(
            username='refreshuser',
            email='refresh@example.com',
            password='RefreshPass123!'
        )
    
        login_url = reverse('login')
        login_data = {
            'username': 'refreshuser',
            'password': 'RefreshPass123!'
        }
        
        login_response = api_client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh': refresh_token
        }
        
        response = api_client.post(refresh_url, refresh_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        assert 'access' in response.data