from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.models import Cart,CartItem
from cart.views import _cart_id
import requests
from orders.models import Order,OrderProduct
from .forms import UserProfileForm
from .models import UserProfile





def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username alreadyy taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already taken.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request,'Registration successful, You can now login.')
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
    return render(request,'account/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(car=cart)

                    for item in cart_item:
                        item.user = user
                        user.save()

            except:
                pass

            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                messages.success(request,'You are now logged in.')
                return redirect('/')

        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'account/login.html')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    userprofile = get_object_or_404(UserProfile, user=request.user)
    orders_count = orders.count()

    context = {
        'orders_count':orders_count,
        'userprofile':userprofile,
    }
    return render(request,'account/dashboard.html',context)

def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')
    return redirect('/')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Resest Your Password'
            message = render_to_string('account/reset_password_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request,'Account Does Not Exist.')
            return redirect(request,'forgot_password')
    return render(request,'account/forgot_password.html')


def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Please Reset Your Password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password changed successfully')
            return redirect('login')
        else:
            messages.error(request,'Passwords do not match!')
            return redirect('reset_password')
        
    else:
        return render(request,'account/reset_password.html')



@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request,'account/my_orders.html',context)



@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
    else:
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'profile_form':profile_form,
        'userprofile':userprofile,
    }

    return render(request,'account/edit_profile.html',context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request,'Password updated successfully.')
                return redirect('change_password')   
            else:
                messages.error(request,'Please enter a valid current password')  
                return redirect('change_password')   
        else:
            messages.error(request,'The new passwords do not match')
            return redirect('change_password')   
        
    return render(request,'account/change_password.html')




@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price*i.quantity
    context = {
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal
    }
    return render(request,'account/order_detail.html',context)