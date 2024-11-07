import urllib.parse

def svg_to_url(svg_string):
    # URL编码SVG字符串
    encoded_svg = urllib.parse.quote(svg_string)

    # 创建data URL
    url = f"data:image/svg+xml,{encoded_svg}"

    return url

# 使用示例
svg_content = """
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"> <!-- Black background --> <rect width="100%" height="100%" fill="#000000"/> <!-- Main chat bubble outline --> <path d="M50 100 L90 60 L150 60 L150 120 L110 160 L50 160 Z" fill="none" stroke="white" stroke-width="2" opacity="0.9"/> <!-- Circuit pattern lines --> <g stroke="white" stroke-width="1.5" opacity="0.8"> <path d="M70 90 L130 90"> <animate attributeName="opacity" values="0.8;0.4;0.8" dur="3s" repeatCount="indefinite"/> </path> <path d="M70 110 L130 110"/> <path d="M70 130 L130 130"/> </g> <!-- Dynamic angular elements --> <path d="M90 60 L120 30 L180 30 L150 60" fill="none" stroke="white" stroke-width="1.5" opacity="0.6"/> <!-- AI node points --> <circle cx="70" cy="90" r="3" fill="white"/> <circle cx="130" cy="110" r="3" fill="white"/> <circle cx="100" cy="130" r="3" fill="white"> <animate attributeName="r" values="3;4;3" dur="2s" repeatCount="indefinite"/> </circle> </svg>
"""

url = svg_to_url(svg_content)
print(url)