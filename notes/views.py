from django.shortcuts import render, redirect
from .models import Notes
from ignite_knowledge.utils import markdown_transfer

language,code,input_data,output_data = (
    '','','',''
)
# @linhaifeng 屏蔽 CSRF

def main(request):
    notes = Notes.objects.all()
    return render(request, 'main.html',{'notes':notes})

def show_notes(request,note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        note = None
    note.content,note_toc = markdown_transfer(note.content)

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
        print(note.content)
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
        print(f"content:{content}")
        outline = request.POST.get('outline')
        content_type = request.POST.get('content_type')
        general_type = request.POST.get('general_type')
        from datetime import datetime
        update_date = datetime.now()
        Notes.objects.create(title=title,content=content,outline=outline,content_type=content_type,general_type=general_type,update_date=update_date)
        return redirect("/manage_notes")

