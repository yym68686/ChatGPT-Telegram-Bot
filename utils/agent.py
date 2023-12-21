import os
import re
import json
import base64

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
# import jieba

import asyncio
import tiktoken
import requests
import threading

import urllib.parse
from typing import Any
import time as record_time
from bs4 import BeautifulSoup

from langchain.llms import OpenAI
from langchain.chains import LLMChain, RetrievalQA, RetrievalQAWithSourcesChain
from langchain.agents import AgentType, load_tools, initialize_agent, tool
from langchain.schema import HumanMessage
from langchain.schema.output import LLMResult
from langchain.callbacks.manager import CallbackManager
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults, Tool
from langchain.utilities import WikipediaAPIWrapper
from utils.googlesearch import GoogleSearchAPIWrapper
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

def get_doc_from_url(url):
    filename = urllib.parse.unquote(url.split("/")[-1])
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    return filename

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

def Document_extract(docurl):
    filename = get_doc_from_url(docurl)
    docpath = os.getcwd() + "/" + filename
    if filename[-3:] == "pdf":
        from pdfminer.high_level import extract_text
        text = extract_text(docpath)
    if filename[-3:] == "txt":
        with open(docpath, 'r') as f:
            text = f.read()
    prompt = (
        "Here is the document, inside <document></document> XML tags:"
        "<document>"
        "{}"
        "</document>"
    ).format(text)
    os.remove(docpath)
    return prompt

from typing import Optional, List
from langchain.llms.base import LLM
import g4f
class EducationalLLM(LLM):

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        out = g4f.ChatCompletion.create(
            model=config.GPT_ENGINE,
            messages=[{"role": "user", "content": prompt}],
        )  #
        if stop:
            stop_indexes = (out.find(s) for s in stop if s in out)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                out = out[:min_stop]
        return out

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
    
