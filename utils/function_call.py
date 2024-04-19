function_call_list = \
{
    "base": {
        "functions": [],
        "function_call": "auto"
    },
    "current_weather": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "celsius",
                        "fahrenheit"
                    ]
                }
            },
            "required": [
                "location"
            ]
        }
    },
    "SEARCH_USE_GPT": {
        "name": "get_search_results",
        "description": "Search Google to enhance knowledge.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The prompt to search."
                }
            },
            "required": [
                "prompt"
            ]
        }
    },
    "URL": {
        "name": "get_url_content",
        "description": "Get the webpage content of a URL",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "the URL to request"
                }
            },
            "required": [
                "url"
            ]
        }
    },
    "DATE": {
        "name": "get_date_time_weekday",
        "description": "Get the current time, date, and day of the week",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "VERSION": {
        "name": "get_version_info",
        "description": "Get version information",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
}
def gpt2claude_tools_json(json_dict):
    import copy
    json_dict = copy.deepcopy(json_dict)
    keys_to_change = {
        "parameters": "input_schema",
        "functions": "tools",
        "function_call": None  # 如果没有新的键名，则设置为None或留空
    }
    for old_key, new_key in keys_to_change.items():
        if old_key in json_dict:
            if new_key:
                json_dict[new_key] = json_dict.pop(old_key)
            else:
                json_dict.pop(old_key)
    return json_dict

claude_tools_list = {f"{key}": gpt2claude_tools_json(function_call_list[key]) for key in function_call_list.keys()}
