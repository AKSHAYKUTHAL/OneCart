from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages



def _cart_id(request):
    if request.user.is_authenticated:
        # If the user is logged in, use their user ID as part of the cart ID
        cart_id = str(request.user.id)
        if 'cart_id' in request.session:
            # Merge the session cart items with the user's cart items if both exist
            session_cart_id = request.session['cart_id']
            if session_cart_id != cart_id:
                try:
                    session_cart = Cart.objects.get(cart_id=session_cart_id)
                    user_cart, created = Cart.objects.get_or_create(cart_id=cart_id)

                    # Transfer the session cart items to the user's cart
                    session_cart_items = CartItem.objects.filter(cart=session_cart)
                    for session_cart_item in session_cart_items:
                        # Check if the same item exists in the user's cart
                        user_cart_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=session_cart_item.product,
                            item_color=session_cart_item.item_color,
                            item_size=session_cart_item.item_size,
                            user=request.user,  # Set the user field to the logged-in user
                        )
                        if not created:
                            # If the item already exists, update the quantity by adding the session quantity
                            user_cart_item.quantity += session_cart_item.quantity
                        else:
                            # If the item did not exist in the user's cart, assign the session quantity
                            user_cart_item.quantity = session_cart_item.quantity
                        user_cart_item.save()

                    # Delete the session cart
                    session_cart.delete()
                    del request.session['cart_id']
                except Cart.DoesNotExist:
                    pass
        return cart_id
    else:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart_id = str(uuid.uuid4())  # Generate a random cart ID
            request.session['cart_id'] = cart_id
        return cart_id





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



def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        current_user = request.user
        cart_id = str(request.user.id)
    else:
        
        cart_id = _cart_id(request)
        request.session['cart_id'] = cart_id

    if request.method == 'POST':
        color = request.POST.get('color', 'choose')  # Default to 'choose' if not provided
        size = request.POST.get('size', 'choose')    # Default to 'choose' if not provided
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
            if product.product_stock > cart_item.quantity:
            # If the item exists, increase its quantity by 1
                cart_item.quantity += 1
                cart_item.save()
            else:
                alert_message = "Sorry, there is limited stock available for this product."
                messages.warning(request, alert_message)
        else:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.create(
                    user=current_user,
                    product=product,
                    quantity=1,
                    cart=cart,
                    item_color=color,
                    item_size=size,
                )
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
            if request.user.is_authenticated:
                cart = Cart.objects.create(cart_id=cart_id)
                cart_item = CartItem.objects.create(
                    user=current_user,
                    product=product,
                    quantity=1,
                    cart=cart,
                    item_color=color,
                    item_size=size,
                )
                cart_item.save()
            else:
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



@login_required(login_url='login')
def checkout(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request), is_active=True)

    # Calculate other checkout-related details here if needed
    total = 0
    for cart_item in cart_items:
        total += cart_item.sub_total()

    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'cart_items': cart_items,  # Pass the cart items to the template
        'total': total,            # Pass the total to the template
        'tax': tax,                # Pass the tax to the template
        'grand_total': grand_total  # Pass the grand total to the template
    }

    return render(request, 'store/checkout.html', context)


