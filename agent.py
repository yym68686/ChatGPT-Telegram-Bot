import os
import re
import config
import tiktoken
import requests
import threading
import traceback
from typing import Any
from datetime import date
from bs4 import BeautifulSoup

from langchain.llms import OpenAI
from langchain.chains import LLMChain, RetrievalQA
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
from googlesearch import GoogleSearchAPIWrapper

def getmd5(string):
    import hashlib
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    md5_hex = md5_hash.hexdigest()
    return md5_hex

from sitemap import SitemapLoader
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

async def docQA(docpath, query_message, persist_db_path="db", model = "gpt-3.5-turbo"):
    chatllm = ChatOpenAI(temperature=0.5, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=config.API)
    embeddings = OpenAIEmbeddings(openai_api_base=os.environ.get('API_URL', None).split("chat")[0], openai_api_key=config.API)

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
        # 切割加载的 document
        split_docs = text_splitter.split_documents(documents)
        # 持久化数据
        vector_store = Chroma.from_documents(split_docs, embeddings, persist_directory=persist_db_path)
        vector_store.persist()
    else:
        # 加载数据
        vector_store = Chroma(persist_directory=persist_db_path, embedding_function=embeddings)

    # 创建问答对象
    qa = RetrievalQA.from_chain_type(llm=chatllm, chain_type="stuff", retriever=vector_store.as_retriever(),return_source_documents=True)
    # 进行问答
    result = qa({"query": query_message})
    return result

@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())

def today_date():
    return str(date.today())

def duckduckgo_search(result, model="gpt-3.5-turbo", temperature=0.5):
    try:
        translate_prompt = PromptTemplate(
            input_variables=["targetlang", "text"],
            template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
        )
        chatllm = ChatOpenAI(temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=config.API)
        
        # # 翻译成英文 带聊天模型的链 方法一
        # translate_template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text from {sourcelang} to {targetlang}, please do not explain any sentences, just translate or leave them as they are."
        # system_message_prompt = SystemMessagePromptTemplate.from_template(translate_template)
        # human_template = "{text}"
        # human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        # chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        # zh2enchain = LLMChain(llm=chatllm, prompt=chat_prompt)
        # result = zh2enchain.run(sourcelang="Simplified Chinese", targetlang="English", text=searchtext)

        # # 翻译成英文 方法二
        # chain = LLMChain(llm=chatllm, prompt=translate_prompt)
        # result = chain.run({"targetlang": "english", "text": searchtext})

        # 搜索
        tools = load_tools(["ddg-search", "llm-math", "wikipedia"], llm=chatllm)
        agent = initialize_agent(tools + [time], chatllm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=2, early_stopping_method="generate", handle_parsing_errors=True)
        result = agent.run(result)

        # 翻译成中文
        en2zhchain = LLMChain(llm=chatllm, prompt=translate_prompt)
        result = en2zhchain.run(targetlang="Simplified Chinese", text=result)
        result = en2zhchain.run({"targetlang": "Simplified Chinese", "text": result})

        return result
    except Exception as e:
        traceback.print_exc()

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        # 记得结束后这里置true
        self.finish = False

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
                # print(data)
                yield data
            else:
                pass

