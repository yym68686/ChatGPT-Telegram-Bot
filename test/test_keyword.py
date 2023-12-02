import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from utils.googlesearch import GoogleSearchAPIWrapper


def getgooglesearchurl(result, numresults=1):
    google_search = GoogleSearchAPIWrapper()
    urls = []
    googleresult = google_search.results(result, numresults)
    for i in googleresult:
        if "No good Google Search Result was found" in i:
            continue
        urls.append(i["link"])
    return urls

chainllm = ChatOpenAI(temperature=0.5, openai_api_base=os.environ.get('API_URL', None).split("chat")[0], model_name="gpt-3.5-turbo-1106", openai_api_key=os.environ.get('API', None))
# keyword_prompt = PromptTemplate(
#     input_variables=["source"],
#     # template="*{source}*, ——我想通过网页搜索引擎，获取上述问题的可能答案。请你提取上述问题相关的关键词作为搜索用词(用空格隔开)，直接给我结果(不要多余符号)。",
#     template="根据我的问题，总结最少的关键词概括，用空格连接，不要出现其他符号，例如这个问题《How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?》，最小关键词是《zeabur price》，这是我的问题：{source}",
#     # template="根据我的问题，仔细想想用什么样的搜索词更有可能搜索到答案，直接给我最好的搜索词，搜索词尽可能少，这是我的问题：{source}",
#     # template="请你帮我抽取关键词，输出的关键词之间用空格连接。输出除了关键词，不用解释，也不要出现其他内容，只要出现关键词，必须用空格连接关键词，不要出现其他任何连接符。下面是要提取关键词的文字：{source}",
# )

keyword_prompt = PromptTemplate(
    input_variables=["source"],
    template=(
        "根据我的问题，总结最少的关键词概括，给出三行不同的关键词组合，每行的关键词用空格连接，至少有一行关键词里面有中文，至少有一行关键词里面有英文。只要直接给出这三行关键词，不需要其他任何解释，不要出现其他符号。"
        "下面是示例："
        "问题1：How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?"
        "三行关键词是："
        "zeabur price"
        "zeabur documentation"
        "zeabur 价格"
        "问题2：pplx API 怎么使用？"
        "三行关键词是："
        "pplx API demo"
        "pplx API"
        "pplx API 使用方法"
        "问题3：以色列哈马斯的最新情况"
        "三行关键词是："
        "以色列 哈马斯 最新情况"
        "Israel Hamas situation"
        "哈马斯 以色列 冲突"
        "这是我的问题：{source}"
    ),
)
key_chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
result = key_chain.run("以色列哈马斯的最新情况").split('\n')
# result = key_chain.run("今天的微博热搜有哪些？").split('\n')
# result = key_chain.run("鸿蒙是安卓套壳吗？")
# result = key_chain.run("How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?")
print(result)
# print(getgooglesearchurl("zeabur price"))
for i in result:
    print(getgooglesearchurl(i))