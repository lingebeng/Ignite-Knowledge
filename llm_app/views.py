import markdown
from django.conf import settings
from django.shortcuts import render
from model import Model
prompt = ''

with open("config/llm-keys.txt", "r") as f:
    api_keys = f.read()

model = Model(api_keys)

def ai_explore(request):
    global prompt
    gen_text = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        print(prompt)
        gen_text = model.generate(prompt)
        md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
        gen_text = md.convert(gen_text)
    return render(request, 'ai_explore.html',{"prompt":prompt,"gen_text":gen_text})

