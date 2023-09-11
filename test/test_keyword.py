import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from googlesearch import GoogleSearchAPIWrapper


def getgooglesearchurl(result, numresults=3):
    google_search = GoogleSearchAPIWrapper()
    urls = []
    googleresult = google_search.results(result, numresults)
    urls = [i["link"] for i in googleresult]
    # print("google urls", urls)
    return urls

chainllm = ChatOpenAI(temperature=0.5, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name="gpt-3.5-turbo-16k", openai_api_key=os.environ.get('API', None))
keyword_prompt = PromptTemplate(
    input_variables=["source"],
    # template="*{source}*, ——我想通过网页搜索引擎，获取上述问题的可能答案。请你提取上述问题相关的关键词作为搜索用词(用空格隔开)，直接给我结果(不要多余符号)。",
    template="根据我的问题，总结最少的关键词概括，用空格连接，不要出现其他符号，例如这个问题《How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?》，最小关键词是《zeabur price》，这是我的问题：{source}",
    # template="根据我的问题，仔细想想用什么样的搜索词更有可能搜索到答案，直接给我最好的搜索词，搜索词尽可能少，这是我的问题：{source}",
    # template="请你帮我抽取关键词，输出的关键词之间用空格连接。输出除了关键词，不用解释，也不要出现其他内容，只要出现关键词，必须用空格连接关键词，不要出现其他任何连接符。下面是要提取关键词的文字：{source}",
)
key_chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
result = key_chain.run("How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?")
print(result)
# print(getgooglesearchurl("zeabur price"))
print(getgooglesearchurl(result))