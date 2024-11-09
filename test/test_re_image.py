import re

tmpresult = '''
{"prompt": "A cute, realistic drawing of a cat sitting and looking curious. The cat has soft fur with a mix of light gray and white colors, with big, expressive eyes, and small whiskers. The background is simple, light-colored, and unobtrusive to focus on the cat. The cat is in a relaxed position with its tail wrapped around its paws, giving a calm and friendly appearance.", "size": "1024x1024"}

Вот изображение летнего пейзажа с полем цветов и голубым небом:\n\n![Летний пейзаж](https://dalleproduse.blob.core.windows.net/private/images/2eaaa4d4-0a52-4e05-a1e0-6e656677d97f/generated_00.png?se=2024-11-09T17%3A58%3A05Z&sig=gqpXku59hDTglUXSV%2FYr%2BtFH32YsRpbSHH45OpxJgAY%3D&ske=2024-11-14T06%3A25%3A30Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-11-07T06%3A25%3A30Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02)\n\nНадеюсь, вам понравится!
https://pfst.cf2.poecdn.net/base/image/7fe4e48a4213e54a893e10aee94dd554942b21d27fd9fab40058cea8088ac5a7?w=1024&h=768&pmaid=200986697
![Летний пейзаж](https://dalleproduse.blob.core.windows.net/private/images/2eaaa4d4-0a52-4e05-a1e0-6e656677d97f/generated_00.png?se=2024-11-09T17%3A58%3A05Z&sig=gqpXku59hDTglUXSV%2FYr%2BtFH32YsRpbSHH45OpxJgAY%3D&ske=2024-11-14T06%3A25%3A30Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-11-07T06%3A25%3A30Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02)
下载1 (https://filesystem.site/cdn/download/20241108/GHLsxBAJNidSekOO4aYu8ksHeiwmr7.webp)

Here image of cat!
'''

# 修改正则表达式模式，使用括号来捕获整个URL
image_extensions = r'(https?://[^\s<>\"()]+(?:\.(?:webp|jpg|jpeg|png|gif)|/image)[^\s<>\"()]*)'
image_urls = re.findall(image_extensions, tmpresult, re.IGNORECASE)
image_urls_result = [url[0] if isinstance(url, tuple) else url for url in image_urls]

# 如果结果是元组列表，我们可以获取第一个元素
print(image_urls_result[0])
