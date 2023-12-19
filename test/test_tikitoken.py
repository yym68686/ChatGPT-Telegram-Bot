import tiktoken
tiktoken.get_encoding("cl100k_base")
tiktoken.model.MODEL_TO_ENCODING["claude-2.1"] = "cl100k_base"
tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
# encoding = tiktoken.encoding_for_model("claude-2.1")
encode_web_text_list = []
if encode_web_text_list == []:
    encode_web_text_list = encoding.encode("Hello, my dog is cute")
    print("len", len(encode_web_text_list))
function_response = encoding.decode(encode_web_text_list[:2])
print(function_response)
encode_web_text_list = encode_web_text_list[2:]
print(encode_web_text_list)
encode_web_text_list = [856, 5679, 374, 19369]
tiktoken.get_encoding("cl100k_base")
encoding1 = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
function_response = encoding1.decode(encode_web_text_list[:2])
print(function_response)