from django.db import models

class User(models.Model):
    """
    User(用户名，邮箱，密码，注册日期)
    """
    username = models.CharField(max_length=40)
    email = models.EmailField(max_length=40,unique=True)
    password = models.CharField(max_length=16)
    register_date = models.DateTimeField(auto_now_add=True)

class ValidCode(models.Model):
    """
    ValidCode(邮箱，验证码，创建日期)
    """
    email = models.EmailField(unique=True)
    valid_code = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now_add=True)