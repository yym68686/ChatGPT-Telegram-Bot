import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tiktoken
from utils.function_call import function_call_list
import config
import requests
import json
import re

from dotenv import load_dotenv
load_dotenv()

def get_token_count(messages) -> int:
    tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    num_tokens = 0
    for message in messages:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 5
        for key, value in message.items():
            if value:
                num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += 5  # role is always required and always 1 token
    num_tokens += 5  # every reply is primed with <im_start>assistant
    return num_tokens
# print(get_token_count(message_list))



def get_message_token(url, json_post):
    headers = {"Authorization": f"Bearer {os.environ.get('API', None)}"}
    response = requests.Session().post(
        url,
        headers=headers,
        json=json_post,
        timeout=None,
    )
    if response.status_code != 200:
        json_response = json.loads(response.text)
        string = json_response["error"]["message"]
        print(string)
        string = re.findall(r"\((.*?)\)", string)[0]
        numbers = re.findall(r"\d+\.?\d*", string)
        numbers = [int(i) for i in numbers]
        if len(numbers) == 2:
            return {
                "messages": numbers[0],
                "total": numbers[0],
            }
        elif len(numbers) == 3:
            return {
                "messages": numbers[0],
                "functions": numbers[1],
                "total": numbers[0] + numbers[1],
            }
        else:
            raise Exception("Unknown error")


if __name__ == "__main__":
    # message_list = [{'role': 'system', 'content': 'You are ChatGPT, a large language model trained by OpenAI. Respond conversationally in Simplified Chinese. Knowledge cutoff: 2021-09. Current date: [ 2023-12-12 ]'}, {'role': 'user', 'content': 'hi'}]
    messages = [{'role': 'system', 'content': 'You are ChatGPT, a large language model trained by OpenAI. Respond conversationally in Simplified Chinese. Knowledge cutoff: 2021-09. Current date: [ 2023-12-12 ]'}, {'role': 'user', 'content': 'hi'}, {'role': 'assistant', 'content': '你好！有什么我可以帮助你的吗？'}]

    model = "gpt-3.5-turbo"
    temperature = 0.5
    top_p = 0.7
    presence_penalty = 0.0
    frequency_penalty = 0.0
    reply_count = 1
    role = "user"
    model_max_tokens = 5000
    url = config.bot_api_url.chat_url

    json_post = {
            "model": model,
            "messages": messages,
            "stream": True,
            "temperature": temperature,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "n": reply_count,
            "user": role,
            "max_tokens": model_max_tokens,
    }
    # json_post.update(function_call_list["base"])
    # if config.PLUGINS["SEARCH_USE_GPT"]:
    #     json_post["functions"].append(function_call_list["SEARCH_USE_GPT"])
    # json_post["functions"].append(function_call_list["URL"])
    # print(get_token_count(message_list))
    print(get_message_token(url, json_post))
