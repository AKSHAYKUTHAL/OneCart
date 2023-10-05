from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),  # Define the URL pattern for the custom login view
    path('logout', views.logout, name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<str:uidb64>/<str:token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password',views.reset_password,name='reset_password'),
]