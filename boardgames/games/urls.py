from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('add/<int:event_id>/', views.add_game, name='add_game'),
]