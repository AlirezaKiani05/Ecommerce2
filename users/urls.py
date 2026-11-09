from django.urls import path
from .views import RegisteView, UserProfileView, keycloak_register, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from mozilla_django_oidc.views import OIDCLogoutView

# urlpatterns = [
#     path('register2/', RegisteView.as_view(), name='register'),
#     path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

# ]
urlpatterns = [

    path("login/", RedirectView.as_view(url="/oidc/authenticate/",
         permanent=False), name="login"),

    path("register/", keycloak_register, name='customer-register'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
