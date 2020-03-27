from django.urls import path
from . import views

urlpatterns = [
    path('bounce', views.bounce_handler),
]
