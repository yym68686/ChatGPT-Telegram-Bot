# my_list = [
#     {"role": "admin", "content": "This is admin content."},
#     {"role": "user", "content": "This is user content."}
# ]
a = {"role": "admin"}
b = {"content": "This is user content."}
a.update(b)
# print(a)

# content_list = [item["content"] for item in my_list]
# print(content_list)

# engine = "gpt-3.5-turbo-1106"
# truncate_limit = (
#     30500
#     if "gpt-4-32k" in engine
#     else 6500
#     if "gpt-4" in engine
#     else 14500
#     if "gpt-3.5-turbo-16k" in engine or "gpt-3.5-turbo-1106" in engine
#     else 98500
#     if ("claude-2-web" or "claude-2") in engine
#     else 3400
# )

# print(truncate_limit)
import os
# import sys
# import json
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from utils.function_call import function_call_list

# print(json.dumps(function_call_list["web_search"], indent=4))

class openaiAPI:
    def __init__(
        self,
        api_url: str = (os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions"),
    ):
        from urllib.parse import urlparse, urlunparse
        self.source_api_url: str = api_url
        parsed_url = urlparse(self.source_api_url)
        self.base_url: str = urlunparse(parsed_url[:2] + ("",) * 4)
        self.chat_url: str = urlunparse(parsed_url[:2] + ("/v1/chat/completions",) + ("",) * 3)
        self.image_url: str = urlunparse(parsed_url[:2] + ("/v1/images/generations",) + ("",) * 3)


a = openaiAPI()
print(a.chat_url)