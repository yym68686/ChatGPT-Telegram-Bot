import os
import re
import asyncio
import traceback
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.agents import AgentType
from langchain.schema import HumanMessage
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
from langchain.agents import tool
from langchain.memory import ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper


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
        # tools = load_tools(["serpapi", "llm-math"], llm=chatllm)
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

def search_summary(result, model="gpt-3.5-turbo", temperature=0.5):
    search = DuckDuckGoSearchRun()
    webresult = search.run(result) + "`\n\n"

    chatllm = ChatOpenAI(temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=API)
    # 搜索
    tools = load_tools(["ddg-search", "llm-math", "wikipedia"], llm=chatllm)
    agent = initialize_agent(tools + [time], chatllm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=2, early_stopping_method="generate", handle_parsing_errors=True)
    agentresult = agent.run(result)

    summary_prompt = PromptTemplate(
        input_variables=["agentresult", "webresult", "question"],
        template="下面分别是这个问题的网页搜索结果：{agentresult}，{webresult}，请你结合上面搜索结果，挑选相关的内容，总结回答我的问题：{question}，在回答中请不要出现我的问题，如果搜索结果中没有提到相关内容，直接告诉我没有，请不要杜撰、臆断、假设或者给出不准确的回答。回答要求：使用简体中文作答，给出清晰、结构化、详尽的回答，语言严谨且学术化，逻辑清晰，行文流畅。",
    )
    chain = LLMChain(llm=chatllm, prompt=summary_prompt)
    result = chain.run({"agentresult": agentresult, "webresult": webresult, "question": result})
    return result

def getweibo(searchtext, model="gpt-3.5-turbo", temperature=0.5):
    # 加载 OpenAI 模型
    llm = ChatOpenAI(temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=API) 

    # 加载 serpapi 工具
    tools = load_tools(["ddg-search"])

    # 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
    agent = initialize_agent(tools + [time], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    # 运行 agent
    result = agent.run(searchtext)
    return result

if __name__ == "__main__":
    os.system("clear")
    
    # from langchain.agents import get_all_tool_names
    # print(get_all_tool_names())

    # 搜索
    # print(getweibo("今天是几号? 今天微博的热搜话题有哪些？"))
    # print(duckduckgo_search("凡凡还有多久出狱？"))
    # print(search_summary("凡凡还有多久出狱？"))
    print(search_summary("今天微博的热搜话题有哪些？"))

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