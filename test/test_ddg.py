import re
import time
import requests
import json
import os
from bs4 import BeautifulSoup
from langchain.tools import DuckDuckGoSearchResults
from duckduckgo_search import DDGS
def getddgsearchurl1(result, numresults=3):
    requrl = f"https://html.duckduckgo.com/html?q={result}&kl=us-en&s=0&dc=0"
    try:
        response = requests.get(requrl)
        soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
        print(soup)
        urls = []
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            urls.append(link.get('href'))
        urls = urls[:numresults]
    except Exception as e:
        print('\033[31m')
        print("duckduckgo error", e)
        print('\033[0m')
        urls = []
    return urls

def search_duckduckgo(query):
    url = 'https://duckduckgo.com/html/'
    params = {
        'q': query,
        'ia': 'web'
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    for link in soup.find_all('a', class_='result__url'):
        print(link.get('href'))



from duckduckgo_search import DDGS

def getddg(result, numresults=3):
    with DDGS(timeout=2) as ddgs:
        results = [r["href"] for r in ddgs.text(result, max_results=numresults)]
        # print(json.dumps(results, ensure_ascii=False, indent=4))
        return results

def getddgsearchurl(result, numresults=3):
    try:
        # webresult = getddg(result, numresults)
        search = DuckDuckGoSearchResults(num_results=numresults)
        webresult = search.run(result)
        print(webresult)
        if webresult == None:
            return []
        urls = re.findall(r"(https?://\S+)\]", webresult, re.MULTILINE)
    except Exception as e:
        print('\033[31m')
        print("duckduckgo error", e)
        print('\033[0m')
        urls = []
    return urls


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

if __name__ == '__main__':
    start_time = time.time()

    # search_duckduckgo('python programming')
    # print(getddg("尊嘟假嘟 含义"))
    # urls = getddgsearchurl("python programming")
    # urls = getddgsearchurl1("test")
    # urls = getddgsearchurl("你知道今天有什么热点新闻吗")
    # urls = getddg("尊嘟假嘟 含义")
    urls = getddgsearchurl("它会返回一个包含搜索结果的列表")
    print(urls)
    # for url in urls:
    #     print(Web_crawler(url))
    #     print('-----------------------------')
    end_time = time.time()
    run_time = end_time - start_time
    # 打印运行时间
    print(f"程序运行时间：{run_time}秒")