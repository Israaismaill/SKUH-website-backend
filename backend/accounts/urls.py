from django.urls import path
from .views import RegisterView, EmailTokenObtainPairView, create_appointment, get_doctors, get_news 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # This makes the full URL: http://127.0.0.1:8000/api/register/
    path('register/', RegisterView.as_view(), name='register'),
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('login/', EmailTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('doctors/', get_doctors, name='get_doctors'),
    path('news/', get_news, name='get_news'),
]