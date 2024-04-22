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

The Space-Time Video Super-Resolution (STVSR) task aims to enhance the visual quality of videos, by simultaneously performing video frame interpolation (VFI) and video super-resolution (VSR). However, facing the challenge of the additional temporal dimension and scale inconsistency, most existing STVSR methods are complex and inflexible in dynamically modeling different motion amplitudes. In this work, we find that choosing an appropriate processing scale achieves remarkable benefits in flow-based feature propagation. We propose a novel Scale-Adaptive Feature Aggregation (SAFA) network that adaptively selects sub-networks with different processing scales for individual samples. Experiments on four public STVSR benchmarks demonstrate that SAFA achieves state-of-the-art performance. Our SAFA network outperforms recent state-of-the-art methods such as TMNet [83] and VideoINR [10] by an average improvement of over 0.5dB on PSNR, while requiring less than half the number of parameters and only 1/3 computational costs.

上面的文字翻译成中文

'''
    answer = ""
    for result in query_ollama(prompt, model):
        os.system("clear")
        answer += result
        md = Markdown(answer)
        console.print(md, no_wrap=False)
