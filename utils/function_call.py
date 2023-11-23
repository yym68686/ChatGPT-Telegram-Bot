function_call_list = {
  "current_weather": {
      "functions": [
          {
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
                  "enum": ["celsius", "fahrenheit"]
                }
              },
              "required": ["location"]
            }
          }
        ],
        "function_call": "auto"
  },
  "web_search": {
      "functions": [
          {
            "name": "get_web_search_results",
            "description": "Search Google to enhance knowledge.",
            "parameters": {
              "type": "object",
              "properties": {
                "prompt": {
                  "type": "string",
                  "description": "The prompt to search."
                }
              },
              "required": ["prompt"]
            }
          }
        ],
        "function_call": "auto"
  },
  "url_fetch": {
      "functions": [
          {
            "name": "get_url_content",
            "description": "Get the webpage content of a URL",
            "parameters": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "description": "The url to get the webpage content"
                }
              },
              "required": ["url"]
            }
          }
        ],
        "function_call": "auto"
  },
  # "web_search": {
  #     "functions": [
  #         {
  #           "name": "get_web_search_results",
  #           "description": "Get the web page search results in a given keywords",
  #           "parameters": {
  #             "type": "object",
  #             "properties": {
  #               "keywords": {
  #                 "type": "string",
  #                 "description": "keywords that can yield better search results, keywords are connected with spaces, e.g. 1. The keywords of the sentence (How much does the zeabur software service cost per month?) is (zeabur price). 2. The keywords of the sentence (今天的微博热搜有哪些？) is (微博 热搜)"
  #               }
  #             },
  #             "required": ["keywords"]
  #           }
  #         }
  #       ],
  #       "function_call": "auto"
  # },
}

