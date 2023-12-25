import re
import datetime

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

if __name__ == "__main__":
    urls = ['https://www.bbc.com/zhongwen/simp/chinese-news-58392571', 'https://glginc.cn/articles/china-gaming-regulation-impact/', 'https://www.gov.cn/zhengce/2021-08/30/content_5634208.htm', 'https://zwgk.mct.gov.cn/zfxxgkml/zcfg/zcjd/202012/t20201205_915382.html', 'https://www.aljazeera.com/news/2023/12/23/china-considers-revising-gaming-rules-after-tech-giants-lose-billions', 'https://www.reuters.com/world/china/china-issues-draft-rules-online-game-management-2023-12-22/', 'https://www.cnn.com/2023/12/22/business/chinese-tech-giants-shares-plunge-online-gaming-ban-intl-hnk/index.html', 'https://www.bbc.com/news/technology-67801091', 'https://news.cctv.com/2023/12/22/ARTIUFZFQtfoBp1tfwsq1w1B231222.shtml', 'https://news.sina.com.cn/c/2023-12-22/doc-imzywncy6795505.shtml', 'https://www.thepaper.cn/newsDetail_forward_25728500', 'https://new.qq.com/rain/a/20230907A01LKT00']
    print(sort_by_time(urls))