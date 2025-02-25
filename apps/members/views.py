from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from datetime import timedelta
from .models import Member, Membership
from .serializers import MemberSerializer, MembershipSerializer


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff



class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff



class AdminMemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserMembershipListView(generics.ListAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Membership.objects.filter(member__user=self.request.user)


class MembershipCreateView(generics.CreateAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("member")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        try:
            member = Member.objects.get(user__id=user_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=404)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(member=member)
            return Response({
                "message": "Membership created successfully",
                "membership": serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)


#For the User

class MembershipStatusView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            member = Member.objects.get(user=request.user)
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({"error": "Membership not found"}, status=status.HTTP_404_NOT_FOUND)

class RenewMembershipView(APIView):
    permission_classes = [IsAuthenticated, IsUser]  
    def post(self, request):
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)


        membership = Membership.objects.filter(member=member).order_by("-end_date").first()
        if not membership:
            return Response({"error": "No active membership found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_start = max(membership.end_date, now().date())
        membership.end_date = new_start + timedelta(days=30)
        membership.save()

        return Response({
            "message": "Membership renewed successfully",
            "new_end_date": membership.end_date
        }, status=status.HTTP_200_OK)

class MembershipHistoryView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            return Response({"error": "Membership not found"}, status=status.HTTP_404_NOT_FOUND)

        memberships = Membership.objects.filter(member=member).order_by("start_date")

        if not memberships.exists():
            return Response({"error": "No membership history found"}, status=status.HTTP_404_NOT_FOUND)

        history = []
        for membership in memberships:
            history.append({
                "event_type": "membership_start",
                "date": membership.start_date,
                "details": "Membership started"
            })
            history.append({
                "event_type": "membership_end",
                "date": membership.end_date,
                "details": "Membership ended"
            })

        return Response(history, status=status.HTTP_200_OK)
