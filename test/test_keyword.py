import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time as record_time
import config
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


if __name__ == "__main__":
    # os.system("clear")
    start_time = record_time.time()

    chainllm = ChatOpenAI(temperature=0.5, openai_api_base=config.bot_api_url.v1_url, model_name=config.GPT_ENGINE, openai_api_key=config.API)
    keyword_prompt = PromptTemplate(
        input_variables=["source"],
        template=(
            "根据我的问题，总结关键词概括问题，输出要求如下："
            "1. 给出三行不同的关键词组合，每行的关键词用空格连接。每行关键词可以是一个或者多个。"
            "2. 至少有一行关键词里面有中文，至少有一行关键词里面有英文。"
            "3. 只要直接给出这三行关键词，不需要其他任何解释，不要出现其他符号和内容。"
            "4. 如果问题有关于日漫，至少有一行关键词里面有日文。"
            "下面是一些根据问题提取关键词的示例："
            "问题 1：How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?"
            "三行关键词是："
            "zeabur price"
            "zeabur documentation"
            "zeabur 价格"
            "问题 2：pplx API 怎么使用？"
            "三行关键词是："
            "pplx API demo"
            "pplx API"
            "pplx API 使用方法"
            "问题 3：以色列哈马斯的最新情况"
            "三行关键词是："
            "以色列 哈马斯 最新情况"
            "Israel Hamas situation"
            "哈马斯 以色列 冲突"
            "问题 4：话说葬送的芙莉莲动漫是半年番还是季番？完结没？"
            "三行关键词是："
            "葬送的芙莉莲"
            "葬送のフリーレン"
            "Frieren: Beyond Journey's End"
            "问题 5：周海媚最近发生了什么"
            "三行关键词是："
            "周海媚"
            "周海媚 事件"
            "Kathy Chau Hoi Mei news"
            "这是我的问题：{source}"
        ),
    )
    key_chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
    # result = key_chain.run("以色列哈马斯的最新情况")
    # result = key_chain.run("今天的微博热搜有哪些？")
    result = key_chain.run("中国最新公布的游戏政策，对游戏行业和其他相关行业有什么样的影响？")
    # result = key_chain.run("鸿蒙是安卓套壳吗？")
    # result = key_chain.run("How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?")
    
    end_time = record_time.time()
    run_time = end_time - start_time

    print(result)
    print("Run time: {}".format(run_time))
    # print(getgooglesearchurl("zeabur price"))
    # for i in result:
    #     print(getgooglesearchurl(i))