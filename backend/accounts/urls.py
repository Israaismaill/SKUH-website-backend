from django.urls import path
from .views import (
    RegisterView, EmailTokenObtainPairView, UserListView,
    create_appointment, update_appointment, delete_appointment,
    get_appointments, create_appointment_admin,
    get_doctors, create_doctor, update_doctor, delete_doctor,
    get_news, create_news, update_news, delete_news,
    verify_email
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # This makes the full URL: http://127.0.0.1:8000/api/register/
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('verify-email/', verify_email, name='verify_email'),
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('login/', EmailTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('doctors/', get_doctors, name='get_doctors'),
    path('doctors/create/', create_doctor, name='create_doctor'),
    path('doctors/<int:pk>/update/', update_doctor, name='update_doctor'),
    path('doctors/<int:pk>/delete/', delete_doctor, name='delete_doctor'),
    path('news/', get_news, name='get_news'),
    path('news/create/', create_news, name='create_news'),
    path('news/<int:pk>/update/', update_news, name='update_news'),
    path('news/<int:pk>/delete/', delete_news, name='delete_news'),
    path('appointments/', get_appointments, name='get_appointments'),
    path('appointments/create/admin/', create_appointment_admin, name='create_appointment_admin'),
    path('appointments/<int:pk>/update/', update_appointment, name='update_appointment'),
    path('appointments/<int:pk>/delete/', delete_appointment, name='delete_appointment'),
]