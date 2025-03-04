from django.urls import path
from .views import (
    AdminMemberViewSet,
    MembershipCreateView,
    AdminMembershipListView,
    MembershipUpdateView,   
    MembershipDeleteView,
    MembershipRenewViewSet,
    MembershipHistoryViewSet,
    RenewHistoryofall,
    MembershipByMemberIDView
    
)
urlpatterns = [
    path("admin/members/", AdminMemberViewSet.as_view({'get': 'list'}), name="members"),
    path("memberships/", AdminMembershipListView.as_view(), name="admin_membership_list"),
    path("membershipshistory/", MembershipByMemberIDView.as_view(), name="membership-by-member-id"),
    path("admin/memberships/create/", MembershipCreateView.as_view(), name="admin_create_membership"),
    path("admin/memberships/<int:pk>/update/", MembershipUpdateView.as_view(), name="update_membership"),  
    path("admin/memberships/<int:pk>/delete/", MembershipDeleteView.as_view(), name="delete_membership"),  
    path("memberships/renew/", MembershipRenewViewSet.as_view({'post': 'renew_membership'}), name="renew-membership"),
    path("memberships/history/", MembershipHistoryViewSet.as_view({'get': 'list'}), name="membership-history"),
    path("admin/history/", RenewHistoryofall.as_view({'get': 'list'}), name="fetchHisorty" ),


]





