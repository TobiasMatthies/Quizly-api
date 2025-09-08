from django.urls import path

from .views import (CookieTokenObtainPairView, LogoutAPIView, RegisterAPIView,
                    TokenRefreshAPIView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token-refresh')
]
