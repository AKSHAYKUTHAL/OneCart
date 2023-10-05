from django.shortcuts import render, get_object_or_404
from cart.views import _cart_id
from . models import Product
from home.models import Categories
from cart.models import CartItem
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator







def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Categories, category_slug=category_slug)
        products = Product.objects.filter(category=categories, product_is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(product_is_available=True).order_by('id')
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request), is_active=True)
    cart_product_ids = []
    for item in cart_items:
        cart_product_ids.append(item.product.id)

    context = {
        'products': paged_products, 
        'cart_product_ids': cart_product_ids,
        'product_count':product_count
        }

    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__category_slug=category_slug, product_slug=product_slug)

    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request), is_active=True)
    cart_product_ids = []
    for item in cart_items:
        cart_product_ids.append(item.product.id)

    selected_color = product.product_colors
    selected_size = product.product_sizes 

    is_in_cart = product.id in cart_product_ids

    context = {
        'product': product,
        'product_slug': product_slug, 
        'cart_product_ids': cart_product_ids,
        'selected_color':selected_color,
        'selected_size':selected_size,
        'is_in_cart':is_in_cart
    }

    return render(request, 'store/product_details.html',context)




def search_store(request):
    query = None
    results = []
    if request.method == 'POST':
        query = request.POST.get('search_store')
        results = Product.objects.order_by('-product_created_date').filter(Q(product_name__icontains = query)| Q(product_description__icontains = query))
    
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request), is_active=True)
    cart_product_ids = []
    for item in cart_items:
        cart_product_ids.append(item.product.id)
    
    product_count = results.count()
    
    context = {
        'query':query,
        'products':results,
        'cart_product_ids':cart_product_ids,
        'product_count':product_count
    }
    return render(request,'store/store.html',context)