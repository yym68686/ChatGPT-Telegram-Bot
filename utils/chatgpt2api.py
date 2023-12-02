import os
import json
from pathlib import Path
from typing import AsyncGenerator

import httpx
import requests
import tiktoken

from . import typings as t
from typing import Set

import config
from utils.agent import Web_crawler, search_web_and_summary, get_search_results
from utils.function_call import function_call_list

def get_filtered_keys_from_object(obj: object, *keys: str) -> Set[str]:
    """
    Get filtered list of object variable names.
    :param keys: List of keys to include. If the first key is "not", the remaining keys will be removed from the class keys.
    :return: List of class keys.
    """
    class_keys = obj.__dict__.keys()
    if not keys:
        return set(class_keys)

    # Remove the passed keys from the class keys.
    if keys[0] == "not":
        return {key for key in class_keys if key not in keys[1:]}
    # Check if all passed keys are valid
    if invalid_keys := set(keys) - class_keys:
        raise ValueError(
            f"Invalid keys: {invalid_keys}",
        )
    # Only return specified keys that are in class_keys
    return {key for key in keys if key in class_keys}

ENGINES = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-4-0613",
    "gpt-4-32k-0613",
    "gpt-4-1106-preview",
    "claude-2-web",
    "claude-2.1",
]

class claudeConversation(dict):
    def Conversation(self, index):
        conversation_list = super().__getitem__(index)
        return "\n\n" + "\n\n".join([f"{item['role']}:{item['content']}" for item in conversation_list]) + "\n\nAssistant:"


class claudebot:
    def __init__(
        self,
        api_key: str,
        engine: str = os.environ.get("GPT_ENGINE") or "claude-2.1",
        temperature: float = 0.5,
        top_p: float = 0.7,
        chat_url: str = "https://api.anthropic.com/v1/complete",
        timeout: float = None,
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
        **kwargs,
    ):
        self.api_key: str = api_key
        self.engine: str = engine
        self.temperature = temperature
        self.top_p = top_p
        self.chat_url = chat_url
        self.timeout = timeout
        self.session = requests.Session()
        self.conversation = claudeConversation()
        self.system_prompt = system_prompt

    def add_to_conversation(
        self,
        message: str,
        role: str,
        convo_id: str = "default",
        pass_history: bool = True,
    ) -> None:
        """
        Add a message to the conversation
        """

        if convo_id not in self.conversation or pass_history == False:
            self.reset(convo_id=convo_id)
        self.conversation[convo_id].append({"role": role, "content": message})

    def reset(self, convo_id: str = "default", system_prompt: str = None) -> None:
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
        tiktoken.model.MODEL_TO_ENCODING["gpt-4"] = "cl100k_base"
        tiktoken.model.MODEL_TO_ENCODING["claude-2-web"] = "cl100k_base"
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
        pass_history = True
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
        # print(repr(self.conversation.Conversation(convo_id)))
        # print("total tokens:", self.get_token_count(convo_id))



class Imagebot:
    def __init__(
        self,
        api_key: str,
        timeout: float = None,
    ):
        self.api_key: str = api_key
        self.engine: str = "dall-e-3"
        self.session = requests.Session()
        self.timeout: float = timeout

    def dall_e_3(
        self,
        prompt: str,
        model: str = None,
        **kwargs,
    ):
        url = config.bot_api_url.image_url
        headers = {"Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"}

        json_post = {
                "model": os.environ.get("IMAGE_MODEL_NAME") or model or self.engine,
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
        }
        response = self.session.post(
            url,
            headers=headers,
            json=json_post,
            timeout=kwargs.get("timeout", self.timeout),
            stream=True,
        )
        if response.status_code != 200:
            raise t.APIConnectionError(
                f"{response.status_code} {response.reason} {response.text}",
            )
        json_data = json.loads(response.text)
        url = json_data["data"][0]["url"]
        yield url

