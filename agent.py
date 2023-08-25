import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.agents import AgentType
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent

from config import BOT_TOKEN, WEB_HOOK, NICK, API, API4, PASS_HISTORY, temperature


# from langchain.agents import get_all_tool_names
# print(get_all_tool_names())

def duckduckgo_search(searchtext, model="gpt-3.5-turbo", temperature=0):
    llm = ChatOpenAI(temperature=temperature, openai_api_base='https://api.ohmygpt.com/v1/', model_name=model, openai_api_key=API)
    tools = load_tools(["ddg-search", "llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    result = agent.run(searchtext)

    en2zh_prompt = PromptTemplate(
        input_variables=["targetlang", "text"],
        template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
    )
    chain = LLMChain(llm=llm, prompt=en2zh_prompt)
    return chain.run({"targetlang": "simplified chinese", "text": result})

if __name__ == "__main__":
    os.system("clear")
    print(duckduckgo_search("夏威夷火灾死了多少人？"))