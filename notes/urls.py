from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("main",views.main,name="main"),
    path("edit_note/",views.edit_notes,name="edit_notes"),
    path("show_notes/<int:note_id>",views.show_notes,name="show_notes"),
    path("manage_notes",views.manage_notes,name="manage_notes"),
    path("delete_note/",views.delete_note,name="delete_note"),
    path("record",views.add_note,name="record"),
]



