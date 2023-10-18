my_list = [
    {"role": "admin", "content": "This is admin content."},
    {"role": "user", "content": "This is user content."}
]

content_list = [item["content"] for item in my_list]
print(content_list)
