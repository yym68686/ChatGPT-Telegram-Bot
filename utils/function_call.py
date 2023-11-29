function_call_list = {
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
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  },
  "web_search": {
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
      "required": ["prompt"]
    }
  },
  "url_fetch": {
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
      "required": ["url"]
    }
  },
}