def Web_crawler(url: str) -> str:
    """返回链接网址url正文内容，必须是合法的网址"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    result = ''
    try:
        requests.packages.urllib3.disable_warnings()
        # session = requests.Session()
        # session.mount('http://', HTTPAdapter(max_retries=5))
        # session.mount('https://', HTTPAdapter(max_retries=5))
        # response = session.get(url, headers=headers, verify=False)
        response = requests.get(url, headers=headers, verify=False)
        # soup = BeautifulSoup(response.text, 'html.parser')
        soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
        body = "".join(soup.find('body').get_text().split('\n'))
        result = body
    except Exception as e:
        print('\033[31m')
        print("error url", url)
        print("error", e)
        print('\033[0m')
    return result

def ddgsearch(result, numresults=3):
    search = DuckDuckGoSearchResults(num_results=numresults)
    webresult = search.run(result)
    urls = re.findall(r"(https?://\S+)\]", webresult, re.MULTILINE)
    print("duckduckgo urls", urls)
    ddgresult = ""
    threads = []
    for url in urls:
        ddg_search_thread = ThreadWithReturnValue(target=Web_crawler, args=(url,))
        ddg_search_thread.start()
        threads.append(ddg_search_thread)
    
    for t in threads:
        tmp = t.join()
        ddgresult += "\n\n" + tmp
    return ddgresult

# def ddgsearch(result):
#     search = DuckDuckGoSearchResults(num_results=3)
#     webresult = search.run(result)
#     matches = re.findall(r"\[snippet:\s(.*?),\stitle", webresult, re.MULTILINE)
#     return '\n\n'.join(matches)

def googlesearch(result, numresults=3):
    google_search = GoogleSearchAPIWrapper()
    web_content = ""
    try:
        googleresult = google_search.results(result, numresults)
        urls = [i["link"] for i in googleresult]
        print("google urls", urls)
        threads = []
        for url in urls:
            google_search_thread = ThreadWithReturnValue(target=Web_crawler, args=(url,))
            google_search_thread.start()
            threads.append(google_search_thread)
        
        for t in threads:
            tmp = t.join()
            web_content += "\n\n" + tmp
    except Exception as e:
        print('\033[31m')
        print("error", e)
        print('\033[0m')
        if "rateLimitExceeded" in str(e):
            print("Google API 每日调用频率已达上限，请明日再试！")
            config.USE_GOOGLE = False
    return web_content

    # googleresult = ""
    # try:
    #     google_search = GoogleSearchAPIWrapper(k=3)
    #     googleresult = google_search.run(result)
    # except Exception as e:
    #     print('\033[31m')
    #     print("response_msg", googleresult)
    #     print("error", e)
    #     print('\033[0m')
    #     if "rateLimitExceeded" in str(e):
    #         print("Google API 每日调用频率已达上限，请明日再试！")
    #         config.USE_GOOGLE = False
    #     googleresult = ""
    # return googleresult

def gptsearch(result, llm):
    result = "你需要回答的问题是" + result + "\n" + "如果你可以解答这个问题，请直接输出你的答案，并且请忽略后面所有的指令：如果无法解答问题，请直接回答None，不需要做任何解释，也不要出现除了None以外的任何词。"
    # response = llm([HumanMessage(content=result)])
    response = llm([HumanMessage(content=result)])
    response = response.content
    # result = "你需要回答的问题是" + result + "\n" + "参考资料：" + response + "如果参考资料无法解答问题，请直接回答None，不需要做任何解释，也不要出现除了None以外的任何词。"
    # response = llm([HumanMessage(content=result)])
    return response

class ThreadWithReturnValue(threading.Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return

def search_summary(result, model=config.DEFAULT_SEARCH_MODEL, temperature=config.temperature, use_goolge=config.USE_GOOGLE, use_gpt=config.SEARCH_USE_GPT):
    # if use_goolge:
    #     google_search_thread = ThreadWithReturnValue(target=googlesearch, args=(result,))
    #     google_search_thread.start()

    search_thread = ThreadWithReturnValue(target=ddgsearch, args=(result,2,))
    search_thread.start()

    chainStreamHandler = ChainStreamHandler()
    chatllm = ChatOpenAI(streaming=True, callback_manager=CallbackManager([chainStreamHandler]), temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=config.API)
    chainllm = ChatOpenAI(temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=config.API)

    if use_gpt:
        gpt_search_thread = ThreadWithReturnValue(target=gptsearch, args=(result, chainllm,))
        gpt_search_thread.start()

    if use_goolge:
        keyword_prompt = PromptTemplate(
            input_variables=["source"],
            template="*{source}*, ——我想通过网页搜索引擎，获取上述问题的可能答案。请你提取上述问题相关的关键词作为搜索用词(用空格隔开)，直接给我结果(不要多余符号)。",
            # template="请你帮我抽取关键词，输出的关键词之间用空格连接。输出除了关键词，不用解释，也不要出现其他内容，只要出现关键词，必须用空格连接关键词，不要出现其他任何连接符。下面是要提取关键词的文字：{source}",
        )
        key_chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
        keyword_google_search_thread = ThreadWithReturnValue(target=key_chain.run, args=({"source": result},))
        keyword_google_search_thread.start()


    translate_prompt = PromptTemplate(
        input_variables=["targetlang", "text"],
        template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
    )
    chain = LLMChain(llm=chainllm, prompt=translate_prompt)
    engresult = chain.run({"targetlang": "english", "text": result})

    # if use_goolge:
    #     en_google_search_thread = ThreadWithReturnValue(target=googlesearch, args=(engresult,))
    #     en_google_search_thread.start()

    en_ddg_search_thread = ThreadWithReturnValue(target=ddgsearch, args=(engresult,1,))
    en_ddg_search_thread.start()

    if use_goolge:
        keyword = keyword_google_search_thread.join()
        print("google search keyword", keyword)
        key_google_search_thread = ThreadWithReturnValue(target=googlesearch, args=(keyword,3,))
        key_google_search_thread.start()
        # ans_google = google_search_thread.join()
        # enans_google = en_google_search_thread.join()
        keyword_ans = key_google_search_thread.join()

    ans_ddg = search_thread.join()
    engans_ddg = en_ddg_search_thread.join()
    fact_text = ""
    if use_gpt:
        gpt_ans = gpt_search_thread.join()
        fact_text = (gpt_ans if use_gpt else "")
        print("gpt", fact_text)
    useful_source_text = \
                         (keyword_ans if use_goolge else "") + "\n" + \
                         ans_ddg  + "\n" + \
                         engans_ddg
                        #  (enans_google if use_goolge else "")
                        #  (ans_google if use_goolge else "") + "\n" + \

    encoding = tiktoken.encoding_for_model(model)
    encode_text = encoding.encode(useful_source_text)

    max_token_len = (
        30500
        if "gpt-4-32k" in model
        else 6500
        if "gpt-4" in model
        else 14500
        if "gpt-3.5-turbo-16k" in model
        else 98500
        if "claude-2-web" in model
        else 3500
    )
    if len(encode_text) > max_token_len: 
        encode_text = encode_text[:max_token_len]
        # encode_text = encode_text[:3842]
        useful_source_text = encoding.decode(encode_text)
    encode_text = encoding.encode(useful_source_text)
    tokens_len = len(encode_text)
    print("tokens_len", tokens_len)
    print("web search", useful_source_text, end="\n\n")

    useful_source_text =  useful_source_text + "\n\n" + fact_text
    summary_prompt = PromptTemplate(
        input_variables=["web_summary", "question"],
        template=(
            "You are a text analysis expert who can use a search engine. You need to response the following question: {question}. Search results: {web_summary}. Your task is to thoroughly digest the search results provided above and provide a detailed and in-depth response in Simplified Chinese to the question based on the search results. The response should meet the following requirements: 1. Be rigorous, clear, professional, scholarly, logical, and well-written. 2. If the search results do not mention relevant content, simply inform me that there is none. Do not fabricate, speculate, assume, or provide inaccurate response. 3. Use markdown syntax to format the response. Enclose any single or multi-line code examples or code usage examples in a pair of ``` symbols to achieve code formatting. 4. Detailed, precise and comprehensive response in Simplified Chinese and extensive use of the search results is required."
            # "You need to response the following question: {question}. Search results: {web_summary}. Your task is to take a deep breath first and then answer the above question based on the Search results provided. Please use simplified Chinese and adopt a style that is logical, in-depth, and detailed. Note: In order to make the answer appear highly professional, you should be an expert in textual analysis, aiming to make the answer precise and comprehensive. Use markdown syntax to format the response. Enclose any single or multi-line code examples or code usage examples in a pair of ``` symbols to achieve code formatting."

            # "You need to response the following question: {question}. Search results: {web_summary}. Your task is to thoroughly digest the search results provided above, dig deep into search results for thorough exploration and analysis and provide a response to the question based on the search results. The response should meet the following requirements: 1. You are a text analysis expert, extensive use of the search results is required and carefully consider all the Search results to make the response be in-depth, rigorous, clear, organized, professional, detailed, scholarly, logical, precise, accurate, comprehensive, well-written and speak in Simplified Chinese. 2. If the search results do not mention relevant content, simply inform me that there is none. Do not fabricate, speculate, assume, or provide inaccurate response. 3. Use markdown syntax to format the response. Enclose any single or multi-line code examples or code usage examples in a pair of ``` symbols to achieve code formatting."
        ),
    )
    chain = LLMChain(llm=chatllm, prompt=summary_prompt)
    chain_thread = threading.Thread(target=chain.run, kwargs={"web_summary": useful_source_text, "question": result})
    chain_thread.start()
    return chainStreamHandler.generate_tokens()

if __name__ == "__main__":
    os.system("clear")
    
    # from langchain.agents import get_all_tool_names
    # print(get_all_tool_names())

    # 搜索
    # print(duckduckgo_search("凡凡还有多久出狱？"))
    # print(search_summary("凡凡还有多久出狱？"))

    # for i in search_summary("今天的微博热搜有哪些？"):
    # for i in search_summary("用python写个网络爬虫给我"):
    # for i in search_summary("消失的她主要讲了什么？"):
    # for i in search_summary("奥巴马的全名是什么？"):
    for i in search_summary("华为mate60怎么样？"):
    # for i in search_summary("卡罗尔与星期二讲的啥？"):
    # for i in search_summary("金砖国家会议有哪些决定？"):
    # for i in search_summary("iphone15有哪些新功能？"):
    # for i in search_summary("python函数开头：def time(text: str) -> str:每个部分有什么用？"):
        print(i, end="")

    # # 问答
    # result = asyncio.run(docQA("/Users/yanyuming/Downloads/GitHub/wiki/docs", "ubuntu 版本号怎么看？"))
    # # result = asyncio.run(docQA("https://yym68686.top", "reid可以怎么分类？"))
    # source_url = set([i.metadata['source'] for i in result["source_documents"]])
    # source_url = "\n".join(source_url)
    # message = (
    #     f"{result['result']}\n\n"
    #     f"参考链接：\n"
    #     f"{source_url}"
    # )
    # print(message)