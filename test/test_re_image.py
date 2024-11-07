import re

tmpresult = '''
{"prompt": "A cute, realistic drawing of a cat sitting and looking curious. The cat has soft fur with a mix of light gray and white colors, with big, expressive eyes, and small whiskers. The background is simple, light-colored, and unobtrusive to focus on the cat. The cat is in a relaxed position with its tail wrapped around its paws, giving a calm and friendly appearance.", "size": "1024x1024"}

image1 (https://filesystem.site/cdn/20241108/GHLsxBAJNidSekOO4aYu8ksHeiwmr7.webp)

下载1 (https://filesystem.site/cdn/download/20241108/GHLsxBAJNidSekOO4aYu8ksHeiwmr7.webp)

Here image of cat!
'''

# 修改正则表达式模式，使用括号来捕获整个URL
image_extensions = r'(https?://[^\s<>\"]+?/[^\s<>\"]+?\.(webp|jpg|jpeg|png|gif))'
image_urls = re.findall(image_extensions, tmpresult, re.IGNORECASE)
image_urls_result = [url[0] if isinstance(url, tuple) else url for url in image_urls]

# 如果结果是元组列表，我们可以获取第一个元素
print(image_urls_result[0])
