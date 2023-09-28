import g4f
async def get_async_response(message, model="gpt-3.5-turbo"):
    response = await g4f.ChatCompletion.create_async(
        model=model,
        messages=[{"role": "user", "content": message}],
    )
    return response

def get_response(message, model="gpt-3.5-turbo"):
    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": message}],
        stream=True,
    )
    for message in response:
        yield message


# def get_response(message, callback, model="gpt-3.5-turbo"):
#     response = g4f.ChatCompletion.create(
#         model=model,
#         messages=[{"role": "user", "content": message}],
#         stream=True,
#     )
#     for message in response:
#         callback(message)

# def handle_response(response):
#     yield response

if __name__ == "__main__":
    import asyncio
    message = r"""
在多线程编程场景下，为了避免There is no current event loop in thread错误，怎么使用回调函数返回这个函数的结果：
def get_response(message, model="gpt-3.5-turbo"):
    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": message}],
        stream=True,
    )
    for message in response:
        yield message
    """

    # result = asyncio.run(get_response(message, "gpt-4"))
    # print(result)

    # for result in get_response(message, handle_response):
    #     print(result, flush=True, end='')
    for result in get_response(message, "gpt-4"):
        print(result, flush=True, end='')