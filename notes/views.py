from django.http import HttpResponse
from django.shortcuts import render
import markdown

from ignite_knowledge import settings
from .models import Notes

def index(request):
    return render(request,'index.html')

def main(request):
    notes = Notes.objects.all()
    return render(request, 'main.html',{'notes':notes})

def edit_notes(request):
    return render(request, 'edit_notes.html')


def show_notes(request,note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        note = None
    html = markdown.markdown(note.content,extensions=settings.MARKDOWN_EXTENSIONS)
    return render(request,"note_content.html",{"note":note,"content":html})

