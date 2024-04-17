def is_surrounded_by_chinese(text, index):
    left_char = text[index - 1]
    if 0 < index < len(text) - 1:
        right_char = text[index + 1]
        return '\u4e00' <= left_char <= '\u9fff' or '\u4e00' <= right_char <= '\u9fff'
    if index == len(text) - 1:
        return '\u4e00' <= left_char <= '\u9fff'
    return False

def replace_char(string, index, new_char):
    return string[:index] + new_char + string[index+1:]

def claude_replace(text):
    Punctuation_mapping = {",": "，", ":": "：", "!": "！", "?": "？", ";": "；"}
    key_list = list(Punctuation_mapping.keys())
    for i in range(len(text)):
        if is_surrounded_by_chinese(text, i) and (text[i] in key_list):
            text = replace_char(text, i, Punctuation_mapping[text[i]])
    return text

text = '''
你好！我是一名人工智能助手，很高兴见到你。有什么我可以帮助你的吗？无论是日常问题还是专业领域，我都会尽我所能为你解答。让我们开始愉快的交流吧!'''

if __name__ == '__main__':
    new_text = claude_replace(text)
    print(new_text)