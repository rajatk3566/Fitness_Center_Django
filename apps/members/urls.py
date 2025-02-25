from django.urls import path
from .views import (
    MembershipStatusView,
    RenewMembershipView,
    MembershipHistoryView,
    AdminMemberViewSet,
    UserMembershipListView,
    MembershipCreateView
)

urlpatterns = [
    path("admin/members/", AdminMemberViewSet.as_view({'get': 'list'}), name="members"),
    path("members/", MembershipStatusView.as_view(), name="membership_status"),
    path("members/renew/", RenewMembershipView.as_view(), name="renew_membership"),
    path("members/history/", MembershipHistoryView.as_view(), name="membership_history"),

    path("admin/memberships/", UserMembershipListView.as_view(), name="admin_membership_list"),
    path("admin/memberships/create/", MembershipCreateView.as_view(), name="admin_create_membership"),
]
