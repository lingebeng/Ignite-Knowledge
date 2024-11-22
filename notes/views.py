from django.http import JsonResponse
from django.shortcuts import render, redirect
import markdown
from django.views.decorators.csrf import csrf_exempt
import re
from ignite_knowledge import settings
from .models import Notes
from django.conf import settings
import subprocess as sp

language,code,input_data,output_data = (
    '','','',''
)
# @linhaifeng 屏蔽 CSRF
@csrf_exempt
def exec_code(request):
    global language, code, input_data,output_data
    if request.method == 'POST':
        language = request.POST['language']
        code = request.POST['code']
        input_data = request.POST['input_data']
        code_exec = settings.EXEC_CODE
        in_file = code_exec / 'tmp.in'
        out_file = code_exec / 'tmp.out'


        if language == 'python':
            exec_file = code_exec / "tmp.py"
            with open(exec_file, 'w') as f:
                f.write(code)

            with open(in_file, 'w') as f:
                f.write(input_data)

            process = sp.run(f"python {exec_file} < {in_file} > {out_file}", shell=True,stderr=sp.PIPE)
            error = process.stderr.decode()
            if error == "":
                with open(out_file, 'r') as f:
                    output_data = f.read()
            else:
                pattern = "/home/lhf/program/Django/Ignite-Knowledge/static/code_exec/tmp.py"
                output_data = re.sub(pattern,"tmp.py",error)
                print(output_data)



        elif language == 'text/x-c++src':
            exec_file = code_exec / "tmp.c"
            with open(code_exec / "tmp.c", 'w') as f:
                f.write(code)

            with open(in_file, 'w') as f:
                f.write(input_data)

            process = sp.run(f"gcc {exec_file} -o tmp && ./tmp < {in_file} > {out_file}", shell=True,stderr=sp.PIPE)

            error = process.stderr.decode()
            if error == "":
                with open(out_file, 'r') as f:
                    output_data = f.read()
            else:
                pattern = "/home/lhf/program/Django/Ignite-Knowledge/static/code_exec/tmp.c"
                output_data = re.sub(pattern, "tmp.c", error)

        return JsonResponse({'status': 'success', 'message': 'Form submitted successfully', "data": {
            "output_data": output_data
        }})

def coding(request):
    global language,code,input_data,output_data

    return render(request,"coding.html",{'language':language,'code':code,'input_data':input_data,'output_data':output_data})

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
    all_latex = re.findall("\$(.*?)\$", note.content, re.S)
    for latex in all_latex:
        latex = latex.strip()
        transfer = f"""<div style="background-color:white"><img align="center" src="https://latex.codecogs.com/svg.latex?{latex}"></div>"""
        note.content = note.content.replace(latex,transfer)
    content = note.content.replace("$", '')

    note.content = re.sub(r'<img', r'<img class="diy-image" ', content)
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