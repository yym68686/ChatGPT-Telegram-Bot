a = '''
'''

print(len(a))  # 1911

def split_code(text):
    import re
    split_list = []
    if len(text) > 2000:
        split_str_list = text.split('\n\n')

        conversation_len = len(split_str_list)
        message_index = 1
        while message_index < conversation_len:
            if split_str_list[message_index].startswith('    '):
                split_str_list[message_index - 1] += split_str_list[message_index + 1]
                split_str_list.pop(message_index)
                conversation_len = conversation_len - 1
            else:
                message_index = message_index + 1

        split_index = 0
        for index, _ in enumerate(split_str_list):
            if len("".join(split_str_list[:index])) < len(text) // 2:
                split_index += 1
                continue
            else:
                break
        str1 = '\n\n'.join(split_str_list[:split_index])
        str1 = str1 + "\n```"
        split_list.append(str1)
        code_type = text.split('\n')[0]
        str2 = '\n\n'.join(split_str_list[split_index:])
        str2 = code_type + "\n" + str2
        split_list.append(str2)
    else:
        split_list.append(text)
    split_list = "\n@|@|@|@\n\n".join(split_list)
    return split_list


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from md2tgmd.src.md2tgmd import replace_all
text = replace_all(a, r"(```[\D\d\s]+?```)", split_code)
print(text)
# for i in split_code(a):
#     print(i)