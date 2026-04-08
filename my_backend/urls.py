from django.http import HttpResponse
from django.urls import path, include
from django.contrib import admin

def home_view(request):
    return HttpResponse("<h1>Backend is Running!</h1><p>Go to /admin to see users.</p>")

urlpatterns = [
    path('', home_view), # This fixes the 404 at the root!
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
]