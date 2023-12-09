import jieba
import jieba.analyse

# 加载文本
# text = "话说葬送的芙莉莲动漫是半年番还是季番？完结没？"
# text = "民进党当初为什么支持柯文哲选台北市长？"
text = "今天的微博热搜有哪些？"
# text = "How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?"

# 使用TF-IDF算法提取关键词
keywords_tfidf = jieba.analyse.extract_tags(text, topK=10, withWeight=False, allowPOS=())

# 使用TextRank算法提取关键词
keywords_textrank = jieba.analyse.textrank(text, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))

print("TF-IDF算法提取的关键词：", keywords_tfidf)
print("TextRank算法提取的关键词：", keywords_textrank)


seg_list = jieba.cut(text, cut_all=True)
print("Full Mode: " + " ".join(seg_list))  # 全模式

seg_list = jieba.cut(text, cut_all=False)
print("Default Mode: " + " ".join(seg_list))  # 精确模式

seg_list = jieba.cut(text)  # 默认是精确模式
print(" ".join(seg_list))

seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
result = " ".join(seg_list)

print([result] * 3)