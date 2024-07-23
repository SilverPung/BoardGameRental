from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from games.views import fetch_bgg_data
urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('summary/<int:event_id>/', views.summary, name='summary'),
    path('fetch_bgg_data/',fetch_bgg_data, name='fetch_bgg_data'),
]