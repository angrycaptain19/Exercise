from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import auth
from .forms import LoginForm, RefForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            if user is None:
                login_form.add_error(None, '用户名或密码错误')
                content = {'login_form': login_form}
                return render(request, 'login.html', content)
            else:
                auth.login(request, user)
                return redirect('/ex')

    else:
        login_form = LoginForm()
        referer = request.META.get('HTTP_REFERER', '/ex')
        content = {'login_form': login_form, 'referer': referer}
        return render(request, 'login.html', content)


def register(request):
    if request.method == 'POST':
        reg_form = RefForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.first_name = reg_form.cleaned_data['name']
            user.save()
            # 登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('/ex')
        else:
            content = {'reg_form': reg_form}
            return render(request, 'register.html', content)
    else:
        reg_form = RefForm()
        content = {'reg_form': reg_form}
        return render(request, 'register.html', content)


def logout(request):
    auth.logout(request)
    return redirect('/')
