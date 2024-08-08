from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('fetch_bgg_data/', views.fetch_bgg_data, name='fetch_bgg_data'),
    path('get_distributor_suggestions/', views.get_distributor_suggestions, name='get_distributor_suggestions'),
    path('add/<int:event_id>/', views.add_game, name='add_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
    
]