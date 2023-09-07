import requests
from bs4 import BeautifulSoup
def Web_crawler(url: str) -> str:
    """返回链接网址url正文内容，必须是合法的网址"""
    response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(response.text.encode(response.encoding), 'lxml', from_encoding='utf-8')
    # print(soup)
    body = "".join(soup.find('body').get_text().split('\n'))
    result = body
    # result = summary(body)
    return result

import os
os.system("clear")
for i in ['https://www.gov.cn/ldhd/2013-12/07/content_2543945.htm', 'http://brics2022.mfa.gov.cn/chn/hywj/ldrhwcgwj/202203/t20220308_10649249.html', 'https://www.fmprc.gov.cn/chn/gxh/tyb/zyxw/202308/t20230825_11132502.html']:
    print(Web_crawler(i))
    # break