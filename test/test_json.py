import json

json_data = '爱'
# json_data = '爱的主人，我会尽快为您规划一个走线到美国的安全路线。请您稍等片刻。\n\n首先，我会检查免签国家并为您提供相应的信息。接下来，我会 搜索有关旅行到美国的安全建议和路线规划。{}'
def check_json(json_data):
    while True:
        try:
            json.loads(json_data)
            break
        except json.decoder.JSONDecodeError as e:
            print("JSON error：", e)
            print("JSON body", repr(json_data))
            if "Invalid control character" in str(e):
                json_data = json_data.replace("\n", "\\n")
            if "Unterminated string starting" in str(e):
                json_data += '"}'
            if "Expecting ',' delimiter" in str(e):
                json_data += '}'
            if "Expecting value: line 1 column 1" in str(e):
                json_data = '{"prompt": ' + json.dumps(json_data) + '}'
    return json_data
print(json.loads(check_json(json_data)))
