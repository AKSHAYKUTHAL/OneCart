from .models import Product

def product_links(request):
    products = Product.objects.all()
    return dict(products=products)