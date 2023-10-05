from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Define the URL pattern for the custom login view
    path('logout', views.logout, name='logout'),

]