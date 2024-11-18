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

class NoteModelForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['general_type',"content","outline"]


def edit_notes(request):
    note_id = request.GET.get('id')
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        note = None

    if request.method == "GET":
        return render(request, 'edit_notes.html',{"note":note})
    else:
        content = request.POST.get('content')
        Notes.objects.filter(id=note_id).update(content=content)
        return redirect("/manage_notes")

def add_note(request):
    form = NoteModelForm()
    return render(request,"add_note.html",{"note":None,"form":form})