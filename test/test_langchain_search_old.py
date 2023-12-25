import os
import re

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from langchain.chat_models import ChatOpenAI


from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

from langchain.document_loaders import UnstructuredPDFLoader

def getmd5(string):
    import hashlib
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    md5_hex = md5_hash.hexdigest()
    return md5_hex

from utils.sitemap import SitemapLoader
async def get_doc_from_sitemap(url):
    # https://www.langchain.asia/modules/indexes/document_loaders/examples/sitemap#%E8%BF%87%E6%BB%A4%E7%AB%99%E7%82%B9%E5%9C%B0%E5%9B%BE-url-
    sitemap_loader = SitemapLoader(web_path=url)
    docs = await sitemap_loader.load()
    return docs

async def get_doc_from_local(docpath, doctype="md"):
    from langchain.document_loaders import DirectoryLoader
    # 加载文件夹中的所有txt类型的文件
    loader = DirectoryLoader(docpath, glob='**/*.' + doctype)
    # 将数据转成 document 对象，每个文件会作为一个 document
    documents = loader.load()
    return documents

system_template="""Use the following pieces of context to answer the users question. 
If you don't know the answer, just say "Hmm..., I'm not sure.", don't try to make up an answer.
ALWAYS return a "Sources" part in your answer.
The "Sources" part should be a reference to the source of the document from which you got your answer.

Example of your response should be:

```
The answer is foo

Sources:
1. abc
2. xyz
```
Begin!
----------------
{summaries}
"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)

def get_chain(store, llm):
    chain_type_kwargs = {"prompt": prompt}
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm, 
        chain_type="stuff", 
        retriever=store.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
        reduce_k_below_max_tokens=True
    )
    return chain

async def docQA(docpath, query_message, persist_db_path="db", model = "gpt-3.5-turbo"):
    chatllm = ChatOpenAI(temperature=0.5, openai_api_base=config.bot_api_url.v1_url, model_name=model, openai_api_key=config.API)
    embeddings = OpenAIEmbeddings(openai_api_base=config.bot_api_url.v1_url, openai_api_key=config.API)

    sitemap = "sitemap.xml"
    match = re.match(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', docpath)
    if match:
        doc_method = get_doc_from_sitemap
        docpath = os.path.join(docpath, sitemap)
    else:
        doc_method = get_doc_from_local

    persist_db_path = getmd5(docpath)
    if not os.path.exists(persist_db_path):
        documents = await doc_method(docpath)
        # 初始化加载器
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=50)
        # 持久化数据
        split_docs = text_splitter.split_documents(documents)
        vector_store = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_db_path)
        vector_store.persist()
    else:
        # 加载数据
        vector_store = Chroma(persist_directory=persist_db_path, embedding_function=embeddings)

    # 创建问答对象
    qa = get_chain(vector_store, chatllm)
    # qa = RetrievalQA.from_chain_type(llm=chatllm, chain_type="stuff", retriever=vector_store.as_retriever(), return_source_documents=True)
    # 进行问答
    result = qa({"question": query_message})
    return result


def persist_emdedding_pdf(docurl, persist_db_path):
    embeddings = OpenAIEmbeddings(openai_api_base=config.bot_api_url.v1_url, openai_api_key=os.environ.get('API', None))
    filename = get_doc_from_url(docurl)
    docpath = os.getcwd() + "/" + filename
    loader = UnstructuredPDFLoader(docpath)
    documents = loader.load()
    # 初始化加载器
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=25)
    # 切割加载的 document
    split_docs = text_splitter.split_documents(documents)
    vector_store = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_db_path)
    vector_store.persist()
    os.remove(docpath)
    return vector_store

async def pdfQA(docurl, docpath, query_message, model="gpt-3.5-turbo"):
    chatllm = ChatOpenAI(temperature=0.5, openai_api_base=config.bot_api_url.v1_url, model_name=model, openai_api_key=os.environ.get('API', None))
    embeddings = OpenAIEmbeddings(openai_api_base=config.bot_api_url.v1_url, openai_api_key=os.environ.get('API', None))
    persist_db_path = getmd5(docpath)
    if not os.path.exists(persist_db_path):
        vector_store = persist_emdedding_pdf(docurl, persist_db_path)
    else:
        vector_store = Chroma(persist_directory=persist_db_path, embedding_function=embeddings)
    qa = RetrievalQA.from_chain_type(llm=chatllm, chain_type="stuff", retriever=vector_store.as_retriever(), return_source_documents=True)
    result = qa({"query": query_message})
    return result['result']


def pdf_search(docurl, query_message, model="gpt-3.5-turbo"):
    chatllm = ChatOpenAI(temperature=0.5, openai_api_base=config.bot_api_url.v1_url, model_name=model, openai_api_key=os.environ.get('API', None))
    embeddings = OpenAIEmbeddings(openai_api_base=config.bot_api_url.v1_url, openai_api_key=os.environ.get('API', None))
    filename = get_doc_from_url(docurl)
    docpath = os.getcwd() + "/" + filename
    loader = UnstructuredPDFLoader(docpath)
    try:
        documents = loader.load()
    except:
        print("pdf load error! docpath:", docpath)
        return ""
    os.remove(docpath)
    # 初始化加载器
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=25)
    # 切割加载的 document
    split_docs = text_splitter.split_documents(documents)
    vector_store = Chroma.from_documents(split_docs, embeddings)
    # 创建问答对象
    qa = RetrievalQA.from_chain_type(llm=chatllm, chain_type="stuff", retriever=vector_store.as_retriever(),return_source_documents=True)
    # 进行问答
    result = qa({"query": query_message})
    return result['result']

def summary_each_url(threads, chainllm, prompt):
    summary_prompt = PromptTemplate(
        input_variables=["web_summary", "question", "language"],
        template=(
            "You need to response the following question: {question}."
            "Your task is answer the above question in {language} based on the Search results provided. Provide a detailed and in-depth response"
            "If there is no relevant content in the search results, just answer None, do not make any explanations."
            "Search results: {web_summary}."
        ),
    )
    summary_threads = []

    for t in threads:
        tmp = t.join()
        print(tmp)
        chain = LLMChain(llm=chainllm, prompt=summary_prompt)
        chain_thread = ThreadWithReturnValue(target=chain.run, args=({"web_summary": tmp, "question": prompt, "language": config.LANGUAGE},))
        chain_thread.start()
        summary_threads.append(chain_thread)

    url_result = ""
    for t in summary_threads:
        tmp = t.join()
        print("summary", tmp)
        if tmp != "None":
            url_result += "\n\n" + tmp
    return url_result

def get_search_results(prompt: str, context_max_tokens: int):

    url_text_list = get_url_text_list(prompt)
    useful_source_text = "\n\n".join(url_text_list)
    # useful_source_text = summary_each_url(threads, chainllm, prompt)

    useful_source_text, search_tokens_len = cut_message(useful_source_text, context_max_tokens)
    print("search tokens len", search_tokens_len, "\n\n")

    return useful_source_text

from typing import Any
from langchain.schema.output import LLMResult
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        # 记得结束后这里置true
        self.finish = False
        self.answer = ""

    def on_llm_new_token(self, token: str, **kwargs):
        # print(token)
        self.tokens.append(token)
        # yield ''.join(self.tokens)
        # print(''.join(self.tokens))

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.finish = 1

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        print(str(error))
        self.tokens.append(str(error))

    def generate_tokens(self):
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                self.answer += data
                yield data
            else:
                pass
        return self.answer