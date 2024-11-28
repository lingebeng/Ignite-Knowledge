from django.urls import path
from . import views

urlpatterns = [
    path("ai_explore",views.ai_explore,name="ai_explore"),
    path("ai_review",views.ai_review,name="ai_review"),
]