import random
import string
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm,LoginForm
from .models import User,ValidCode
from datetime import datetime


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            exist = User.objects.filter(email=email).exists()
            if not exist:
                return redirect('/register')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')

            real_password = User.objects.filter(email=email).first().password
            register_date = User.objects.filter(email=email).first().register_date.strftime("%Y-%m-%d %H:%M:%S")
            if password == real_password:
                if not remember:
                    request.session.set_expiry(0)
                username = User.objects.filter(email=email).first().username
                request.session['info'] = {"username": username,"email": email,"password": password,"register_date":register_date}
                return redirect('/main')
            else:
                form.add_error('email', '邮箱或者密码错误！')
                return render(request, 'login.html', context={"form": form})
        else:
            email = form.cleaned_data.get('email')
            if email is None:
                email = ""
            return render(request, 'login.html', {'form': form,"email":email})

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create(email=email, username=username, password=password)
            return redirect("/login")
        else:
            return render(request, 'register.html', context={"form": form})

def logout(request):
    return redirect("/login")


def send_email(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
    valid_code = "".join(random.sample(string.digits, 4))
    ValidCode.objects.update_or_create(email=email, defaults={'valid_code':valid_code,'create_time':datetime.now()})
    send_mail("Ignite Knowledge 注册验证码",
              message=f"您的注册验证码是：{valid_code}",
              recipient_list=[email],from_email=None)
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})
