from django.db import models
from mdeditor.fields import MDTextField

# Create your models here.

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    content = MDTextField()

