import re
from langchain_core.messages import SystemMessage,HumanMessage
import markdown
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from django.conf import settings

# 将markdown转换成html，其中添加了行内latex公式的转换！
def markdown_transfer(content,flag=True):
    md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
    content = md.convert(content)
    """
    @linhaifeng:奇技淫巧使得在markdown中显示latex数学公式，但是没法变颜色，网上的方法不太行！
    """
    if flag:
        all_latex = re.findall("\\$(.*?)\\$", content, re.S)
        for latex in all_latex:
            latex = latex.strip()
            transfer = f"""<div style="background-color:white;text-align:center;border: green solid 1px;""><img src="https://latex.codecogs.com/svg.latex?{latex}"></div>"""
            content = content.replace(latex, transfer)
        content = content.replace("$", '')
        content = re.sub(r'<img', r'<img class="diy-image" ', content)
        toc = md.toc
        return content,toc
    else:
        return content

class Model:
    def __init__(self):
        load_dotenv()
        self.model = ChatOpenAI(model="qwen-plus")

    def invoke(self,message):
        return self.model.invoke(message).content

class RAG:
    def __init__(self,data,model_name):
        load_dotenv()
        self.model = ChatOpenAI(model="qwen-plus")
        self.data = data
        self.embedding_model_name = model_name
        self.embedding_model,self.split_content,self.persist_filename = (
            None,None,None
        )

    def split_chunk(self,chunk_size=250,chunk_overlap=50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        self.split_content = splitter.split_documents(self.data)
        print("--",self.split_content)

    def vector_persist(self,persist_filename):
        self.persist_filename = persist_filename
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.embedding_model_name,model_kwargs=model_kwargs,encode_kwargs=encode_kwargs)
        if self.split_content is None:
            print("Please input some contents")
        else:
            Chroma.from_documents(self.split_content, self.embedding_model, persist_directory=self.persist_filename)

    def knowledge_quiz(self,content):
        db = Chroma(persist_directory=self.persist_filename, embedding_function=self.embedding_model)
        similar_docs = db.similarity_search(content, k=3)
        print(similar_docs)
        summary_prompt = "".join([doc.page_content for doc in similar_docs])
        send_message = (f"下面的信息({summary_prompt})是否有这个问题({content})有关，如果你觉得无关请告诉我无法根据提供的上下文回答'{content}'这个问题，"
                        f"根据你自己之前的知识回答即可，如果回答不出来可以选择不会答，否则请根据{summary_prompt}对{content}的问题进行回答")
        print(send_message)
        messages = [
            SystemMessage(content="您是一个知识的总结与提问者"),
            HumanMessage(content=send_message),
        ]
        answer = self.model.invoke(messages).content

        return answer


