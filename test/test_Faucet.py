from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def gptsearch(result, llm):
    response = llm([HumanMessage(content=result)])
    response = response.content
    return response


print(gptsearch("鲁迅和周树人为什么打架", chainllm))