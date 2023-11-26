import re
import time
import requests
import os
from bs4 import BeautifulSoup
from langchain.tools import DuckDuckGoSearchResults
def getddgsearchurl(result, numresults=3):
    search = DuckDuckGoSearchResults(num_results=numresults)
    webresult = search.run(result)
    urls = re.findall(r"(https?://\S+)\]", webresult, re.MULTILINE)
    return urls

urls = getddgsearchurl("你知道今天有什么热点新闻吗")
print(urls)

def Web_crawler(url: str) -> str:
    """返回链接网址url正文内容，必须是合法的网址"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    result = ''
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=headers, verify=False, timeout=5, stream=True)
        if response.status_code == 404:
            print("Page not found:", url)
            return ""
        content_length = int(response.headers.get('Content-Length', 0))
        if content_length > 5000000:
            print("Skipping large file:", url)
            return result
        soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
        body = "".join(soup.find('body').get_text().split('\n'))
        result = body
    except Exception as e:
        print('\033[31m')
        print("error url", url)
        print("error", e)
        print('\033[0m')
    return result

start_time = time.time()

for url in urls:
    print(Web_crawler(url))
    print('-----------------------------')
end_time = time.time()
run_time = end_time - start_time
# 打印运行时间
print(f"程序运行时间：{run_time}秒")