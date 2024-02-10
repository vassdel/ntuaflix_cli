from django.urls import path
from . import views

urlpatterns = [
    path('cli/', views.cli, name='cli'),
    path('application/x-www-form-urlencoded/', views.user_endpoint_view, name='user-endpoint'),
]