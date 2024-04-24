import re
import os
os.system('cls' if os.name == 'nt' else 'clear')
import time
import chardet
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

# def Web_crawler(url: str) -> str:
#     """返回链接网址url正文内容，必须是合法的网址"""
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
#     result = ''
#     try:
#         requests.packages.urllib3.disable_warnings()
#         response = requests.get(url, headers=headers, verify=False)
#         soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
#         body = "".join(soup.find('body').get_text().split('\n'))
#         result = body
#     except Exception as e:
#         print('\033[31m')
#         print("error", e)
#         print('\033[0m')
#     return result

# def Web_crawler(url: str) -> str:
#     """返回链接网址url正文内容，必须是合法的网址"""
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
#     result = ''
#     try:
#         requests.packages.urllib3.disable_warnings()
#         response = requests.get(url, headers=headers, verify=False, timeout=5, stream=True)
#         content_length = int(response.headers.get('Content-Length', 0))
#         if content_length > 500000:
#             print("Skipping large file:", url)
#             return result
#         # detected_encoding = chardet.detect(response.content)['encoding']
#         # decoded_content = response.content.decode(detected_encoding, errors='replace')
#         # # soup = BeautifulSoup(response.text, 'html.parser')
#         # soup = BeautifulSoup(decoded_content, 'lxml')
#         # # soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
#         # body = "".join(soup.find('body').get_text().split('\n'))
#         # result = body

#         detected_encoding = chardet.detect(response.content)['encoding']
#         decoded_content = response.content.decode(detected_encoding, errors='ignore')
#         decoded_content = re.sub(r'[^\u0000-\uFFFF]', ' ', decoded_content)
#         soup = BeautifulSoup(decoded_content, 'lxml')
#         body = soup.find('body').get_text()
#         body = body.replace('\n', ' ')
#         body = re.sub(r'http[s]?://\S+', ' ', body)
#         body = re.sub(r'\s+', ' ', body)
#         result = body

#     except Exception as e:
#         print('\033[31m')
#         print("error url", url)
#         print("error", e)
#         print('\033[0m')
#     return result

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
            return "抱歉，网页不存在，目前无法访问该网页。@Trash@"
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
            result = "抱歉，可能反爬虫策略，目前无法访问该网页。@Trash@"
        if result.count("\"") > 1000:
            result = ""
    except Exception as e:
        print('\033[31m')
        print("error url", url)
        print("error", e)
        print('\033[0m')
    print("url content", result + "\n\n")
    return result

def jina_ai_Web_crawler(url: str, isSearch=False) -> str:
    """返回链接网址url正文内容，必须是合法的网址"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    result = ''
    try:
        requests.packages.urllib3.disable_warnings()
        url = "https://r.jina.ai/" + url
        response = requests.get(url, headers=headers, verify=False, timeout=3, stream=True)
        if response.status_code == 404:
            print("Page not found:", url)
            return "抱歉，网页不存在，目前无法访问该网页。@Trash@"
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
            result = "抱歉，可能反爬虫策略，目前无法访问该网页。@Trash@"
        if result.count("\"") > 1000:
            result = ""
    except Exception as e:
        print('\033[31m')
        print("error url", url)
        print("error", e)
        print('\033[0m')
    print(result + "\n\n")
    return result

# def Web_crawler(url: str) -> str:
#     """返回链接网址url正文内容，必须是合法的网址"""
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
#     result = ''
#     try:
#         requests.packages.urllib3.disable_warnings()
#         response = requests.get(url, headers=headers, verify=False, timeout=5, stream=True)
#         content_length = int(response.headers.get('Content-Length', 0))
#         if content_length > 500000:
#             print("Skipping large file:", url)
#             return result
#         soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
#         body = "".join(soup.find('body').get_text().split('\n'))
#         result = body
#     except Exception as e:
#         print('\033[31m')
#         print("error url", url)
#         print("error", e)
#         print('\033[0m')
#     return result

start_time = time.time()
# for url in ['https://www.zhihu.com/question/557257320', 'https://job.achi.idv.tw/2021/12/05/what-is-the-403-forbidden-error-how-to-fix-it-8-methods-explained/', 'https://www.lifewire.com/403-forbidden-error-explained-2617989']:
# for url in ['https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403', 'https://www.hostinger.com/tutorials/what-is-403-forbidden-error-and-how-to-fix-it', 'https://beebom.com/what-is-403-forbidden-error-how-to-fix/']:
# for url in ['https://www.lifewire.com/403-forbidden-error-explained-2617989']:
# for url in ['https://www.usnews.com/news/best-countries/articles/2022-02-24/explainer-why-did-russia-invade-ukraine']:
# for url in ['https://github.com/EAimTY/tuic/issues/107']:
# TODO 没办法访问
# for url in ['https://s.weibo.com/top/summary?cate=realtimehot']:
# for url in ['https://tophub.today/n/KqndgxeLl9']:
# for url in ['https://support.apple.com/zh-cn/HT213931']:
for url in ["https://zeta.zeabur.app", "https://www.anthropic.com/research/probes-catch-sleeper-agents"]:
# for url in ['https://finance.sina.com.cn/stock/roll/2023-06-26/doc-imyyrexk4053724.shtml', 'https://s.weibo.com/top/summary?cate=realtimehot', 'https://tophub.today/n/KqndgxeLl9', 'https://www.whatsonweibo.com/', 'https://www.trendingonweibo.com/?ref=producthunt', 'https://www.trendingonweibo.com/', 'https://www.statista.com/statistics/1377073/china-most-popular-news-on-weibo/']:
# for url in ['https://www.usnews.com/news/entertainment/articles/2023-12-22/china-drafts-new-rules-proposing-restrictions-on-online-gaming']:
# for url in ['https://developer.aliyun.com/article/721836']:
# for url in ['https://cn.aliyun.com/page-source/price/detail/machinelearning_price']:
# for url in ['https://mp.weixin.qq.com/s/Itad7Y-QBcr991JkF3SrIg']:
# for url in ['https://zhidao.baidu.com/question/317577832.html']:
# for url in ['https://www.cnn.com/2023/09/06/tech/huawei-mate-60-pro-phone/index.html']:
# for url in ['https://www.reddit.com/r/China_irl/comments/15qojkh/46%E6%9C%88%E5%A4%96%E8%B5%84%E5%AF%B9%E4%B8%AD%E5%9B%BD%E7%9B%B4%E6%8E%A5%E6%8A%95%E8%B5%84%E5%87%8F87/', 'https://www.apple.com.cn/job-creation/Apple_China_CSR_Report_2020.pdf', 'https://hdr.undp.org/system/files/documents/hdr2013chpdf.pdf']:
# for url in ['https://www.airuniversity.af.edu/JIPA/Display/Article/3111127/the-uschina-trade-war-vietnam-emerges-as-the-greatest-winner/']:
# for url in ['https://zhuanlan.zhihu.com/p/646786536', 'https://zh.wikipedia.org/wiki/%E4%BF%84%E7%BE%85%E6%96%AF%E5%85%A5%E4%BE%B5%E7%83%8F%E5%85%8B%E8%98%AD', 'https://stock.finance.sina.com.cn/usstock/quotes/aapl.html']:
    Web_crawler(url)
    # jina_ai_Web_crawler(url)
    print('-----------------------------')
end_time = time.time()
run_time = end_time - start_time
# 打印运行时间
print(f"程序运行时间：{run_time}秒")
