from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("index",views.index,name="index"),
    path("index1",views.index1,name="index1"),
    path("edit_note",views.edit_notes,name="edit_notes"),
]



