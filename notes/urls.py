from django.urls import path
from . import views
urlpatterns = [
    path("main",views.main,name="main"),
    path("edit_note/",views.edit_notes,name="edit_notes"),
    path("show_notes/<int:note_id>",views.show_notes,name="show_notes"),
    path("manage_notes",views.manage_notes,name="manage_notes"),
    path("delete_note/",views.delete_note,name="delete_note"),
    path("review_note/",views.review_note,name="review_note"),
    path("record",views.add_note,name="record"),
    path("show_answer",views.show_answer,name="show_answer"),

    path("search/",views.search,name="search"),

]




