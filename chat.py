import json
import requests
url = 'https://chatgpt-api.shn.hk/v1/'
body = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello, how are you?"}]
}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(body), headers=headers)
print(f"{r.text}")