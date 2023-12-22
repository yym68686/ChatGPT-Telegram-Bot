import json
# my_list = [
#     {"role": "admin", "content": "This is admin content."},
#     {"role": "user", "content": "This is user content."}
# ]
a = {"role": "admin"}
b = {"content": []}
c = {"role": "admin"}
a.update(b)
a["content"].append(c)
print(b)
print(a)
# print(json.dumps(str(a), indent=4))

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

# print(json.dumps(function_call_list["SEARCH_USE_GPT"], indent=4))

# class openaiAPI:
#     def __init__(
#         self,
#         api_url: str = (os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions"),
#     ):
#         from urllib.parse import urlparse, urlunparse
#         self.source_api_url: str = api_url
#         parsed_url = urlparse(self.source_api_url)
#         self.base_url: str = urlunparse(parsed_url[:2] + ("",) * 4)
#         self.v1_url: str = urlunparse(parsed_url[:2] + ("/v1",) + ("",) * 3)
#         self.chat_url: str = urlunparse(parsed_url[:2] + ("/v1/chat/completions",) + ("",) * 3)
#         self.image_url: str = urlunparse(parsed_url[:2] + ("/v1/images/generations",) + ("",) * 3)


# a = openaiAPI()
# print(a.v1_url)

# def getddgsearchurl(result, numresults=3):
#     # print("ddg-search", result)
#     search = DuckDuckGoSearchResults(num_results=numresults)
#     webresult = search.run(result)
#     # print("ddgwebresult", webresult)
#     urls = re.findall(r"(https?://\S+)\]", webresult, re.MULTILINE)
#     # print("duckduckgo urls", urls)
#     return urls