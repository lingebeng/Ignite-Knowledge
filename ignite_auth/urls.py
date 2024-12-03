from django.urls import path
from . import views

urlpatterns = [
    path("login",views.login,name="login"),
    path("register",views.register,name="register"),
    path("logout",views.logout,name="logout"),
    path("send_email/",views.send_email,name="send_email"),
]