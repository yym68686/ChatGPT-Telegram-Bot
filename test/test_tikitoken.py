import tiktoken
# tiktoken.get_encoding("cl100k_base")
tiktoken.model.MODEL_TO_ENCODING["claude-2.1"] = "cl100k_base"
encoding = tiktoken.encoding_for_model("claude-2.1")