from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from datetime import timedelta
from .models import Member, Membership, MembershipHistory
from .serializers import MemberSerializer,MembershipSerializer, MembershipHistorySerializer, MembershipRenewSerializer




class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff



class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff



class AdminMemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.filter(user__is_staff=False, user__is_superuser=False)
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AdminMembershipListView(generics.ListAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return Membership.objects.all()  
    

class MembershipCreateView(generics.CreateAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        member_id = request.data.get("member") 
        if not member_id:
            return Response({"error": "Member ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            member = Member.objects.get(id=int(member_id))  
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        active_membership = Membership.objects.filter(member=member, end_date__gte=now().date()).exists()
        if active_membership:
            return Response({"error": "User already has an active membership"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(member=member)  
            return Response({
                "message": "Membership created successfully",
                "membership": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MembershipUpdateView(generics.UpdateAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Membership.objects.all()


class MembershipDeleteView(generics.DestroyAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Membership.objects.all()




class MembershipRenewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def renew_membership(self, request):
        try:
            membership = Membership.objects.get(member__user=request.user)

            serializer = MembershipRenewSerializer(data=request.data)

            if serializer.is_valid():
                renewal_type = serializer.validated_data["renewal_type"]
                amount_paid = serializer.validated_data["amount_paid"]
                
                membership.renew_membership(renewal_type, amount_paid)

                return Response({
                    "message": "Membership renewed successfully",
                    "new_end_date": membership.end_date
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Membership.DoesNotExist:
            return Response({"error": "No active membership found for this user"}, status=status.HTTP_404_NOT_FOUND)

        

        

class MembershipHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MembershipHistorySerializer

    def get_queryset(self):
        member_id = self.request.user.id 
        
        if member_id:
            return MembershipHistory.objects.filter(member_id=member_id).order_by("-renewed_on")
        
        return MembershipHistory.objects.none()  


class RenewHistoryofall(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = MembershipHistorySerializer

    def get_queryset(self):
        """
        If the user is an admin, return the full membership history table.
        Otherwise, return only the logged-in user's history.
        """
        if self.request.user.is_staff:  # Check if user is an admin/staff
            return MembershipHistory.objects.all().order_by("-renewed_on")

        return MembershipHistory.objects.filter(member_id=self.request.user.id).order_by("-renewed_on")
    


class MembershipByMemberIDView(generics.ListAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        try:
            member = Member.objects.get(user=self.request.user)
            return Membership.objects.filter(member=member) 
        
        except Member.DoesNotExist:
            return Membership.objects.none()  
 

