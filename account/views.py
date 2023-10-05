from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage







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
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'account/login.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request,'account/dashboard.html')

def logout(request):
    auth.logout(request)
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