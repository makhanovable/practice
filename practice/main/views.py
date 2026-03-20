from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail


# Main
def main_view(request):
    return render(request, 'main.html')


# Registration
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    message = None
    success = None

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            message = 'Passwords do not match'
        elif User.objects.filter(username=username).exists():
            message = 'Username already exists'
        elif User.objects.filter(email=email).exists():
            message = 'Email already exists'
        else:
            user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

            token = signing.dumps({'user_id': user.id})
            send_mail(
                subject='Email confirmation',
                message=f'Click the link to confirm your account: http://127.0.0.1:8000/activate/{token}/',
                from_email='makhanovable@gmail.com',
                recipient_list=[email],
            )
            success = 'Confirmation email sent, please check your mail'

    return render(request, 'register.html', {'message': message, 'success': success})


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            message = 'Invalid username or password'

    return render(request, 'login.html', {'message': message})


# Logout
def logout_view(request):
    logout(request)
    return redirect('/')


# Activate
def activate_view(request, token):
    try:
        data = signing.loads(token, max_age=86400)
        user = User.objects.get(id=data['user_id'])
        user.is_active = True
        user.save()
        return redirect('/login/')
    except (signing.BadSignature, signing.SignatureExpired, User.DoesNotExist):
        return redirect('/')


# Some secret page
@login_required(login_url='/login/')
def secret_view(request):
    return render(request, 'secret.html')
