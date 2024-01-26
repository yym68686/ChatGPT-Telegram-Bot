import re
import g4f
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

GPT_ENGINE_map = {
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k": "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0301": "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613": "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106": "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k-0613": "gpt-3.5-turbo-0613",
    "gpt-4": "gpt-4",
    "gpt-4-0314": "gpt-4",
    "gpt-4-32k": "gpt-4-32k",
    "gpt-4-32k-0314": "gpt-4",
    "gpt-4-0613": "gpt-4-0613",
    "gpt-4-32k-0613": "gpt-4-32k-0613",
    "gpt-4-1106-preview": "gpt-4-turbo",
    "gpt-4-turbo-preview": "gpt-4-turbo",
    "gpt-4-0125-preview": "gpt-4-turbo",
    "gpt-4-vision-preview": "gpt-4",
    "claude-2-web": "gpt-4",
    "claude-2": "gpt-4",
}

def ask_stream(message, **kwargs):
    response = g4f.ChatCompletion.create(
        model=GPT_ENGINE_map[config.GPT_ENGINE],
        messages=[{"role": "user", "content": message}],
        stream=True,
    )
    for message in response:
        yield message

def bing(response):
    response = re.sub(r"\[\^\d+\^\]", "", response)
    if len(response.split("\n\n")) >= 2:
        result = "\n\n".join(response.split("\n\n")[1:])
        return result
    else:
        return response

if __name__ == "__main__":

    message = rf"""
鲁迅和周树人为什么打架
    """
    answer = ""
    for result in ask_stream(message, model="gpt-4"):
        print(result, end="")