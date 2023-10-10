import g4f
import re
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

def bing(response):
    response = re.sub(r"\[\^\d+\^\]", "", response)
    if len(response.split("\n\n")) >= 2:
        result = "\n\n".join(response.split("\n\n")[1:])
        return result
    else:
        return response

if __name__ == "__main__":
    import asyncio
    message = r"""

    """

    # result = asyncio.run(get_response(message, "gpt-4"))
    # print(result)

    # for result in get_response(message, handle_response):
    #     print(result, flush=True, end='')
    for result in get_response(message, "gpt-4"):
    # for result in get_response(message, "claude-v2"):
        print(bing(result), flush=True, end='')