import time
import markdown
from django.conf import settings
from django.shortcuts import render

from model import Model
prompt = ''
gen_text = ''
with open("config/llm-keys.txt", "r") as f:
    api_keys = f.read()

model = Model(api_keys)

def ai_explore(request):
    global prompt,gen_text

    if request.method == 'POST':
        gen_text = ""
        prompt = request.POST.get('prompt')
        # print(prompt)
        gen_text = model.generate(prompt)
        md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
        gen_text = md.convert(gen_text)

        # print(gen_text)
    return render(request, 'ai_explore.html',{"prompt":prompt,"gen_text":gen_text})



# 放弃流式输出了，不会搞 @linhaifeng
# @require_GET
# def stream_data(request):
#     def data_generator():
#         client = OpenAI(api_key="sk-91aafa6c4d68401c9fecb8245fdcd65d", base_url="https://api.deepseek.com/")
#
#         messages=[
#                 {"role":"system","content":"你是一个知识管理高手"},
#                 {"role":"user","content":"请写一个冒泡排序"},
#             ]
#         response = client.chat.completions.create(
#                 model="deepseek-chat",
#                 messages=messages,
#                 temperature=2,
#                 max_tokens=4096,
#                 stream=True,
#             )
#         for chunk in response:
#             text = chunk.choices[0].delta.content
#             yield text
#
#     response = StreamingHttpResponse(data_generator(), content_type='text/plain')
#     return response