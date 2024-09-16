def is_emoji(character):
    if len(character) != 1:
        return False

    code_point = ord(character)

    # 定义表情符号的Unicode范围
    emoji_ranges = [
        (0x1F300, 0x1F5FF),  # 杂项符号和图形
        (0x1F600, 0x1F64F),  # 表情符号
        (0x1F680, 0x1F6FF),  # 交通和地图符号
        (0x2600, 0x26FF),    # 杂项符号
        (0x2700, 0x27BF),    # 装饰符号
        (0x1F900, 0x1F9FF)   # 补充符号和图形
    ]

    # 检查字符的Unicode码点是否在任何一个表情符号范围内
    return any(start <= code_point <= end for start, end in emoji_ranges)

print(is_emoji("😭"))  # 应该返回 True
print(is_emoji("A"))   # 应该返回 False
print(is_emoji("你"))  # 应该返回 False