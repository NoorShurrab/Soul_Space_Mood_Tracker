from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
import secrets
from django.core.cache import cache
from django.conf import settings
import bcrypt

# ============================================================
# Forgot Password — يبحث في Custom User model وليس auth.User
# ============================================================

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_list = User.objects.filter(email=email)

        if user_list.exists():
            user = user_list[0]
            
            # ولّدي token عشوائي واحفظيه في cache لمدة 30 دقيقة
            token = secrets.token_urlsafe(32)
            cache.set(f"reset_{token}", user.id, timeout=1800)
            
            reset_link = f"{request.scheme}://{request.get_host()}/reset/{token}/"

            send_mail(
                subject='Reset Your SoulSpace Password',
                message=f'Click the link to reset your password:\n\n{reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

        return redirect('/password_reset/done/')

    return render(request, 'registration/password_reset_form.html')


def reset_password_confirm(request, token):
    # اجيبي الـ user id من الـ cache
    user_id = cache.get(f"reset_{token}")
    
    if not user_id:
        return render(request, 'registration/password_reset_confirm.html', {
            'validlink': False
        })

    if request.method == 'POST':
        password = request.POST.get('new_password1')
        confirm = request.POST.get('new_password2')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/password_reset_confirm.html', {'validlink': True})

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, 'registration/password_reset_confirm.html', {'validlink': True})

        user = User.objects.get(pk=user_id)
        user.password = make_password(password, hasher='bcrypt')
        user.save()
        
        # احذفي الـ token بعد الاستخدام
        cache.delete(f"reset_{token}")
        
        return redirect('/reset/done/')

    return render(request, 'registration/password_reset_confirm.html', {'validlink': True})


# ============================================================
# باقي الـ views — بدون تغيير
# ============================================================
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                birthday=request.POST['birthday'],
                password=make_password(request.POST['password'], hasher='bcrypt')
            )
            messages.success(request, "Registration successful! Please log in to your account.", extra_tags='success-msg')
            return redirect('/login')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/login')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
            request.session['user_last_name'] = user.last_name

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect('/mood/dashboard')
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('/login')