class ThreadWithReturnValue(threading.Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return

def Web_crawler(url: str, isSearch=False) -> str:
    """返回链接网址url正文内容，必须是合法的网址"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    result = ''
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, verify=False, timeout=3, stream=True)
        if response.status_code == 404:
            print("Page not found:", url)
            return "抱歉，网页不存在，目前无法访问该网页。@Trash@"
        content_length = int(response.headers.get('Content-Length', 0))
        if content_length > 5000000:
            print("Skipping large file:", url)
            return result
        soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
        
        table_contents = ""
        tables = soup.find_all('table')
        for table in tables:
            table_contents += table.get_text()
            table.decompose()
        body = "".join(soup.find('body').get_text().split('\n'))
        result = table_contents + body
        if result == '' and not isSearch:
            result = "抱歉，可能反爬虫策略，目前无法访问该网页。@Trash@"
        if result.count("\"") > 1000:
            result = ""
    except Exception as e:
        print('\033[31m')
        print("error url", url)
        print("error", e)
        print('\033[0m')
    # print("url content", result + "\n\n")
    return result

def getddgsearchurl(result, numresults=4):
    try:
        search = DuckDuckGoSearchResults(num_results=numresults)
        webresult = search.run(result)
        if webresult == None:
            return []
        urls = re.findall(r"(https?://\S+)\]", webresult, re.MULTILINE)
    except Exception as e:
        print('\033[31m')
        print("duckduckgo error", e)
        print('\033[0m')
        urls = []
    # print("ddg urls", urls)
    return urls

def getgooglesearchurl(result, numresults=3):
    google_search = GoogleSearchAPIWrapper()
    urls = []
    try:
        googleresult = google_search.results(result, numresults)
        for i in googleresult:
            if "No good Google Search Result was found" in i or "google.com" in i["link"]:
                continue
            urls.append(i["link"])
    except Exception as e:
        print('\033[31m')
        print("error", e)
        print('\033[0m')
        if "rateLimitExceeded" in str(e):
            print("Google API 每日调用频率已达上限，请明日再试！")
            config.USE_GOOGLE = False
    # print("google urls", urls)
    return urls

def get_search_url(prompt, chainllm):
    urls_set = []
    yield "🌐 正在提取关键词..."
    keyword_prompt = PromptTemplate(
        input_variables=["source"],
        template=(
            "根据我的问题，总结关键词概括问题，输出要求如下："
            "1. 给出三行不同的关键词组合，每行的关键词用空格连接。每行关键词可以是一个或者多个。"
            "2. 至少有一行关键词里面有中文，至少有一行关键词里面有英文。"
            "3. 只要直接给出这三行关键词，不需要其他任何解释，不要出现其他符号和内容。"
            "4. 如果问题有关于日漫，至少有一行关键词里面有日文。"
            "下面是一些根据问题提取关键词的示例："
            "问题 1：How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?"
            "三行关键词是："
            "zeabur price"
            "zeabur documentation"
            "zeabur 价格"
            "问题 2：pplx API 怎么使用？"
            "三行关键词是："
            "pplx API demo"
            "pplx API"
            "pplx API 使用方法"
            "问题 3：以色列哈马斯的最新情况"
            "三行关键词是："
            "以色列 哈马斯 最新情况"
            "Israel Hamas situation"
            "哈马斯 以色列 冲突"
            "问题 4：话说葬送的芙莉莲动漫是半年番还是季番？完结没？"
            "三行关键词是："
            "葬送的芙莉莲"
            "葬送のフリーレン"
            "Frieren: Beyond Journey's End"
            "问题 5：周海媚最近发生了什么"
            "三行关键词是："
            "周海媚"
            "周海媚 事件"
            "Kathy Chau Hoi Mei news"
            "这是我的问题：{source}"
        ),
    )
    key_chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
    keyword_google_search_thread = ThreadWithReturnValue(target=key_chain.run, args=({"source": prompt},))
    keyword_google_search_thread.start()
    keywords = keyword_google_search_thread.join().split('\n')[-3:]
    print("keywords", keywords)
    keywords = [item.replace("三行关键词是：", "") for item in keywords if "\\x" not in item if item != ""]
    print("select keywords", keywords)

    # # seg_list = jieba.cut_for_search(prompt)  # 搜索引擎模式
    # seg_list = jieba.cut(prompt, cut_all=True)
    # result = " ".join(seg_list)
    # keywords = [result] * 3
    # print("keywords", keywords)

    search_threads = []
    urls_set = []
    if len(keywords) == 3:
        search_url_num = 4
    if len(keywords) == 2:
        search_url_num = 6
    if len(keywords) == 1:
        search_url_num = 12
    # print(keywords)
    yield "🌐 正在获取搜索链接🔗..."
    if config.USE_GOOGLE:
        search_thread = ThreadWithReturnValue(target=getgooglesearchurl, args=(keywords[0],search_url_num,))
        search_thread.start()
        search_threads.append(search_thread)
        keywords.pop(0)
    # print(keywords)
    for keyword in keywords:
        search_thread = ThreadWithReturnValue(target=getddgsearchurl, args=(keyword,search_url_num,))
        search_thread.start()
        search_threads.append(search_thread)
    # exit(0)

    for t in search_threads:
        tmp = t.join()
        urls_set += tmp
    url_set_list = sorted(set(urls_set), key=lambda x: urls_set.index(x))
    # cut_num = int(len(url_set_list) * 2 / 3)
    url_pdf_set_list = [item for item in url_set_list if item.endswith(".pdf")]
    url_set_list = [item for item in url_set_list if not item.endswith(".pdf")]
    # return url_set_list[:cut_num], url_pdf_set_list
    return url_set_list, url_pdf_set_list

def concat_url(threads):
    url_result = []
    for t in threads:
        tmp = t.join()
        if tmp:
            url_result.append(tmp)
    return url_result

def summary_each_url(threads, chainllm):
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

def get_url_text_list(prompt):
    start_time = record_time.time()
    yield "🌐 正在搜索，请稍等..."

    if config.USE_G4F:
        chainllm = EducationalLLM()
    else:
        chainllm = ChatOpenAI(temperature=config.temperature, openai_api_base=config.bot_api_url.v1_url, model_name=config.GPT_ENGINE, openai_api_key=config.API)

    url_set_list, url_pdf_set_list = yield from get_search_url(prompt, chainllm)

    yield "🌐 正在获取链接内容🔗..."
    threads = []
    for url in url_set_list:
        url_search_thread = ThreadWithReturnValue(target=Web_crawler, args=(url,True,))
        url_search_thread.start()
        threads.append(url_search_thread)

    url_text_list = concat_url(threads)


    yield "🌐 搜索完成✅，正在整理搜索结果..."
    end_time = record_time.time()
    run_time = end_time - start_time
    print("urls", url_set_list)
    print(f"搜索用时：{run_time}秒")

    return url_text_list

def get_text_token_len(text):
    tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model(config.GPT_ENGINE)
    encode_text = encoding.encode(text)
    return len(encode_text)

def cut_message(message: str, max_tokens: int):
    tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model(config.GPT_ENGINE)
    encode_text = encoding.encode(message)
    if len(encode_text) > max_tokens:
        encode_text = encode_text[:max_tokens]
        message = encoding.decode(encode_text)
    encode_text = encoding.encode(message)
    return message, len(encode_text)

def get_search_results(prompt: str, context_max_tokens: int):

    url_text_list = get_url_text_list(prompt)
    useful_source_text = "\n\n".join(url_text_list)
    # useful_source_text = summary_each_url(threads, chainllm)

    useful_source_text, search_tokens_len = cut_message(useful_source_text, context_max_tokens)
    print("search tokens len", search_tokens_len, "\n\n")

    return useful_source_text

def check_json(json_data):
    while True:
        try:
            json.loads(json_data)
            break
        except json.decoder.JSONDecodeError as e:
            print("JSON error：", e)
            print("JSON body", repr(json_data))
            if "Invalid control character" in str(e):
                json_data = json_data.replace("\n", "\\n")
            if "Unterminated string starting" in str(e):
                json_data += '"}'
    return json_data

def get_date_time_weekday():
    import datetime
    import pytz
    tz = pytz.timezone('Asia/Shanghai')  # 为东八区设置时区
    now = datetime.datetime.now(tz)  # 获取东八区当前时间
    weekday = now.weekday()
    weekday_str = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][weekday]
    return "今天是：" + str(now.date()) + "，现在的时间是：" + str(now.time())[:-7] + "，" + weekday_str

# 使用函数
def get_version_info():
    import subprocess
    current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(['git', '-C', current_directory, 'log', '-1'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    return output

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_encode_image(image_url):
    filename = get_doc_from_url(image_url)
    image_path = os.getcwd() + "/" + filename
    base64_image = encode_image(image_path)
    prompt = f"data:image/jpeg;base64,{base64_image}"
    os.remove(image_path)
    return prompt

if __name__ == "__main__":
    os.system("clear")
    print(get_date_time_weekday())
    # print(get_version_info())
    
    # from langchain.agents import get_all_tool_names
    # print(get_all_tool_names())

    # # 搜索

    # for i in search_web_and_summary("今天的微博热搜有哪些？"):
    # for i in search_web_and_summary("阿里云24核96G的云主机价格是多少"):
    # for i in search_web_and_summary("话说葬送的芙莉莲动漫是半年番还是季番？完结没？"):
    # for i in search_web_and_summary("周海媚事件进展"):
    # for i in search_web_and_summary("macos 13.6 有什么新功能"):
    # for i in search_web_and_summary("用python写个网络爬虫给我"):
    # for i in search_web_and_summary("消失的她主要讲了什么？"):
    # for i in search_web_and_summary("奥巴马的全名是什么？"):
    # for i in search_web_and_summary("华为mate60怎么样？"):
    # for i in search_web_and_summary("慈禧养的猫叫什么名字?"):
    # for i in search_web_and_summary("民进党当初为什么支持柯文哲选台北市长？"):
    # for i in search_web_and_summary("Has the United States won the china US trade war？"):
    # for i in search_web_and_summary("What does 'n+2' mean in Huawei's 'Mate 60 Pro' chipset? Please conduct in-depth analysis."):
    # for i in search_web_and_summary("AUTOMATIC1111 是什么？"):
    # for i in search_web_and_summary("python telegram bot 怎么接收pdf文件"):
    # for i in search_web_and_summary("中国利用外资指标下降了 87% ？真的假的。"):
    # for i in search_web_and_summary("How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?"):
    # for i in search_web_and_summary("英国脱欧没有好处，为什么英国人还是要脱欧？"):
    # for i in search_web_and_summary("2022年俄乌战争为什么发生？"):
    # for i in search_web_and_summary("卡罗尔与星期二讲的啥？"):
    # for i in search_web_and_summary("金砖国家会议有哪些决定？"):
    # for i in search_web_and_summary("iphone15有哪些新功能？"):
    # for i in search_web_and_summary("python函数开头：def time(text: str) -> str:每个部分有什么用？"):
        # print(i, end="")

    # 问答
    # result = asyncio.run(docQA("/Users/yanyuming/Downloads/GitHub/wiki/docs", "ubuntu 版本号怎么看？"))
    # result = asyncio.run(docQA("https://yym68686.top", "说一下HSTL pipeline"))
    # result = asyncio.run(docQA("https://wiki.yym68686.top", "PyTorch to MindSpore翻译思路是什么？"))
    # print(result['answer'])
    # result = asyncio.run(pdfQA("https://api.telegram.org/file/bot5569497961:AAHobhUuydAwD8SPkXZiVFybvZJOmGrST_w/documents/file_1.pdf", "HSTL的pipeline详细讲一下"))
    # print(result)
    # source_url = set([i.metadata['source'] for i in result["source_documents"]])
    # source_url = "\n".join(source_url)
    # message = (
    #     f"{result['result']}\n\n"
    #     f"参考链接：\n"
    #     f"{source_url}"
    # )
    # print(message)