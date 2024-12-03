from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from llm_app.models import RAGVector
from codeforces.models import CodeForces
from .models import Notes
from ignite_knowledge.utils import markdown_transfer, Model

model = Model()
language, code, input_data, output_data = (
    '', '', '', ''
)
q1, a1 = '', ''
q2, a2 = '', ''
q3, a3 = '', ''
summary = ''


# @linhaifeng 屏蔽 CSRF
def main(request):
    notes = Notes.objects.all()
    return render(request, 'main.html', {'notes': notes})


def show_notes(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        note = None
    note.content, note_toc = markdown_transfer(note.content)

    return render(request, "note_content.html", {"title":note.title,"content": note.content, "toc": note_toc})


def manage_notes(request):
    notes = Notes.objects.filter(author=request.session['info']['username']).all()
    return render(request, "manage_note.html", {"notes": notes})


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
        # print(note.content)
        return render(request, 'edit_notes.html', {"note": note})
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        outline = request.POST.get('outline')
        content_type = request.POST.get('content_type')
        general_type = request.POST.get('general_type')
        from datetime import datetime
        update_date = datetime.now()
        Notes.objects.filter(id=note_id).update(title=title, content=content, outline=outline,
                                                content_type=content_type, general_type=general_type,
                                                update_date=update_date)
        return redirect("/manage_notes")


def add_note(request):
    if request.method == "GET":
        return render(request, 'add_note.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        # print(f"content:{content}")
        outline = request.POST.get('outline')
        content_type = request.POST.get('content_type')
        general_type = request.POST.get('general_type')
        from datetime import datetime
        update_date = datetime.now()
        Notes.objects.create(author=request.session['info']['username'],title=title, content=content, outline=outline, content_type=content_type,
                             general_type=general_type, update_date=update_date)
        return redirect("/manage_notes")


def review_note(request):
    global q1, a1, q2, a2, q3, a3, summary
    q1, a1, q2, a2, q3, a3, summary = (
        '', '', '', '', '', '', ''
    )
    note_id = request.GET.get('id')
    note = Notes.objects.get(pk=note_id)
    question_template = ("#### 问题一\n问题描述:....\n\n  \n答案要点:....  \n---\n  "
                         "#### 问题二\n问题描述:....\n\n  \n答案要点:....  \n---\n  "
                         "#### 问题三\n问题描述:....\n\n  \n答案要点:....  \n---\n  ")

    prompt = (f"您是一个善于学习知识的人，您可以对知识进行系统的总结，并善于利用费曼学习法，"
              f"请对以下内容({note.content})进行总结，并提出三个问题来检验自己的学习成果"
              f"问题的模板如下({question_template})")

    answer = model.invoke(prompt)
    try:
        questions = answer.split("### 问题")
        summary = markdown_transfer('\n'.join(questions[0].split('\n')[:-2]), False)
        query = []

        for question in questions[1:4]:
            Q = ""
            A = ""
            flag = 0
            for line in question.split("\n")[1:]:
                if "问题描述" in line:
                    Q = line
                    flag = 1
                elif "答案要点" in line:
                    A = line
                    flag = 2
                else:
                    if flag == 1:
                        Q += line
                    elif flag == 2:
                        A += line
            Q = markdown_transfer(Q, False)
            A = markdown_transfer(A, False)
            query.append((Q, A))
        # print(query)
        q1, a1 = query[0]
        q2, a2 = query[1]
        q3, a3 = query[2]
        return render(request, 'review_note.html', {"summary": summary, "q1": q1, "q2": q2, "q3": q3})
    except:
        import traceback
        traceback.print_exc()
        return render(request, 'review_note.html', {"summary": summary, "q1": q1, "q2": q2, "q3": q3})


@csrf_exempt
def show_answer(request):
    global a1, a2, a3
    return JsonResponse({"data": {
        "answer1": a1,
        "answer2": a2,
        "answer3": a3,
    }})


@require_GET
def search(request):
    query = request.GET.get('query')
    if query.startswith("code"):
        query = query[5:]
        problem_set = CodeForces.objects.filter(author=request.session["info"]["username"]).filter(Q(title__icontains=query) | Q(algorithm_type__icontains=query)).all()
        return render(request, "manage_problems.html", {"problem_set": problem_set})
    elif query.startswith("rag"):
        query = query[4:]
        rag_vector = RAGVector.objects.filter(author=request.session['info']['username']).filter(Q(name__icontains=query) | Q(content_type__icontains=query)).all()
        return render(request, 'ai_rag.html', {"rag_vector": rag_vector})
    else:
        notes = Notes.objects.filter(author=request.session["info"]["username"]).filter(Q(outline__icontains=query)).all()
        return render(request, 'main.html', {'notes': notes})