from django.shortcuts import render
from store.models import Product
from .models import Categories
from store.models import ReviewRating

def home(request):
    products = Product.objects.all().filter(product_is_available=True).order_by('product_created_date')
    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id,status=True)

    context = {
        'products':products,
        'reviews':reviews,
    }

    return render(request,'index.html',context)
