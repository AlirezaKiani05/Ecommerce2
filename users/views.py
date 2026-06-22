from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer
from .models import Profile


User = get_user_model()

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import urllib.parse
from django.shortcuts import redirect

def logout_view(request):
    return redirect('oidc_logout')

def keycloak_register(request):

    login_url = reverse('oidc_authentication_init')
    register_url = f"{login_url}?prompt=register"
    
    return redirect(register_url)


class RegisteView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user)
        return profile


# class RegisterView(APIView):
#     def post(self ,request):
#        serializer=RegisterSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data,status=status.HTTP_201_CREATED)
#        return Response(status=status.HTTP_400_BAD_REQUEST)
