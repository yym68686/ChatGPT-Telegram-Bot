import os
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


from config import BOT_TOKEN, WEB_HOOK, NICK, API, API4, PASS_HISTORY, temperature

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

from langchain.document_loaders.sitemap import SitemapLoader
def getsitemap(url):
    # https://www.langchain.asia/modules/indexes/document_loaders/examples/sitemap#%E8%BF%87%E6%BB%A4%E7%AB%99%E7%82%B9%E5%9C%B0%E5%9B%BE-url-
    sitemap_loader = SitemapLoader(web_path=url)
    
    docs = sitemap_loader.load()
    return docs
 

if __name__ == "__main__":
    os.system("clear")
    
    # from langchain.agents import get_all_tool_names
    # print(get_all_tool_names())

    # print(getweibo("今天是几号? 今天微博的热搜话题有哪些？"))
    print(duckduckgo_search("凡凡还有多久出狱？"))
    # print(getsitemap("https://yym68686.top/sitemap.xml"))