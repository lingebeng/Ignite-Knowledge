from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("index",views.index,name="index"),
    path("main",views.main,name="main"),
    path("edit_note",views.edit_notes,name="edit_notes"),
    path("show_notes/<int:note_id>",views.show_notes,name="show_notes"),
]