class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        api_key: str,
        engine: str = os.environ.get("GPT_ENGINE") or "gpt-3.5-turbo",
        proxy: str = None,
        timeout: float = None,
        max_tokens: int = None,
        temperature: float = 0.5,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        reply_count: int = 1,
        truncate_limit: int = None,
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        self.engine: str = engine
        self.api_key: str = api_key
        self.system_prompt: str = system_prompt
        self.max_tokens: int = max_tokens or (
            4096
            if "gpt-4-1106-preview" in engine
            else 31000
            if "gpt-4-32k" in engine
            else 7000
            if "gpt-4" in engine
            else 4096
            if "gpt-3.5-turbo-1106" in engine
            else 15000
            if "gpt-3.5-turbo-16k" in engine
            else 99000
            if "claude-2-web" in engine or "claude-2" in engine
            else 4000
        )
        # context max tokens
        self.truncate_limit: int = truncate_limit or (
            16000
            # 126500 Control the number of search characters to prevent excessive spending
            if "gpt-4-1106-preview" in engine
            else 30500
            if "gpt-4-32k" in engine
            else 6500
            if "gpt-4" in engine
            else 14500
            if "gpt-3.5-turbo-16k" in engine or "gpt-3.5-turbo-1106" in engine
            else 98500
            if "claude-2-web" in engine or "claude-2" in engine
            else 3400
        )
        self.temperature: float = temperature
        self.top_p: float = top_p
        self.presence_penalty: float = presence_penalty
        self.frequency_penalty: float = frequency_penalty
        self.reply_count: int = reply_count
        self.timeout: float = timeout
        self.proxy = proxy
        self.session = requests.Session()
        self.session.proxies.update(
            {
                "http": proxy,
                "https": proxy,
            },
        )
        if proxy := (
            proxy or os.environ.get("all_proxy") or os.environ.get("ALL_PROXY") or None
        ):
            if "socks5h" not in proxy:
                self.aclient = httpx.AsyncClient(
                    follow_redirects=True,
                    proxies=proxy,
                    timeout=timeout,
                )
        else:
            self.aclient = httpx.AsyncClient(
                follow_redirects=True,
                proxies=proxy,
                timeout=timeout,
            )

        self.conversation: dict[str, list[dict]] = {
            "default": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
            ],
        }

        if self.get_token_count("default") > self.max_tokens:
            raise t.ActionRefuseError("System prompt is too long")

    def add_to_conversation(
        self,
        message: str,
        role: str,
        convo_id: str = "default",
        function_name: str = "",
    ) -> None:
        """
        Add a message to the conversation
        """
        if function_name == "" and message != "":
            self.conversation[convo_id].append({"role": role, "content": message})
        else:
            self.conversation[convo_id].append({"role": role, "name": function_name, "content": message})

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

    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    def get_token_count(self, convo_id: str = "default") -> int:
        """
        Get token count
        """
        if self.engine not in ENGINES:
            raise NotImplementedError(
                f"Engine {self.engine} is not supported. Select from {ENGINES}",
            )
        tiktoken.model.MODEL_TO_ENCODING["gpt-4"] = "cl100k_base"
        tiktoken.model.MODEL_TO_ENCODING["claude-2-web"] = "cl100k_base"
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

    def get_max_tokens(self, convo_id: str) -> int:
        """
        Get max tokens
        """
        # print("self.max_tokens, self.get_token_count(convo_id)", self.max_tokens, self.get_token_count(convo_id))
        return self.max_tokens - self.get_token_count(convo_id)

    def ask_stream(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        model: str = None,
        pass_history: bool = True,
        function_name: str = "",
        **kwargs,
    ):
        """
        Ask a question
        """
        # Make conversation if it doesn't exist
        if convo_id not in self.conversation or pass_history == False:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, role, convo_id=convo_id, function_name=function_name)
        self.__truncate_conversation(convo_id=convo_id)
        # print(self.conversation[convo_id])
        # Get response
        url = config.bot_api_url.chat_url
        headers = {"Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"}

        if self.engine == "gpt-4-1106-preview":
            model_max_tokens = kwargs.get("max_tokens", self.max_tokens)
        elif self.engine == "gpt-3.5-turbo-1106":
            model_max_tokens = min(kwargs.get("max_tokens", self.max_tokens), self.truncate_limit - self.get_token_count(convo_id))
        else:
            model_max_tokens = min(self.get_max_tokens(convo_id=convo_id) - 500, kwargs.get("max_tokens", self.max_tokens))
        json_post = {
                "model": os.environ.get("MODEL_NAME") or model or self.engine,
                "messages": self.conversation[convo_id] if pass_history else [{"role": "system","content": self.system_prompt},{"role": role, "content": prompt}],
                "stream": True,
                # kwargs
                "temperature": kwargs.get("temperature", self.temperature),
                "top_p": kwargs.get("top_p", self.top_p),
                "presence_penalty": kwargs.get(
                    "presence_penalty",
                    self.presence_penalty,
                ),
                "frequency_penalty": kwargs.get(
                    "frequency_penalty",
                    self.frequency_penalty,
                ),
                "n": kwargs.get("n", self.reply_count),
                "user": role,
                "max_tokens": model_max_tokens,
                # "max_tokens": min(
                #     self.get_max_tokens(convo_id=convo_id),
                #     kwargs.get("max_tokens", self.max_tokens),
                # ),
        }
        json_post.update(function_call_list["base"])
        if config.SEARCH_USE_GPT:
            json_post["functions"].append(function_call_list["web_search"])
        json_post["functions"].append(function_call_list["url_fetch"])
        response = self.session.post(
            url,
            headers=headers,
            json=json_post,
            timeout=kwargs.get("timeout", self.timeout),
            stream=True,
        )
        if response.status_code != 200:
            raise t.APIConnectionError(
                f"{response.status_code} {response.reason} {response.text}",
            )
        response_role: str or None = None
        full_response: str = ""
        function_call_name: str = ""
        need_function_call: bool = False
        for line in response.iter_lines():
            if not line:
                continue
            # Remove "data: "
            line = line.decode("utf-8")[6:]
            if line == "[DONE]":
                break
            resp: dict = json.loads(line)
            choices = resp.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta")
            if not delta:
                continue
            if "role" in delta:
                response_role = delta["role"]
            if "content" in delta and delta["content"]:
                need_function_call = False
                content = delta["content"]
                full_response += content
                yield content
            if "function_call" in delta:
                need_function_call = True
                function_call_content = delta["function_call"]["arguments"]
                if "name" in delta["function_call"]:
                    function_call_name = delta["function_call"]["name"]
                full_response += function_call_content
        if need_function_call:
            max_context_tokens = self.truncate_limit - self.get_token_count(convo_id) - 500
            response_role = "function"
            if function_call_name == "get_search_results":
                prompt = json.loads(full_response)["prompt"]
                # print(self.truncate_limit, self.get_token_count(convo_id), max_context_tokens)
                function_response = eval(function_call_name)(prompt, max_context_tokens)
                function_response = "web search results: \n" + function_response
                yield from self.ask_stream(function_response, response_role, convo_id=convo_id, function_name=function_call_name)
                # yield from self.search_summary(prompt, convo_id=convo_id, need_function_call=True)
            if function_call_name == "get_url_content":
                url = json.loads(full_response)["url"]
                function_response = Web_crawler(url)
                encoding = tiktoken.encoding_for_model(self.engine)
                encode_text = encoding.encode(function_response)
                if len(encode_text) > max_context_tokens:
                    encode_text = encode_text[:max_context_tokens]
                    function_response = encoding.decode(encode_text)
                yield from self.ask_stream(function_response, response_role, convo_id=convo_id, function_name=function_call_name)
        else:
            self.add_to_conversation(full_response, response_role, convo_id=convo_id)
            print("total tokens:", self.get_token_count(convo_id))

    async def ask_stream_async(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        model: str = None,
        pass_history: bool = True,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """
        Ask a question
        """
        # Make conversation if it doesn't exist
        if convo_id not in self.conversation or pass_history == False:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, "user", convo_id=convo_id)
        self.__truncate_conversation(convo_id=convo_id)
        if self.engine == "gpt-4-1106-preview":
            model_max_tokens = kwargs.get("max_tokens", self.max_tokens)
        else:
            model_max_tokens = min(self.get_max_tokens(convo_id=convo_id) - 500, kwargs.get("max_tokens", self.max_tokens))
        # Get response
        async with self.aclient.stream(
            "post",
            config.bot_api_url.chat_url,
            headers={"Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"},
            json={
                "model": model or self.engine,
                "messages": self.conversation[convo_id] if pass_history else [{"role": "system","content": self.system_prompt},{"role": role, "content": prompt}],
                "stream": True,
                # kwargs
                "temperature": kwargs.get("temperature", self.temperature),
                "top_p": kwargs.get("top_p", self.top_p),
                "presence_penalty": kwargs.get(
                    "presence_penalty",
                    self.presence_penalty,
                ),
                "frequency_penalty": kwargs.get(
                    "frequency_penalty",
                    self.frequency_penalty,
                ),
                "n": kwargs.get("n", self.reply_count),
                "user": role,
                "max_tokens": model_max_tokens,
                # "max_tokens": min(
                #     self.get_max_tokens(convo_id=convo_id),
                #     kwargs.get("max_tokens", self.max_tokens),
                # ),
            },
            timeout=kwargs.get("timeout", self.timeout),
        ) as response:
            if response.status_code != 200:
                await response.aread()
                raise t.APIConnectionError(
                    f"{response.status_code} {response.reason_phrase} {response.text}",
                )

            response_role: str = ""
            full_response: str = ""
            async for line in response.aiter_lines():
                line = line.strip()
                if not line:
                    continue
                # Remove "data: "
                line = line[6:]
                if line == "[DONE]":
                    break
                resp: dict = json.loads(line)
                if "error" in resp:
                    raise t.ResponseError(f"{resp['error']}")
                choices = resp.get("choices")
                if not choices:
                    continue
                delta: dict[str, str] = choices[0].get("delta")
                if not delta:
                    continue
                if "role" in delta:
                    response_role = delta["role"]
                if "content" in delta:
                    content: str = delta["content"]
                    full_response += content
                    yield content
        self.add_to_conversation(full_response, response_role, convo_id=convo_id)
        print("total tokens:", self.get_token_count(convo_id))

    async def ask_async(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        model: str = None,
        pass_history: bool = True,
        **kwargs,
    ) -> str:
        """
        Non-streaming ask
        """
        response = self.ask_stream_async(
            prompt=prompt,
            role=role,
            convo_id=convo_id,
            **kwargs,
        )
        full_response: str = "".join([r async for r in response])
        return full_response

    def ask(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        model: str = None,
        pass_history: bool = True,
        **kwargs,
    ) -> str:
        """
        Non-streaming ask
        """
        response = self.ask_stream(
            prompt=prompt,
            role=role,
            convo_id=convo_id,
            model=model,
            pass_history=pass_history,
            **kwargs,
        )
        full_response: str = "".join(response)
        return full_response
    
    def search_summary(
            self,
            prompt: str,
            role: str = "user",
            convo_id: str = "default",
            pass_history: bool = True,
            **kwargs,
        ):

        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, role, convo_id=convo_id)
        self.__truncate_conversation(convo_id=convo_id)

        full_response = yield from search_web_and_summary(prompt, self.engine, self.truncate_limit - self.get_token_count(convo_id))

        self.add_to_conversation(full_response, "assistant", convo_id=convo_id)
        print("total tokens:", self.get_token_count(convo_id))

    def rollback(self, n: int = 1, convo_id: str = "default") -> None:
        """
        Rollback the conversation
        """
        for _ in range(n):
            self.conversation[convo_id].pop()

    def reset(self, convo_id: str = "default", system_prompt: str = None) -> None:
        """
        Reset the conversation
        """
        self.conversation[convo_id] = [
            {"role": "system", "content": system_prompt or self.system_prompt},
        ]

    def save(self, file: str, *keys: str) -> None:
        """
        Save the Chatbot configuration to a JSON file
        """
        with open(file, "w", encoding="utf-8") as f:
            data = {
                key: self.__dict__[key]
                for key in get_filtered_keys_from_object(self, *keys)
            }
            # saves session.proxies dict as session
            # leave this here for compatibility
            data["session"] = data["proxy"]
            del data["aclient"]
            json.dump(
                data,
                f,
                indent=2,
            )

    def load(self, file: Path, *keys_: str) -> None:
        """
        Load the Chatbot configuration from a JSON file
        """
        with open(file, encoding="utf-8") as f:
            # load json, if session is in keys, load proxies
            loaded_config = json.load(f)
            keys = get_filtered_keys_from_object(self, *keys_)

            if (
                "session" in keys
                and loaded_config["session"]
                or "proxy" in keys
                and loaded_config["proxy"]
            ):
                self.proxy = loaded_config.get("session", loaded_config["proxy"])
                self.session = httpx.Client(
                    follow_redirects=True,
                    proxies=self.proxy,
                    timeout=self.timeout,
                    cookies=self.session.cookies,
                    headers=self.session.headers,
                )
                self.aclient = httpx.AsyncClient(
                    follow_redirects=True,
                    proxies=self.proxy,
                    timeout=self.timeout,
                    cookies=self.session.cookies,
                    headers=self.session.headers,
                )
            if "session" in keys:
                keys.remove("session")
            if "aclient" in keys:
                keys.remove("aclient")
            self.__dict__.update({key: loaded_config[key] for key in keys})