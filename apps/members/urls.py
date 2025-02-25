from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminMemberViewSet, 
    UserMembershipListView, 
    MembershipCreateView
)

# router = DefaultRouter()
# router.register(r'members', AdminMemberViewSet) 

urlpatterns = [
    path('members/', AdminMemberViewSet.as_view({'get': 'list'}), name='members'),
    path('memberships/', UserMembershipListView.as_view(), name='membership-list'), 
    path('memberships/create/', MembershipCreateView.as_view(), name='membership-create'),  
]

