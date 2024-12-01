from django.urls import path
from . import views

urlpatterns = [
    path("ai_explore",views.ai_explore,name="ai_explore"),
    path("ai_rag",views.ai_rag,name="ai_rag"),
    path("delete_rag/",views.delete_rag,name="delete_rag"),
    path("edit_rag/",views.edit_rag,name="edit_rag"),
    path("browse_rag/",views.browse_rag,name="browse_rag"),
    path("chat_rag/",views.chat_rag,name="chat_rag"),
]