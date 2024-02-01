import os
import re
import json
import base64
import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils.prompt import search_key_word_prompt
# import jieba

import asyncio
import tiktoken
import requests
import threading

import urllib.parse
import time as record_time
from bs4 import BeautifulSoup


from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchResults
from langchain.chains import LLMChain

# from typing import Optional, List
# from langchain.llms.base import LLM
# import g4f
# class EducationalLLM(LLM):

#     @property
#     def _llm_type(self) -> str:
#         return "custom"

#     def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
#         out = g4f.ChatCompletion.create(
#             model=config.GPT_ENGINE,
#             messages=[{"role": "user", "content": prompt}],
#         )  #
#         if stop:
#             stop_indexes = (out.find(s) for s in stop if s in out)
#             min_stop = min(stop_indexes, default=-1)
#             if min_stop > -1:
#                 out = out[:min_stop]
#         return out

class ThreadWithReturnValue(threading.Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return

def Web_crawler(url: str, isSearch=False) -> str:
    """返回链接网址url正文内容，必须是合法的网址"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    result = ''
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, verify=False, timeout=3, stream=True)
        if response.status_code == 404:
            print("Page not found:", url)
            return ""
            # return "抱歉，网页不存在，目前无法访问该网页。@Trash@"
        content_length = int(response.headers.get('Content-Length', 0))
        if content_length > 5000000:
            print("Skipping large file:", url)
            return result
        soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')

        table_contents = ""
        tables = soup.find_all('table')
        for table in tables:
            table_contents += table.get_text()
            table.decompose()
        body = "".join(soup.find('body').get_text().split('\n'))
        result = table_contents + body
        if result == '' and not isSearch:
            result = ""
            # result = "抱歉，可能反爬虫策略，目前无法访问该网页。@Trash@"
        if result.count("\"") > 1000:
            result = ""
    except Exception as e:
        print('\033[31m')
        print("error url", url)
        print("error", e)
        print('\033[0m')
    # print("url content", result + "\n\n")
    return result

def getddgsearchurl(result, numresults=4):
    try:
        search = DuckDuckGoSearchResults(num_results=numresults)
        webresult = search.run(result)
        # print("ddgwebresult", webresult)
        if webresult == None:
            return []
        urls = re.findall(r"(https?://\S+)\]", webresult, re.MULTILINE)
    except Exception as e:
        print('\033[31m')
        print("duckduckgo error", e)
        print('\033[0m')
        urls = []
    # print("ddg urls", urls)
    return urls

from utils.googlesearch import GoogleSearchAPIWrapper
def getgooglesearchurl(result, numresults=3):
    google_search = GoogleSearchAPIWrapper()
    urls = []
    try:
        googleresult = google_search.results(result, numresults)
        # print("googleresult", googleresult)
        for i in googleresult:
            if "No good Google Search Result was found" in i or "google.com" in i["link"]:
                continue
            urls.append(i["link"])
    except Exception as e:
        print('\033[31m')
        print("error", e)
        print('\033[0m')
        if "rateLimitExceeded" in str(e):
            print("Google API 每日调用频率已达上限，请明日再试！")
            config.USE_GOOGLE = False
    # print("google urls", urls)
    return urls

def sort_by_time(urls):
    def extract_date(url):
        match = re.search(r'[12]\d{3}.\d{1,2}.\d{1,2}', url)
        if match is not None:
            match = re.sub(r'([12]\d{3}).(\d{1,2}).(\d{1,2})', "\\1/\\2/\\3", match.group())
            print(match)
            if int(match[:4]) > datetime.datetime.now().year:
                match = "1000/01/01"
        else:
            match = "1000/01/01"
        try:
            return datetime.datetime.strptime(match, '%Y/%m/%d')
        except:
            match = "1000/01/01"
            return datetime.datetime.strptime(match, '%Y/%m/%d')

    # 提取日期并创建一个包含日期和URL的元组列表
    date_url_pairs = [(extract_date(url), url) for url in urls]

    # 按日期排序
    date_url_pairs.sort(key=lambda x: x[0], reverse=True)

    # 获取排序后的URL列表
    sorted_urls = [url for _, url in date_url_pairs]

    return sorted_urls

def get_search_url(prompt, chainllm):
    urls_set = []

    keyword_prompt = PromptTemplate(
        input_variables=["source"],
        template=search_key_word_prompt,
    )
    key_chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
    keyword_google_search_thread = ThreadWithReturnValue(target=key_chain.run, args=({"source": prompt},))
    keyword_google_search_thread.start()
    keywords = keyword_google_search_thread.join().split('\n')[-3:]
    print("keywords", keywords)
    keywords = [item.replace("三行关键词是：", "") for item in keywords if "\\x" not in item if item != ""]

    keywords = [prompt] + keywords
    keywords = keywords[:3]
    # if len(keywords) == 1:
    #     keywords = keywords * 3
    print("select keywords", keywords)

    # # seg_list = jieba.cut_for_search(prompt)  # 搜索引擎模式
    # seg_list = jieba.cut(prompt, cut_all=True)
    # result = " ".join(seg_list)
    # keywords = [result] * 3
    # print("keywords", keywords)

    search_threads = []
    urls_set = []
    if len(keywords) == 3:
        search_url_num = 4
    if len(keywords) == 2:
        search_url_num = 6
    if len(keywords) == 1:
        search_url_num = 12
    # print(keywords)
    # yield "🌐 正在网上挑选最相关的信息源，请稍候..."
    if config.USE_GOOGLE:
        search_thread = ThreadWithReturnValue(target=getgooglesearchurl, args=(keywords[0],search_url_num,))
        search_thread.start()
        search_threads.append(search_thread)
        keywords.pop(0)
    # print(keywords)
    for keyword in keywords:
        search_thread = ThreadWithReturnValue(target=getddgsearchurl, args=(keyword,search_url_num,))
        search_thread.start()
        search_threads.append(search_thread)
    # exit(0)

    for t in search_threads:
        tmp = t.join()
        urls_set += tmp
    url_set_list = sorted(set(urls_set), key=lambda x: urls_set.index(x))
    url_set_list = sort_by_time(url_set_list)

    url_pdf_set_list = [item for item in url_set_list if item.endswith(".pdf")]
    url_set_list = [item for item in url_set_list if not item.endswith(".pdf")]
    # cut_num = int(len(url_set_list) * 1 / 3)
    return url_set_list[:6], url_pdf_set_list
    # return url_set_list, url_pdf_set_list

def concat_url(threads):
    url_result = []
    for t in threads:
        tmp = t.join()
        if tmp:
            url_result.append(tmp)
    return url_result

def cut_message(message: str, max_tokens: int):
    tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model(config.GPT_ENGINE)
    encode_text = encoding.encode(message)
    if len(encode_text) > max_tokens:
        encode_text = encode_text[:max_tokens]
        message = encoding.decode(encode_text)
    encode_text = encoding.encode(message)
    return message, len(encode_text)

def get_url_text_list(prompt):
    start_time = record_time.time()
    # yield "🌐 正在搜索您的问题，提取关键词..."

    # if config.PLUGINS["USE_G4F"]:
    #     chainllm = EducationalLLM()
    # else:
    #     chainllm = ChatOpenAI(temperature=config.temperature, openai_api_base=config.bot_api_url.v1_url, model_name=config.GPT_ENGINE, openai_api_key=config.API)
    chainllm = ChatOpenAI(temperature=config.temperature, openai_api_base=config.bot_api_url.v1_url, model_name=config.GPT_ENGINE, openai_api_key=config.API)

    url_set_list, url_pdf_set_list = get_search_url(prompt, chainllm)
    # url_set_list, url_pdf_set_list = yield from get_search_url(prompt, chainllm)

    # yield "🌐 已找到一些有用的链接，正在获取详细内容..."
    threads = []
    for url in url_set_list:
        url_search_thread = ThreadWithReturnValue(target=Web_crawler, args=(url,True,))
        url_search_thread.start()
        threads.append(url_search_thread)

    url_text_list = concat_url(threads)
    # print("url_text_list", url_text_list)


    # yield "🌐 快完成了✅，正在为您整理搜索结果..."
    end_time = record_time.time()
    run_time = end_time - start_time
    print("urls", url_set_list)
    print(f"搜索用时：{run_time}秒")

    return url_text_list

# Plugins 搜索
def get_search_results(prompt: str):

    url_text_list = get_url_text_list(prompt)
    useful_source_text = "\n\n".join(url_text_list)

    # useful_source_text, search_tokens_len = cut_message(useful_source_text, context_max_tokens)
    # print("search tokens len", search_tokens_len, "\n\n")

    return useful_source_text

# Plugins 获取日期时间
def get_date_time_weekday():
    import datetime
    import pytz
    tz = pytz.timezone('Asia/Shanghai')  # 为东八区设置时区
    now = datetime.datetime.now(tz)  # 获取东八区当前时间
    weekday = now.weekday()
    weekday_str = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][weekday]
    return "今天是：" + str(now.date()) + "，现在的时间是：" + str(now.time())[:-7] + "，" + weekday_str

# Plugins 使用函数
def get_version_info():
    import subprocess
    current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(['git', '-C', current_directory, 'log', '-1'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    return output



# 公用函数
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_doc_from_url(url):
    filename = urllib.parse.unquote(url.split("/")[-1])
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    return filename

def get_encode_image(image_url):
    filename = get_doc_from_url(image_url)
    image_path = os.getcwd() + "/" + filename
    base64_image = encode_image(image_path)
    prompt = f"data:image/jpeg;base64,{base64_image}"
    os.remove(image_path)
    return prompt

def get_text_token_len(text):
    tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model(config.GPT_ENGINE)
    encode_text = encoding.encode(text)
    return len(encode_text)

def Document_extract(docurl):
    filename = get_doc_from_url(docurl)
    docpath = os.getcwd() + "/" + filename
    if filename[-3:] == "pdf":
        from pdfminer.high_level import extract_text
        text = extract_text(docpath)
    if filename[-3:] == "txt":
        with open(docpath, 'r') as f:
            text = f.read()
    prompt = (
        "Here is the document, inside <document></document> XML tags:"
        "<document>"
        "{}"
        "</document>"
    ).format(text)
    os.remove(docpath)
    return prompt

def check_json(json_data):
    while True:
        try:
            json.loads(json_data)
            break
        except json.decoder.JSONDecodeError as e:
            print("JSON error：", e)
            print("JSON body", repr(json_data))
            if "Invalid control character" in str(e):
                json_data = json_data.replace("\n", "\\n")
            if "Unterminated string starting" in str(e):
                json_data += '"}'
            if "Expecting ',' delimiter" in str(e):
                json_data += '}'
            if "Expecting value: line 1 column 1" in str(e):
                json_data = '{"prompt": ' + json.dumps(json_data) + '}'
    return json_data

if __name__ == "__main__":
    os.system("clear")
    print(get_date_time_weekday())
    # print(get_version_info())
    print(get_search_results("今天的微博热搜有哪些？", 1000))

    # from langchain.agents import get_all_tool_names
    # print(get_all_tool_names())

    # # 搜索

    # for i in search_web_and_summary("今天的微博热搜有哪些？"):
    # for i in search_web_and_summary("给出清华铊中毒案时间线，并作出你的评论。"):
    # for i in search_web_and_summary("红警hbk08是谁"):
    # for i in search_web_and_summary("国务院 2024 放假安排"):
    # for i in search_web_and_summary("中国最新公布的游戏政策，对游戏行业和其他相关行业有什么样的影响？"):
    # for i in search_web_and_summary("今天上海的天气怎么样？"):
    # for i in search_web_and_summary("阿里云24核96G的云主机价格是多少"):
    # for i in search_web_and_summary("话说葬送的芙莉莲动漫是半年番还是季番？完结没？"):
    # for i in search_web_and_summary("周海媚事件进展"):
    # for i in search_web_and_summary("macos 13.6 有什么新功能"):
    # for i in search_web_and_summary("用python写个网络爬虫给我"):
    # for i in search_web_and_summary("消失的她主要讲了什么？"):
    # for i in search_web_and_summary("奥巴马的全名是什么？"):
    # for i in search_web_and_summary("华为mate60怎么样？"):
    # for i in search_web_and_summary("慈禧养的猫叫什么名字?"):
    # for i in search_web_and_summary("民进党当初为什么支持柯文哲选台北市长？"):
    # for i in search_web_and_summary("Has the United States won the china US trade war？"):
    # for i in search_web_and_summary("What does 'n+2' mean in Huawei's 'Mate 60 Pro' chipset? Please conduct in-depth analysis."):
    # for i in search_web_and_summary("AUTOMATIC1111 是什么？"):
    # for i in search_web_and_summary("python telegram bot 怎么接收pdf文件"):
    # for i in search_web_and_summary("中国利用外资指标下降了 87% ？真的假的。"):
    # for i in search_web_and_summary("How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?"):
    # for i in search_web_and_summary("英国脱欧没有好处，为什么英国人还是要脱欧？"):
    # for i in search_web_and_summary("2022年俄乌战争为什么发生？"):
    # for i in search_web_and_summary("卡罗尔与星期二讲的啥？"):
    # for i in search_web_and_summary("金砖国家会议有哪些决定？"):
    # for i in search_web_and_summary("iphone15有哪些新功能？"):
    # for i in search_web_and_summary("python函数开头：def time(text: str) -> str:每个部分有什么用？"):
        # print(i, end="")

    # 问答
    # result = asyncio.run(docQA("/Users/yanyuming/Downloads/GitHub/wiki/docs", "ubuntu 版本号怎么看？"))
    # result = asyncio.run(docQA("https://yym68686.top", "说一下HSTL pipeline"))
    # result = asyncio.run(docQA("https://wiki.yym68686.top", "PyTorch to MindSpore翻译思路是什么？"))
    # print(result['answer'])
    # result = asyncio.run(pdfQA("https://api.telegram.org/file/bot5569497961:AAHobhUuydAwD8SPkXZiVFybvZJOmGrST_w/documents/file_1.pdf", "HSTL的pipeline详细讲一下"))
    # print(result)
    # source_url = set([i.metadata['source'] for i in result["source_documents"]])
    # source_url = "\n".join(source_url)
    # message = (
    #     f"{result['result']}\n\n"
    #     f"参考链接：\n"
    #     f"{source_url}"
    # )
    # print(message)