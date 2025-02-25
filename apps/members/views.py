from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from .models import Member, Membership
from .serializers import MemberSerializer, MembershipSerializer


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff  

class AdminMemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  

class UserMembershipListView(generics.ListAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]  

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
    
