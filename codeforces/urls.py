from django.urls import path
from . import views

urlpatterns = [
    path("coding", views.coding, name="coding"),
    path("exec_code", views.exec_code, name="exec_code"),
    path("codeforces/<int:problem_id>", views.codeforces, name="codeforces"),
    path("judge_result", views.judge_result, name="judge_result"),
    path("check_result", views.check_result, name="check_result"),
]
