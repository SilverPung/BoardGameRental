from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm


urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('summary/<int:event_id>/', views.summary, name='summary'),
    path('signup/', views.signup, name='signup'),
]

