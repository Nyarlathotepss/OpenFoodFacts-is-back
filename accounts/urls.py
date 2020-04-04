from django.urls import path
from .views import SignUpView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user_account/', views.user_account, name='user_page'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
]