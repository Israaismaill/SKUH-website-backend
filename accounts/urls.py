from django.urls import path
from .views import RegisterView, UserListView # Make sure this matches your View name in views.py
from accounts.views import create_appointment

urlpatterns = [
    # This makes the full URL: http://127.0.0.1:8000/api/register/
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('appointments/create/', create_appointment, name='create_appointment'),
]