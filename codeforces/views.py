from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CodeForces
from django.conf import settings
import subprocess as sp
from ignite_knowledge.utils import markdown_transfer
from datetime import datetime

language,code,input_data,output_data = (
    '','','',''
)

def coding(request):
    global language,code,input_data,output_data

    return render(request,"coding.html",{'language':language,'code':code,'input_data':input_data,'output_data':output_data})

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
                pattern = "tmp.py"
                idx = error.find(pattern)
                output_data = error[idx + len(pattern) + 2:].strip()

        elif language == 'text/x-c++src':
            exec_file = code_exec / "tmp.cpp"
            with open(code_exec / "tmp.cpp", 'w') as f:
                f.write(code)

            with open(in_file, 'w') as f:
                f.write(input_data)

            process = sp.run(f"g++ {exec_file} -o tmp && ./tmp < {in_file} > {out_file}", shell=True,stderr=sp.PIPE)

            error = process.stderr.decode()
            if error == "":
                with open(out_file, 'r') as f:
                    output_data = f.read()
            else:
                pattern = "tmp.cpp"
                idx = error.find(pattern)
                if idx == -1:
                    output_data = error
                else:
                    idx = error.find(pattern,idx + len(pattern))
                    output_data = error[idx + len(pattern) + 1:]

        elif language == 'text/x-csrc':
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
                pattern = "tmp.c"
                print(error)
                idx = error.find(pattern)
                idx1 = error.find(pattern,idx + len(pattern))
                if idx1 != -1:
                    idx = idx1
                output_data = error[idx + len(pattern) + 1:]

        elif language == 'text/x-java':
            exec_file = code_exec / "Main.java"
            with open(code_exec / "Main.java", 'w') as f:
                f.write(code)

            with open(in_file, 'w') as f:
                f.write(input_data)

            process = sp.run(f"javac {exec_file}  && java -cp {code_exec} Main < {in_file} > {out_file}", shell=True, stderr=sp.PIPE)
            error = process.stderr.decode()
            if error == "":
                with open(out_file, 'r') as f:
                    output_data = f.read()
            else:
                pattern = "Main.java"
                idx = error.find(pattern)
                output_data = error[idx:]

        return JsonResponse({'status': 'success', 'message': 'Form submitted successfully', "data": {
            "output_data": output_data
        }})

def codeforces(request,problem_id):
    try:
        problem = CodeForces.objects.get(pk=problem_id)
    except CodeForces.DoesNotExist:
        problem = None

    example_input = problem.example_input
    problem.example_input = "input\n```python\n" + problem.example_input + "\n```\n"
    problem.example_output = "output\n```python\n" + problem.example_output + "\n```\n"
    problem.content = problem.content + "\n\n---\n"
    problem.content,_ = markdown_transfer(problem.content)
    problem.example_input = markdown_transfer(problem.example_input,False)
    problem.example_output = markdown_transfer(problem.example_output,False)

    return render(request,"codeforces.html",{"problem":problem,"example_input":example_input})

@csrf_exempt
def judge_result(request):
    global language, code
    problem_id = request.POST["id"]

    try:
        problem = CodeForces.objects.get(pk=problem_id)
    except CodeForces.DoesNotExist:
        problem = None
    test_input,test_output = problem.test_input,problem.test_output
    code_exec = settings.EXEC_CODE

    out_file = code_exec / 'tmp.out'
    in_file = code_exec / 'tmp.in'
    with open(in_file, 'w') as f:
        f.write(test_input)
    code = request.POST["code"]
    language = request.POST["language"]
    if language == 'python':
        exec_file = code_exec / "tmp.py"
        with open(exec_file, 'w') as f:
            f.write(code)

        sp.run(f"python {exec_file} < {in_file} > {out_file}", shell=True, stderr=sp.PIPE)

    elif language == 'text/x-c++src':
        exec_file = code_exec / "tmp.cpp"
        with open(code_exec / "tmp.cpp", 'w') as f:
            f.write(code)

        sp.run(f"g++ {exec_file} -o tmp && ./tmp < {in_file} > {out_file}", shell=True, stderr=sp.PIPE)


    elif language == 'text/x-csrc':
        exec_file = code_exec / "tmp.c"
        with open(code_exec / "tmp.c", 'w') as f:
            f.write(code)

        sp.run(f"gcc {exec_file} -o tmp && ./tmp < {in_file} > {out_file}", shell=True, stderr=sp.PIPE)



    elif language == 'text/x-java':
        exec_file = code_exec / "Main.java"
        with open(code_exec / "Main.java", 'w') as f:
            f.write(code)

        sp.run(f"javac {exec_file}  && java -cp {code_exec} Main < {in_file} > {out_file}", shell=True,
                         stderr=sp.PIPE)

    with open(out_file, 'r') as f:
        result = f.read()

    flag = True
    for x,y in zip(result.split('\n'),test_output.split('\n')):

        x = x.strip().replace("'",'"').replace(" ","")
        y = y.strip().replace("'",'"').replace(" ","")
        if x != y:
            flag = False
            break
    if flag:
        return JsonResponse('''<h1 style="color: green;text-align: center;">AC</h1>''', safe=False)
    else:
        return JsonResponse('''<h1 style="color: red;text-align: center;">WA</h1>''', safe=False)
@csrf_exempt
def check_result(request):
    problem_id = request.POST["id"]
    check_code = CodeForces.objects.get(pk=problem_id).code
    remarks = CodeForces.objects.get(pk=problem_id).remarks

    answer = check_code + "\n\n---\n" + remarks
    answer = markdown_transfer(answer,False)

    return JsonResponse(answer, safe=False)

def manage_problems(request):
    problem_set = CodeForces.objects.filter(author=request.session['info']['username']).all()
    return render(request,"manage_problems.html",{"problem_set":problem_set})


def delete_problem(request):
    problem_id = request.GET.get('id')
    CodeForces.objects.filter(id=problem_id).delete()
    return redirect("/codeforces/manage_problems")

def add_problem(request):
    if request.method == "GET":
        return render(request, 'add_problem.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        algorithm_type = request.POST.get('algorithm_type')
        example_input = request.POST.get('example_input')
        example_output = request.POST.get('example_output')
        test_input = request.POST.get('test_input')
        test_output = request.POST.get('test_output')
        remarks = request.POST.get('remarks')
        code = request.POST.get('code')
        update_date = datetime.now()
        CodeForces.objects.create(author=request.session['info']['username'],title=title,content=content,algorithm_type=algorithm_type,example_input=example_input,example_output=example_output,test_input= test_input,test_output=test_output,remarks=remarks,code=code,update_date=update_date)
        return redirect("/codeforces/manage_problems")

def edit_problem(request):
    problem_id = request.GET.get('id')
    try:
        problem = CodeForces.objects.get(pk=problem_id)
    except CodeForces.DoesNotExist:
        problem = None

    if request.method == "GET":
        return render(request, 'edit_problem.html', {"problem": problem})

    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        algorithm_type = request.POST.get('algorithm_type')
        example_input = request.POST.get('example_input')
        example_output = request.POST.get('example_output')
        test_input = request.POST.get('test_input')
        test_output = request.POST.get('test_output')
        remarks = request.POST.get('remarks')
        code = request.POST.get('code')
        from datetime import datetime
        update_date = datetime.now()
        CodeForces.objects.filter(id=problem_id).update(title=title,content=content,algorithm_type=algorithm_type,example_input=example_input,example_output=example_output,test_input= test_input,test_output=test_output,remarks=remarks,code=code,update_date=update_date)
        return redirect("/codeforces/manage_problems")


