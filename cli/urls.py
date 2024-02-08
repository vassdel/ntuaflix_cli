from django.urls import path
from . import views

urlpatterns = [
    path('cli/', views.cli, name='cli'),
]