import os
import shutil
import markdown
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .models import RAGVector
from django.shortcuts import render, redirect
from ignite_knowledge.utils import Model,markdown_transfer
from django.conf import settings
from datetime import datetime
prompt = ''
gen_text = ''


def ai_explore(request):
    global prompt,gen_text
    model = Model()
    if request.method == 'POST':
        gen_text = ""
        prompt = request.POST.get('prompt')
        gen_text = model.invoke(prompt)
        md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
        gen_text = md.convert(gen_text)

        # print(gen_text)
    return render(request, 'ai_explore.html',{"prompt":prompt,"gen_text":gen_text})


def ai_rag(request):
    rag_vector = RAGVector.objects.filter(author=request.session['info']['username']).all()
    if request.method == 'POST':
        file = request.FILES['file']
        data = file.read().decode('utf-8')
        file_name = str(settings.VECTOR_FILE / file.name)
        prefix,suffix = file.name.split('.')[-2:]
        with open(file_name,'w') as f:
            f.write(data)
        loader = UnstructuredMarkdownLoader(file_name)
        data = loader.load()
        embedding_model = str(settings.EMBEDDING_ROOT)
        vector_folder = str(settings.VECTOR_ROOT / prefix)
        chunk_size = 250
        chunk_overlap = 30

        test_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        splits = test_splitter.split_documents(data)
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model, model_kwargs=model_kwargs,
                                           encode_kwargs=encode_kwargs)
        Chroma.from_documents(splits, embeddings, persist_directory=vector_folder)

        RAGVector.objects.create(author=request.session['info']['username'],name=prefix,content_type="Nothing",update_date=datetime.now(),suffix=suffix)
        return redirect("/llm/ai_rag")
    return render(request, 'ai_rag.html',{"rag_vector":rag_vector})



def delete_rag(request):
    rag_id = request.GET.get('id')
    name = RAGVector.objects.filter(id=rag_id).first().name
    suffix = RAGVector.objects.filter(id=rag_id).first().suffix
    filename = name + '.' + suffix
    RAGVector.objects.filter(id=rag_id).delete()
    try:
        os.remove(settings.VECTOR_FILE / filename)
        shutil.rmtree(settings.VECTOR_ROOT / name)
    except:
        pass
    return redirect("/llm/ai_rag")

def edit_rag(request):
    rag_id = request.GET.get('id')
    try:
        rag = RAGVector.objects.get(pk=rag_id)
    except RAGVector.DoesNotExist:
        rag = None
    pre_name = rag.name
    suffix = rag.suffix
    pre_filename = pre_name + '.' + suffix
    if request.method == "GET":
        return render(request, 'edit_rag.html', {"rag": rag})
    else:
        name = request.POST.get('name')
        filename = name + '.' + suffix
        content_type = request.POST.get('content_type')
        update_date = datetime.now()
        os.rename(settings.VECTOR_ROOT / pre_name, settings.VECTOR_ROOT / name)
        os.rename(settings.VECTOR_FILE / pre_filename, settings.VECTOR_FILE / filename)
        RAGVector.objects.filter(id=rag_id).update(name=name, content_type=content_type,update_date=update_date)
        return redirect("/llm/ai_rag")

def browse_rag(request):
    rag_id = request.GET.get('id')
    rag = RAGVector.objects.get(pk=rag_id)
    filename = str(settings.VECTOR_FILE / rag.name) + '.' + rag.suffix
    with open(filename,'r') as f:
        content = f.read()
    content,toc = markdown_transfer(content)
    return render(request, "note_content.html", {"content": content, "toc": toc})

def chat_rag(request):
    rag_id = request.GET.get('id')
    rag = RAGVector.objects.get(pk=rag_id)

    model_name = str(settings.EMBEDDING_ROOT)
    vector_folder = str(settings.VECTOR_ROOT / rag.name)
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

    db = Chroma(persist_directory=vector_folder,embedding_function=embeddings)
    model = Model()
    question,answer = '',''
    if request.method == 'POST':
        question = request.POST.get('prompt')
        try:
            similarDocs = db.similarity_search(question, k=3)
            summary_prompt = "".join([doc.page_content for doc in similarDocs])

            send_message = f"下面的信息({summary_prompt})是否有这个问题({question})有关，如果你觉得无关请告诉我无法根据提供的上下文回答'{question}'这个问题，简要回答即可，否则请根据{summary_prompt}对{question}的问题进行回答"
            answer = model.invoke(send_message)
            answer = markdown_transfer(answer,False)
        except:
            answer = "<h1>这个问题超纲了，俺不太会！</h1><hr> <h1 style='margin-top:200px'>请换一个俺会的哈！</h1><hr>"
    return render(request, 'ai_explore.html', {"prompt": question, "gen_text": answer})
