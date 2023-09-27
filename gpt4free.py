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

if __name__ == "__main__":
    import asyncio
    message = r"""
    鲁迅和周树人为什么打架
    """

    # result = asyncio.run(get_response(message, "gpt-4"))
    # print(result)

    for result in get_response(message, "gpt-4"):
        print(result, flush=True, end='')