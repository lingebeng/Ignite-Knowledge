import random
import string
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from .models import User,ValidCode
from datetime import datetime

# Create your views here.


def login(request):
    return render(request, 'login.html')


def send_email(request):
    # 1626732574
    email = "1371675203@qq.com"
    if not email:
        return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
    valid_code = "".join(random.sample(string.digits, 4))
    ValidCode.objects.update_or_create(email=email, defaults={'valid_code':valid_code,'create_time':datetime.now()})
    send_mail("Ignite Knowledge 注册验证码",
              message=f"您的注册验证码是：{valid_code}",
              recipient_list=[email],from_email=None)
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})


