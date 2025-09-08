from django.urls import path

from .views import CookieTokenObtainPairView, RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login')
]
