from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('add/<int:event_id>/', views.add_game, name='add_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
]