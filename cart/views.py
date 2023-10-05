from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse




def _cart_id(request):
    if request.user.is_authenticated:
        return str(request.user.id)
    else:
        cart = request.session.get('cart_id')
        if not cart:
            cart = str(uuid.uuid4())  # Generate a random cart ID
            request.session['cart_id'] = cart
        return cart


@login_required
def cart(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0

    cart_id = _cart_id(request)
 
    try:
        cart=Cart.objects.get(cart_id=cart_id)
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)

        for cart_item in cart_items:
            cart_item.total_price = cart_item.product.product_price * cart_item.quantity
            total += (cart_item.product.product_price*cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2*total)/100  
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        
    }
    return render(request, 'store/cart.html',context)


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_id = _cart_id(request)

    if request.method == 'POST':
        color = request.POST.get('color')
        size = request.POST.get('size')
    else:
        # If color and size are not provided in the POST request, set them to the first available options
        available_colors = product.product_colors.all()
        available_sizes = product.product_sizes.all()
        
        if available_colors:
            color = available_colors[0].name
        else:
            color = None
        
        if available_sizes:
            size = available_sizes[0].name
        else:
            size = None

    try:
        cart = Cart.objects.get(cart_id=cart_id)

        # Check if a cart item with the same product, size, and color already exists
        cart_item = CartItem.objects.filter(
            cart=cart,
            product=product,
            item_color=color,
            item_size=size,
        ).first()

        if cart_item:
            # If the item exists, increase its quantity by 1
            cart_item.quantity += 1
            cart_item.save()
        else:
            # If no such item exists, create a new cart item with the selected color and size
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                item_color=color,
                item_size=size,
            )
            cart_item.save()
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id)
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            item_color=color,
            item_size=size,
        )
        cart_item.save()

    return redirect('cart')







    # Create or get the Cart object using the cart_id
    

def remove_from_cart(request, product_id, color, size):
    cart_id = _cart_id(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_item = CartItem.objects.get(cart=cart, product=product, item_color=color, item_size=size)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            pass

        return redirect('cart')
    except Cart.DoesNotExist:
        pass

    return HttpResponseBadRequest("Product not found in the cart.")
   




def remove_stack_from_cart(request, product_id, color, size):
    cart_id = _cart_id(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_item = CartItem.objects.filter(cart=cart, product=product, item_color=color, item_size=size)

        if cart_item.exists():
            cart_item.delete()

        return HttpResponseRedirect(reverse('cart'))
    except Cart.DoesNotExist:
        pass

    return HttpResponseBadRequest("Product not found in the cart.")




