from django.urls import path
from . import views
urlpatterns = [
    
    path('profile/', views.profile, name='profile'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),

]