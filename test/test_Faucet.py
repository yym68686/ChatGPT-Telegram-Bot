from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def gptsearch(result, llm):
    response = llm([HumanMessage(content=result)])
    response = response.content
    return response

chainllm = ChatOpenAI(temperature=0.5, openai_api_base="https://openkey.cloud/v1", model_name="gpt-3.5-turbo", openai_api_key="sk-ucUnnmqI9DdtsAXG8OKxOFxD5dnSrU3E3ZQh4PJa1dgQ7KzE")
# chainllm = ChatOpenAI(temperature=0.5, openai_api_base="https://openkey.cloud/v1", model_name="gpt-4-1106-preview", openai_api_key="sk-ucUnnmqI9DdtsAXG8OKxOFxD5dnSrU3E3ZQh4PJa1dgQ7KzE")
# chainllm = ChatOpenAI(temperature=0.5, openai_api_base="https://openkey.cloud/v1", model_name="gpt-4", openai_api_key="sk-ucUnnmqI9DdtsAXG8OKxOFxD5dnSrU3E3ZQh4PJa1dgQ7KzE")

print(gptsearch("鲁迅和周树人为什么打架", chainllm))