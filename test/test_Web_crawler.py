import os
os.system('cls' if os.name == 'nt' else 'clear')
import requests
from bs4 import BeautifulSoup

def Web_crawler(url: str) -> str:
    """返回链接网址url正文内容，必须是合法的网址"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    result = ''
    try:
        soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
        body = "".join(soup.find('body').get_text().split('\n'))
        result = body
    except Exception as e:
        print('\033[31m')
        print("error", e)
        print('\033[0m')
    return result


# for url in ['https://www.zhihu.com/question/557257320', 'https://job.achi.idv.tw/2021/12/05/what-is-the-403-forbidden-error-how-to-fix-it-8-methods-explained/', 'https://www.lifewire.com/403-forbidden-error-explained-2617989']:
# for url in ['https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403', 'https://www.hostinger.com/tutorials/what-is-403-forbidden-error-and-how-to-fix-it', 'https://beebom.com/what-is-403-forbidden-error-how-to-fix/']:
for url in ['https://www.lifewire.com/403-forbidden-error-explained-2617989']:
    print(Web_crawler(url))
    print('-----------------------------')

