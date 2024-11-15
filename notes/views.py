from django.http import HttpResponse
from django.shortcuts import render
import markdown
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'index.html')

def index1(request):
    return render(request,'index1.html')

def edit_notes(request):
    return render(request, 'edit_notes.html')