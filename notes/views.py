from django.http import HttpResponse
from django.shortcuts import render
import markdown
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'index.html')
