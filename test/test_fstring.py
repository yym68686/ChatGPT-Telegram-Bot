username = "efwef"
def create_info_message():
    return (
        f"`Hi, {username}!`\n\n"
    )

# 假设 update 和 config 是已经定义好的对象
# 当你需要更新 info_message 时，只需调用这个函数
info_message = create_info_message()
print(info_message)
username = "e111111"
info_message = create_info_message()
print(info_message)