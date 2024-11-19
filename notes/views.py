from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
import markdown
from ignite_knowledge import settings
from .models import Notes

def main(request):
    notes = Notes.objects.all()
    return render(request, 'main.html',{'notes':notes})

def show_notes(request,note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        note = None
    md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
    note.content = md.convert(note.content)
    note_toc = md.toc
    """
    @linhaifeng:奇技淫巧使得在markdown中显示latex数学公式，但是没法变颜色，网上的方法不太行！
    """
    import re
    all_latex = re.findall("\$(.*?)\$", note.content, re.S)
    for latex in all_latex:
        latex = latex.strip()
        transfer = f"""<div style="background-color:white"><img align="center" src="https://latex.codecogs.com/svg.latex?{latex}"></div>"""
        note.content = note.content.replace(latex,transfer)
    note.content = note.content.replace("$", '')
    return render(request,"note_content.html",{"note":note,"toc":note_toc})

def manage_notes(request):
    notes = Notes.objects.all()
    return render(request,"manage_note.html",{"notes":notes})

def delete_note(request):
    note_id = request.GET.get('id')
    Notes.objects.filter(id=note_id).delete()
    return redirect("/manage_notes")



def edit_notes(request):
    note_id = request.GET.get('id')
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        note = None
    if request.method == "GET":
        return render(request, 'edit_notes.html',{"note":note})
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        outline = request.POST.get('outline')
        content_type = request.POST.get('content_type')
        general_type = request.POST.get('general_type')
        from datetime import datetime
        update_date = datetime.now()
        Notes.objects.filter(id=note_id).update(title=title,content=content,outline=outline,content_type=content_type,general_type=general_type,update_date=update_date)
        return redirect("/manage_notes")

def add_note(request):
    if request.method == "GET":
        return render(request, 'add_note.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        outline = request.POST.get('outline')
        content_type = request.POST.get('content_type')
        general_type = request.POST.get('general_type')
        Notes.objects.create(title=title,content=content,outline=outline,content_type=content_type,general_type=general_type)
        return redirect("/manage_notes")