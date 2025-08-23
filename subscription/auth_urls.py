from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .auth_views import UserRegistrationAPIView, UserLoginAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]