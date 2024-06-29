from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from myshop.forms import RegistrationForm, LoginForm

def register_user(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user')
    return render(
        request=request,
        template_name='user/register.html',
        context={
            'form': form
        }
    )

def login_user(request):
    if request.user.is_authenticated:
        return redirect('__base.html')
    form = LoginForm()
    message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username = username,
                password = password
            )
            if user is not None:
                print('Bạn đã xác thực thành công')
                login(request=request, user=user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET['next'])
                return redirect('index')
            else:
                message = 'Vui lòng kiểm tra lại Username/Password'
    return render(
        request=request,
        template_name='user/login.html',
        context={
            'form': form,
            'message': message
        }
    )

def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(
        request=request,
        template_name='user/change_password.html',
        context={
            'form': form,

        }
    )

# Hàm phía server nhận từ Javascript gửi lên
# JSON gửi từ JS <=> thì server cũng gửi lại JSON

def validate_username(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            User.objects.get(username=username)
            return JsonResponse({'message': f'{username} đã trùng'}, status=409) # 409 Conflict
        except User.DoesNotExist:
            return JsonResponse({'message': 'OK'}, status=200)
