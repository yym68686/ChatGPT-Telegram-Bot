import os
from rich.console import Console
from rich.markdown import Markdown
import json
import requests

def query_ollama(prompt, model):
    # 设置请求的URL和数据
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": model,
        "prompt": prompt,
        "stream": True,
    }

    response = requests.Session().post(
        url,
        json=data,
        stream=True,
    )
    full_response: str = ""
    for line in response.iter_lines():
        if not line or line.decode("utf-8")[:6] == "event:" or line.decode("utf-8") == "data: {}":
            continue
        line = line.decode("utf-8")
        # print(line)
        resp: dict = json.loads(line)
        content = resp.get("response")
        if not content:
            continue
        full_response += content
        yield content

if __name__ == "__main__":
    console = Console()
    # model = 'llama2'
    # model = 'mistral'
    # model = 'llama3:8b'
    model = 'qwen:14b'
    # model = 'wizardlm2:7b'
    # model = 'codeqwen:7b-chat'
    # model = 'phi'

    # 查询答案
    prompt = r'''

详细讲解一下SAFE块是怎么进行进行时间特征聚合的？

'''
    answer = ""
    for result in query_ollama(prompt, model):
        os.system("clear")
        answer += result
        md = Markdown(answer)
        console.print(md, no_wrap=False)
