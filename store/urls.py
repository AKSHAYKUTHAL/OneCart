from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='category_sort'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_details,name='product_details'),
    path('search_store',views.search_store,name='search_store'),
    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review'),

]
