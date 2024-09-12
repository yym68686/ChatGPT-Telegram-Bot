import urllib.parse

def svg_to_url(svg_string):
    # URL编码SVG字符串
    encoded_svg = urllib.parse.quote(svg_string)

    # 创建data URL
    url = f"data:image/svg+xml,{encoded_svg}"

    return url

# 使用示例
svg_content = """<svg width="400" height="600" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#F0EAD6"/>
  <text x="200" y="50" font-family="楷体" font-size="24" fill="#333" text-anchor="middle">汉语新解</text>
  <line x1="40" y1="70" x2="360" y2="70" stroke="#333" stroke-width="1"/>
  <text x="50" y="100" font-family="楷体" font-size="18" fill="#333">特朗普 (tè lǎng pǔ)</text>
  <text x="50" y="130" font-family="楷体" font-size="16" fill="#555">Trump / トランプ</text>
  <text x="50" y="170" font-family="楷体" font-size="18" fill="#333" width="300">
    <tspan x="50" dy="0">一场政治马戏的主角，</tspan>
    <tspan x="50" dy="30">头顶金色假发的现实版小丑。</tspan>
    <tspan x="50" dy="30">他用推特当剧本，</tspan>
    <tspan x="50" dy="30">把白宫变成了荒诞剧舞台。</tspan>
    <tspan x="50" dy="30">观众们啼笑皆非，</tspan>
    <tspan x="50" dy="30">却不知是该为剧情鼓掌，</tspan>
    <tspan x="50" dy="30">还是为民主哀悼。</tspan>
  </text>
  <path d="M320 500 Q340 480 360 500" stroke="#888" fill="none"/>
  <path d="M40 550 Q60 570 80 550" stroke="#888" fill="none"/>
</svg>"""

url = svg_to_url(svg_content)
print(url)