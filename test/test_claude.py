import os
import requests
# from ..utils import typings as t
import json
import tiktoken
# class claudeConversation(dict):
#     def __getitem__(self, index):
#         conversation_list = super().__getitem__(index)
#         return "\n\n" + "\n\n".join([f"{item['role']}:{item['content']}" for item in conversation_list]) + "\n\nAssistant:"

# c = claudeConversation()
# c['1'] = [{'role': 'A', 'content': 'hello'}, {'role': 'B', 'content': 'hi'}]
# print(repr(c['1']))

import platform
python_version = list(platform.python_version_tuple())
SUPPORT_ADD_NOTES = int(python_version[0]) >= 3 and int(python_version[1]) >= 11

class ChatbotError(Exception):
    """
    Base class for all Chatbot errors in this Project
    """

    def __init__(self, *args: object) -> None:
        if SUPPORT_ADD_NOTES:
            super().add_note(
                "Please check that the input is correct, or you can resolve this issue by filing an issue",
            )
            super().add_note("Project URL: https://github.com/acheong08/ChatGPT")
        super().__init__(*args)

class APIConnectionError(ChatbotError):
    """
    Subclass of ChatbotError

    An exception object thrown when an API connection fails or fails to connect due to network or
    other miscellaneous reasons
    """

    def __init__(self, *args: object) -> None:
        if SUPPORT_ADD_NOTES:
            super().add_note(
                "Please check if there is a problem with your network connection",
            )
        super().__init__(*args)

class claudeConversation(dict):
    def Conversation(self, index):
        conversation_list = super().__getitem__(index)
        return "\n\n" + "\n\n".join([f"{item['role']}:{item['content']}" for item in conversation_list]) + "\n\nAssistant:"


class claudebot:
    def __init__(
        self,
        api_key: str,
        engine: str = os.environ.get("GPT_ENGINE") or "claude-2",
        temperature: float = 0.5,
        top_p: float = 0.7,
        chat_url: str = "https://api.anthropic.com/v1/complete",
        timeout: float = None,
    ):
        self.api_key: str = api_key
        self.engine: str = engine
        self.temperature = temperature
        self.top_p = top_p
        self.chat_url = chat_url
        self.timeout = timeout
        self.session = requests.Session()
        self.conversation = claudeConversation()

    def add_to_conversation(
        self,
        message: str,
        role: str,
        convo_id: str = "default",

    ) -> None:
        """
        Add a message to the conversation
        """
        self.conversation[convo_id].append({"role": role, "content": message})

    def reset(self, convo_id: str = "default") -> None:
        """
        Reset the conversation
        """
        self.conversation[convo_id] = list()

    def __truncate_conversation(self, convo_id: str = "default") -> None:
        """
        Truncate the conversation
        """
        while True:
            if (
                self.get_token_count(convo_id) > self.truncate_limit
                and len(self.conversation[convo_id]) > 1
            ):
                # Don't remove the first message
                self.conversation[convo_id].pop(1)
            else:
                break

    def get_token_count(self, convo_id: str = "default") -> int:
        """
        Get token count
        """
        if self.engine not in ENGINES:
            raise NotImplementedError(
                f"Engine {self.engine} is not supported. Select from {ENGINES}",
            )
        tiktoken.get_encoding("cl100k_base")
        tiktoken.model.MODEL_TO_ENCODING["claude-2"] = "cl100k_base"

        encoding = tiktoken.encoding_for_model(self.engine)

        num_tokens = 0
        for message in self.conversation[convo_id]:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 5
            for key, value in message.items():
                if value:
                    num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += 5  # role is always required and always 1 token
        num_tokens += 5  # every reply is primed with <im_start>assistant
        return num_tokens

    def ask_stream(
        self,
        prompt: str,
        role: str = "Human",
        convo_id: str = "default",
        model: str = None,
        pass_history: bool = True,
        model_max_tokens: int = 4096,
        **kwargs,
    ):
        if convo_id not in self.conversation or pass_history == False:
            self.reset(convo_id=convo_id)
        self.add_to_conversation(prompt, role, convo_id=convo_id)
        # self.__truncate_conversation(convo_id=convo_id)
        # print(self.conversation[convo_id])

        url = self.chat_url
        headers = {
            "accept": "application/json",
            "anthropic-version": "2023-06-01", 
            "content-type": "application/json",      
            "x-api-key": f"{kwargs.get('api_key', self.api_key)}",
        }

        json_post = {
                "model": os.environ.get("MODEL_NAME") or model or self.engine,
                "prompt": self.conversation.Conversation(convo_id) if pass_history else f"\n\nHuman:{prompt}\n\nAssistant:",
                "stream": True,
                "temperature": kwargs.get("temperature", self.temperature),
                "top_p": kwargs.get("top_p", self.top_p),
                "max_tokens_to_sample": model_max_tokens,
        }

        response = self.session.post(
            url,
            headers=headers,
            json=json_post,
            timeout=kwargs.get("timeout", self.timeout),
            stream=True,
        )
        if response.status_code != 200:
            raise BaseException(f"{response.status_code} {response.reason} {response.text}")
        response_role: str = "Assistant"
        full_response: str = ""
        for line in response.iter_lines():
            if not line or line.decode("utf-8") == "event: completion" or line.decode("utf-8") == "event: ping" or line.decode("utf-8") == "data: {}":
                continue
            line = line.decode("utf-8")[6:]
            # print(line)
            resp: dict = json.loads(line)
            content = resp.get("completion")
            full_response += content
            yield content
        self.add_to_conversation(full_response, response_role, convo_id=convo_id)
        print(repr(self.conversation.Conversation(convo_id)))
        # print("total tokens:", self.get_token_count(convo_id))


bot = claudebot(api_key=os.environ.get("claude_api_key"))

for i in bot.ask_stream("python怎么自定义错误"):
    print(i, end="")