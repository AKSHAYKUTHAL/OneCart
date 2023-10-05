from django.shortcuts import render
from store.models import Product
from .models import Categories


def home(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})
