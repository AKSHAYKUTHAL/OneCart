from django.shortcuts import render, get_object_or_404, redirect
from cart.views import _cart_id
from . models import Product,ReviewRating,ProductGallery,ProductColor,ProductSize
from home.models import Categories
from cart.models import CartItem
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal  # Import Decimal for precise decimal arithmetic
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string






def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Categories, category_slug=category_slug)
        products = Product.objects.filter(category=categories, product_is_available=True)
    else:
        products = Product.objects.all().filter(product_is_available=True).order_by('id')

    paginator = Paginator(products, 3)  # Initialize the paginator with 3 items per page
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    discounted_products = []
    for product in paged_products:
        discounted_price = product.product_price * Decimal('1.5')
        discounted_products.append((product, discounted_price))

    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request), is_active=True)
    cart_product_ids = []
    for item in cart_items:
        cart_product_ids.append(item.product.id)

    colors = ProductColor.objects.all()
    sizes = ProductSize.objects.all()


    context = {
        'products': paged_products, 
        'cart_product_ids': cart_product_ids,
        'product_count': product_count,
        'discounted_products': discounted_products,
        'colors':colors,
        'sizes':sizes,
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

    discounted_price = 0
    discounted_price = product.product_price * Decimal('1.5')

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id = product.id,status=True)

    product_gallery = ProductGallery.objects.filter(product_id=product.id)

    context = {
        'product': product,
        'product_slug': product_slug, 
        'cart_product_ids': cart_product_ids,
        'selected_color':selected_color,
        'selected_size':selected_size,
        'is_in_cart':is_in_cart,
        'discounted_price':discounted_price,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery
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
        
        
    discounted_products = []
    for product in results:
        discounted_price = product.product_price * Decimal('1.5')
        discounted_products.append((product, discounted_price))

    product_count = results.count()
    
    context = {
        'query':query,
        'products':results,
        'cart_product_ids':cart_product_ids,
        'product_count':product_count,
        'discounted_products':discounted_products,
    }
    return render(request,'store/store.html',context)


def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)




# def filter_products(request):
#     category_id = request.POST.get('category')
#     color = request.POST.getlist('color')
#     size = request.POST.getlist('size')
#     min_price = request.POST.get('min-price')
#     max_price = request.POST.get('max-price')

#     print(f"categories = {category_id}")
#     print(f"colors = {color}")
#     print(f"sizes = {size}")
#     print(f"min price = {min_price}")
#     print(f"max price = {max_price}")

#     # Ensure that min_price and max_price are converted to Decimal
#     min_price = Decimal(min_price) if min_price else Decimal('0')
#     max_price = Decimal(max_price) if max_price else Decimal('999999999')  # Update with a suitable maximum value


#     # Filter products based on the selected options
#     products = Product.objects.filter(
#         Q(category=category_id),
#         Q(product_colors__name__in=color) if color else Q(),  # Only filter if color is selected
#         Q(product_sizes__name__in=size) if size else Q(),  # Only filter if size is selected
#         Q(product_price__gte=min_price, product_price__lte=max_price),
#         product_is_available=True
#     )

#     # You can serialize the products and return them as JSON
#     product_data = [
#         {
#             'product_name': product.product_name,
#             'product_price': product.product_price,
#             # Add more fields as needed
#         }
#         for product in products
#     ]

#     return JsonResponse({'products': product_data})

