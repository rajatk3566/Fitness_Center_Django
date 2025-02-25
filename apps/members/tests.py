import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.members.models import Member

pytestmark = pytest.mark.django_db 
class TestAdmin:
    def test_admin_flag(self, admin_user, regular_user):
        """Test that admin flag is correctly set"""
       
        assert regular_user.is_admin is False
        
        assert admin_user.is_admin is True
    
    def test_admin_login_to_admin_site(self, client, admin_user):
        """Test admin user can log in to the admin site"""
       
        login_successful = client.login(
            username='adminuser',
            password='TestPassword123!'
        )
        assert login_successful is True
        
        response = client.get('/admin/')
        assert response.status_code == 200 or response.status_code == 302
        
        if response.status_code == 302:
            assert '/admin/login/' not in response.url
    
    def test_regular_user_cannot_access_admin_site(self, client, regular_user):
        """Test regular users cannot access the admin site"""
        login_successful = client.login(
            username='regularuser',
            password='TestPassword123!'
        )
        assert login_successful is True
        
        response = client.get('/admin/')
      
        assert response.status_code in [302, 403]
        
        if response.status_code == 302:
            assert '/admin/login/' in response.url
    
    def test_admin_user_permissions(self, admin_user):
        """Test admin user has appropriate permissions"""
        assert admin_user.is_staff is True




User = get_user_model()
pytestmark = pytest.mark.django_db  

class TestMembership:
    def test_member_creation(self, member, regular_user):
        """Test member is created correctly"""

        assert member.first_name == 'Regular'
        assert member.user.username == 'regularuser'
        assert member.user == regular_user
    
    def test_member_created_on_registration(self, api_client, user_registration_data):
        """Test member is created when a user registers"""
       
        register_url = reverse('register')
        response = api_client.post(register_url, user_registration_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        
        new_user = User.objects.get(username=user_registration_data['username'])
        member = Member.objects.filter(user=new_user).first()
        
        assert member is not None
        assert member.first_name == user_registration_data['first_name']
    
    def test_member_update(self, member):
        """Test updating member information"""
        member.first_name = "UpdatedName"
        member.save()
        
        member.refresh_from_db()
        
        assert member.first_name == "UpdatedName"
    
    def test_member_deletion_on_user_delete(self, member, regular_user):
        """Test that member is deleted when user is deleted"""

        member_id = member.id
        
        regular_user.delete()
    
        assert Member.objects.filter(id=member_id).exists() is False
        
    def test_member_user_relationship(self, member, regular_user):
        """Test the relationship between User and Member models"""
        user_from_member = member.user
        assert user_from_member == regular_user
     
        try:

            member_from_user = regular_user.member
            assert member_from_user == member
        except AttributeError:

            member_from_user = Member.objects.get(user=regular_user)
            assert member_from_user == member