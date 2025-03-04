from django.urls import path
from .views import (
    AdminMemberViewSet,
    MembershipCreateView,
    AdminMemberCreateView,
    AdminMembershipListView,
    MembershipUpdateView,   
    MembershipDeleteView,
    MembershipRenewViewSet,
    MembershipHistoryViewSet
)
urlpatterns = [
    path("admin/members/", AdminMemberViewSet.as_view({'get': 'list'}), name="members"),
    path("admin/members/create/", AdminMemberCreateView.as_view(), name="create-member"), 
    path("memberships/", AdminMembershipListView.as_view(), name="admin_membership_list"),
    path("admin/memberships/create/", MembershipCreateView.as_view(), name="admin_create_membership"),
    path("admin/memberships/<int:pk>/update/", MembershipUpdateView.as_view(), name="update_membership"),  
    path("admin/memberships/<int:pk>/delete/", MembershipDeleteView.as_view(), name="delete_membership"),  
    path("memberships/<int:pk>/renew/", MembershipRenewViewSet.as_view({'post': 'renew_membership'}), name="renew-membership"),
    path("memberships/history/<int:member_id>/", MembershipHistoryViewSet.as_view({'get': 'list'}), name="membership-history"),


]





