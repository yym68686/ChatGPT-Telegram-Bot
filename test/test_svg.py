import urllib.parse

def svg_to_url(svg_string):
    # URL编码SVG字符串
    encoded_svg = urllib.parse.quote(svg_string)

    # 创建data URL
    url = f"data:image/svg+xml,{encoded_svg}"

    return url

# 使用示例
svg_content = """

"""

url = svg_to_url(svg_content)
print(url)