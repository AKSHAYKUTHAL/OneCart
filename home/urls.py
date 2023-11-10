from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('change-language/<str:language_code>/', views.change_language, name='change_language'),

]