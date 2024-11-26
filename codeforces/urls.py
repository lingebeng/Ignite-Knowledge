from django.urls import path
from . import views

urlpatterns = [
    path("coding", views.coding, name="coding"),
    path("exec_code", views.exec_code, name="exec_code"),
    path("codeforces/<int:problem_id>", views.codeforces, name="codeforces"),
    path("judge_result", views.judge_result, name="judge_result"),
    path("check_result", views.check_result, name="check_result"),

    path("manage_problems", views.manage_problems, name="manage_problems"),
    path("delete_problem/", views.delete_problem, name="delete_problem"),
    path("add_problem", views.add_problem, name="add_problem"),
    path("edit_problem/", views.edit_problem, name="edit_problem"),
]
