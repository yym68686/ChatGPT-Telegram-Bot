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

from config import BOT_TOKEN, WEB_HOOK, NICK, API, API4, PASS_HISTORY, temperature

# from langchain.agents import get_all_tool_names
# print(get_all_tool_names())

def duckduckgo_search(searchtext, model="gpt-3.5-turbo", temperature=0.5):
    try:
        translate_prompt = PromptTemplate(
            input_variables=["targetlang", "text"],
            template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
        )
        chatllm = ChatOpenAI(temperature=temperature, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name=model, openai_api_key=API)
        
        # 翻译成英文 带聊天模型的链 方法一
        translate_template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text from {sourcelang} to {targetlang}, please do not explain any sentences, just translate or leave them as they are."
        system_message_prompt = SystemMessagePromptTemplate.from_template(translate_template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        zh2enchain = LLMChain(llm=chatllm, prompt=chat_prompt)
        engquestion = zh2enchain.run(sourcelang="Simplified Chinese", targetlang="English", text=searchtext)

        
        # # 翻译成英文 方法二
        # chain = LLMChain(llm=chatllm, prompt=translate_prompt)
        # engquestion = chain.run({"targetlang": "english", "text": searchtext})

        # 搜索
        tools = load_tools(["ddg-search", "llm-math"], llm=chatllm)
        agent = initialize_agent(tools, chatllm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=10, early_stopping_method="generate", handle_parsing_errors=True)
        result = agent.run(engquestion)

        # 翻译成中文
        en2zhchain = LLMChain(llm=chatllm, prompt=translate_prompt)
        result = en2zhchain.run({"targetlang": "Simplified Chinese", "text": result})

        return result
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    os.system("clear")
    print(duckduckgo_search("langchain agent 怎么在失败的时候重新执行"))