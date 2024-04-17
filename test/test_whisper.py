import requests
import os

headers = {
    "Authorization": f"Bearer {os.environ.get('API', None)}",
    "Content-Type": "multipart/form-data"
}
files = {
    'file': ('filename', open('/path/to/file/audio.mp3', 'rb'), 'audio/mpeg'),
    'model': (None, 'whisper-1')
}

response = requests.post(os.environ.get('API_URL', None), headers=headers, files=files)
print(response.text)