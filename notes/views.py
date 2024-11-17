from django.http import HttpResponse
from django.shortcuts import render, redirect
import markdown
from ignite_knowledge import settings
from .models import Notes

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
    md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
    note.content = md.convert(note.content)
    note_toc = md.toc
    # print(note_toc)
    return render(request,"note_content.html",{"note":note,"toc":note_toc})

def manage_notes(request):
    notes = Notes.objects.all()
    return render(request,"manage_note.html",{"notes":notes})

def delete_note(request):
    note_id = request.GET.get('id')
    Notes.objects.filter(id=note_id).delete()
    return redirect("/manage_notes")