import os
import re
import asyncio
import threading
import traceback
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.agents import AgentType
from langchain.schema import HumanMessage
from langchain.callbacks.manager import CallbackManager
from langchain.schema.output import LLMResult
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from datetime import date
from typing import Any
from langchain.agents import tool
from langchain.memory import ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain.utilities import WikipediaAPIWrapper
from googlesearch import GoogleSearchAPIWrapper
from langchain.tools import Tool


from langchain.chains import RetrievalQA


from config import BOT_TOKEN, WEB_HOOK, NICK, API, API4, PASS_HISTORY, temperature


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
    chatllm = ChatOpenAI(temperature=0.5, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=API)
    embeddings = OpenAIEmbeddings(openai_api_base=os.environ.get('API_URL', None).split("chat")[0], openai_api_key=API)

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

def duckduckgo_search(result, model="gpt-3.5-turbo", temperature=0.5):
    try:
        translate_prompt = PromptTemplate(
            input_variables=["targetlang", "text"],
            template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
        )
        chatllm = ChatOpenAI(temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=API)
        
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

def ddgsearch(result):
    search = DuckDuckGoSearchResults(num_results=7)
    webresult = search.run(result)
    matches = re.findall(r"\[snippet:\s(.*?),\stitle", webresult, re.MULTILINE)
    return '\n\n'.join(matches)

def googlesearch(result):
    # google_search = GoogleSearchAPIWrapper()
    # googleresult = google_search.results(result, 10)
    google_search = GoogleSearchAPIWrapper(k=5)
    googleresult = google_search.run(result)
    return googleresult

class ThreadWithReturnValue(threading.Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return

def search_summary(result, model="gpt-3.5-turbo", temperature=0.5):

    google_search_thread = ThreadWithReturnValue(target=googlesearch, args=(result,))
    google_search_thread.start()
    search_thread = ThreadWithReturnValue(target=ddgsearch, args=(result,))
    search_thread.start()

    chainStreamHandler = ChainStreamHandler()
    chatllm = ChatOpenAI(streaming=True, callback_manager=CallbackManager([chainStreamHandler]), temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=API)
    chainllm = ChatOpenAI(temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=API)

    keyword_prompt = PromptTemplate(
        input_variables=["source"],
        template="请你帮我抽取关键词，输出的关键词之间用空格连接。输出除了关键词，不用解释，也不要出现其他内容，只要出现关键词，必须用空间连接关键词，不要出现其他任何连接符。下面是要提取关键词的文字：{source}，",
    )
    chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
    keyword_google_search_thread = ThreadWithReturnValue(target=chain.run, args=({"source": result},))
    keyword_google_search_thread.start()


    translate_prompt = PromptTemplate(
        input_variables=["targetlang", "text"],
        template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
    )
    chain = LLMChain(llm=chainllm, prompt=translate_prompt)
    engresult = chain.run({"targetlang": "english", "text": result})

    en_google_search_thread = ThreadWithReturnValue(target=googlesearch, args=(engresult,))
    en_google_search_thread.start()

    en_ddg_search_thread = ThreadWithReturnValue(target=ddgsearch, args=(engresult,))
    en_ddg_search_thread.start()

    keyword = keyword_google_search_thread.join()
    keyword_ans = googlesearch(keyword)

    ans_google = google_search_thread.join()
    ans_ddg = search_thread.join()
    enans_google = en_google_search_thread.join()
    engans_ddg = en_ddg_search_thread.join()
    useful_source_text = ans_ddg  + "\n" + keyword_ans + "\n" + ans_google + "\n" + engans_ddg + "\n" + enans_google

    # Judgment_prompt = PromptTemplate(
    #     input_variables=["sourcetext", "question"],
    #     template="下面分别是一段材料：{sourcetext}，请你结合上述材料，判断是否可以解答“{question}”这个问题，如果能够解答{question}这个问题请回答True，如果不能解答{question}这个问题相关请回答False，回答中只能出现True或者Flase，不能出现其他任何内容。",
    # )
    # Judgment_chain_result = Judgment_chain.run({"sourcetext": webresult, "question": result})
    # print("已找到相关内容！" if Judgment_chain_result == "True" else "未找到相关内容！")

    # tools = load_tools(["ddg-search", "llm-math", "wikipedia"], llm=chatllm)
    # agent = initialize_agent(tools + [time], chatllm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=2, early_stopping_method="generate", handle_parsing_errors=True)
    # for i in range(5):
    #     agentresult = agent.run(result)
    #     useful_source_text = agentresult + "\n" + useful_source_text

    summary_prompt = PromptTemplate(
        input_variables=["useful_source_text", "question"],
        template="下面是这个问题的网页搜索结果：{useful_source_text}，请你结合上面搜索结果，忽略重复的和与问题无关的内容，挑选跟我的问题{question}相关的内容，总结并回答我的问题：{question}，在回答中请不要重复出现我的问题，如果搜索结果中没有提到相关内容，直接告诉我没有，请不要杜撰、臆断、假设或者给出不准确的回答。回答要求：使用简体中文作答，不要出现繁体文字，不要有重复冗余的内容，给出清晰、结构化、在不有重复冗余的基础上，给出详尽丰富的回答，不要忽略细节，语言严谨且学术化，逻辑清晰，行文流畅。",
    )

    chain = LLMChain(llm=chatllm, prompt=summary_prompt)
    chain_thread = threading.Thread(target=chain.run, kwargs={"useful_source_text": useful_source_text, "question": result})
    chain_thread.start()
    return chainStreamHandler.generate_tokens()

if __name__ == "__main__":
    os.system("clear")
    
    # from langchain.agents import get_all_tool_names
    # print(get_all_tool_names())

    # 搜索
    # print(duckduckgo_search("凡凡还有多久出狱？"))
    # print(search_summary("凡凡还有多久出狱？"))
    # print(search_summary("今天微博的热搜话题有哪些？"))
    for i in search_summary("yym68686 是谁？"):
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