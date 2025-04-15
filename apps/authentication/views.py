from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer
from apps.members.models import Member

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            Member.objects.create(
                user=user,
                first_name=user.first_name, 
            )

            return Response({
                "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
                "message": "User created successfully and added to members",
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")  
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)  
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=401)

        user = authenticate(request, username=user.username, password=password)  

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "is_admin": user.is_admin,  
                "message": "Login successful!"
            }, status=200)

        return Response({"detail": "Invalid credentials"}, status=401)



from django.http import JsonResponse

def apm_test_view(request):
    return JsonResponse({"status": "ok"})