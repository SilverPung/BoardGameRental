from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('fetch_bgg_data/', views.fetch_bgg_data, name='fetch_bgg_data'),
    path('add/<int:event_id>/', views.add_game, name='add_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
    
]