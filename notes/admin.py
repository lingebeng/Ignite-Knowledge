from django.contrib import admin
from . import models

# Register your models here.

# class MyModelAdmin(admin.ModelAdmin):
#     list_display = ('name', 'content')
#     search_fields = ('name','content')

admin.site.register(models.TestModel)