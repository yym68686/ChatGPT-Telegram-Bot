import json

json_data = '{"prompt":"autogpt \\"}'
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
    return json_data
print(json.loads(check_json(json_data)))
