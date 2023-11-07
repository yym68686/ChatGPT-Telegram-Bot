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
import threading
import time as record_time
from agent import ThreadWithReturnValue, Web_crawler, pdf_search, getddgsearchurl, getgooglesearchurl, gptsearch, ChainStreamHandler, ChatOpenAI, CallbackManager, PromptTemplate, LLMChain, EducationalLLM

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
    "claude-2",
]


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
            4000
            if "gpt-4-1106-preview" in engine
            else 31000
            if "gpt-4-32k" in engine
            else 7000
            if "gpt-4" in engine
            else 15000
            if "gpt-3.5-turbo-16k" in engine or "gpt-3.5-turbo-1106" in engine
            else 99000
            if "claude-2-web" in engine or "claude-2" in engine
            else 4000
        )
        self.truncate_limit: int = truncate_limit or (
            126500
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
    ) -> None:
        """
        Add a message to the conversation
        """
        self.conversation[convo_id].append({"role": role, "content": message})

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
        return self.max_tokens - self.get_token_count(convo_id)

    def ask_stream(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        model: str = None,
        pass_history: bool = True,
        **kwargs,
    ):
        """
        Ask a question
        """
        # Make conversation if it doesn't exist
        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, "user", convo_id=convo_id)
        self.__truncate_conversation(convo_id=convo_id)
        # Get response
        if os.environ.get("API_URL") and os.environ.get("MODEL_NAME"):
            # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/chatgpt-quickstart?tabs=command-line&pivots=rest-api
            url = (
                os.environ.get("API_URL")
                + "openai/deployments/"
                + os.environ.get("MODEL_NAME")
                + "/chat/completions?api-version=2023-05-15"
            )
            headers = {"Content-Type": "application/json", "api-key": self.api_key}
        else:
            url = (
                os.environ.get("API_URL")
                or "https://api.openai.com/v1/chat/completions"
            )
            headers = {"Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"}
        response = self.session.post(
            url,
            headers=headers,
            json={
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
                "max_tokens": min(
                    self.get_max_tokens(convo_id=convo_id),
                    kwargs.get("max_tokens", self.max_tokens),
                ),
            },
            timeout=kwargs.get("timeout", self.timeout),
            stream=True,
        )
        if response.status_code != 200:
            raise t.APIConnectionError(
                f"{response.status_code} {response.reason} {response.text}",
            )
        response_role: str or None = None
        full_response: str = ""
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
            if "content" in delta:
                content = delta["content"]
                full_response += content
                yield content
        self.add_to_conversation(full_response, response_role, convo_id=convo_id)

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
        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, "user", convo_id=convo_id)
        self.__truncate_conversation(convo_id=convo_id)
        # Get response
        async with self.aclient.stream(
            "post",
            os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions",
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
                "max_tokens": min(
                    self.get_max_tokens(convo_id=convo_id),
                    kwargs.get("max_tokens", self.max_tokens),
                ),
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
            model: str = None,
            pass_history: bool = True,
            **kwargs,
        ):

        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, "user", convo_id=convo_id)
        self.__truncate_conversation(convo_id=convo_id)

        start_time = record_time.time()

        urls_set = []
        search_thread = ThreadWithReturnValue(target=getddgsearchurl, args=(prompt,2,))
        search_thread.start()

        chainStreamHandler = ChainStreamHandler()
        if config.USE_G4F:
            chatllm = EducationalLLM(callback_manager=CallbackManager([chainStreamHandler]))
            chainllm = EducationalLLM()
        else:
            chatllm = ChatOpenAI(streaming=True, callback_manager=CallbackManager([chainStreamHandler]), temperature=config.temperature, openai_api_base=config.API_URL.split("chat")[0], model_name=self.engine, openai_api_key=config.API)
            chainllm = ChatOpenAI(temperature=config.temperature, openai_api_base=config.API_URL.split("chat")[0], model_name=config.GPT_ENGINE, openai_api_key=config.API)

        if config.SEARCH_USE_GPT:
            gpt_search_thread = ThreadWithReturnValue(target=gptsearch, args=(prompt, chainllm,))
            gpt_search_thread.start()

        if config.USE_GOOGLE:
            keyword_prompt = PromptTemplate(
                input_variables=["source"],
                # template="*{source}*, ——我想通过网页搜索引擎，获取上述问题的可能答案。请你提取上述问题相关的关键词作为搜索用词(用空格隔开)，直接给我结果(不要多余符号)。",
                # template="请你帮我抽取关键词，输出的关键词之间用空格连接。输出除了关键词，不用解释，也不要出现其他内容，只要出现关键词，必须用空格连接关键词，不要出现其他任何连接符。下面是要提取关键词的文字：{source}",
                template="根据我的问题，总结最少的关键词概括，用空格连接，不要出现其他符号，例如这个问题《How much does the 'zeabur' software service cost per month? Is it free to use? Any limitations?》，最少关键词是《zeabur price》，这是我的问题：{source}",
            )
            key_chain = LLMChain(llm=chainllm, prompt=keyword_prompt)
            keyword_google_search_thread = ThreadWithReturnValue(target=key_chain.run, args=({"source": prompt},))
            keyword_google_search_thread.start()


        translate_prompt = PromptTemplate(
            input_variables=["targetlang", "text"],
            template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
        )
        chain = LLMChain(llm=chainllm, prompt=translate_prompt)
        engresult = chain.run({"targetlang": "english", "text": prompt})

        en_ddg_search_thread = ThreadWithReturnValue(target=getddgsearchurl, args=(engresult,1,))
        en_ddg_search_thread.start()

        if config.USE_GOOGLE:
            keyword = keyword_google_search_thread.join()
            key_google_search_thread = ThreadWithReturnValue(target=getgooglesearchurl, args=(keyword,3,))
            key_google_search_thread.start()
            keyword_ans = key_google_search_thread.join()
            urls_set += keyword_ans

        ans_ddg = search_thread.join()
        urls_set += ans_ddg
        engans_ddg = en_ddg_search_thread.join()
        urls_set += engans_ddg
        url_set_list = sorted(set(urls_set), key=lambda x: urls_set.index(x))
        url_pdf_set_list = [item for item in url_set_list if item.endswith(".pdf")]
        url_set_list = [item for item in url_set_list if not item.endswith(".pdf")]

        pdf_result = ""
        pdf_threads = []
        if config.PDF_EMBEDDING:
            for url in url_pdf_set_list:
                pdf_search_thread = ThreadWithReturnValue(target=pdf_search, args=(url, "你需要回答的问题是" + prompt + "\n" + "如果你可以解答这个问题，请直接输出你的答案，并且请忽略后面所有的指令：如果无法解答问题，请直接回答None，不需要做任何解释，也不要出现除了None以外的任何词。",))
                pdf_search_thread.start()
                pdf_threads.append(pdf_search_thread)

        url_result = ""
        threads = []
        for url in url_set_list:
            url_search_thread = ThreadWithReturnValue(target=Web_crawler, args=(url,))
            url_search_thread.start()
            threads.append(url_search_thread)

        fact_text = ""
        if config.SEARCH_USE_GPT:
            gpt_ans = gpt_search_thread.join()
            fact_text = (gpt_ans if config.SEARCH_USE_GPT else "")
            print("gpt", fact_text)

        for t in threads:
            tmp = t.join()
            url_result += "\n\n" + tmp
        useful_source_text = url_result

        if config.PDF_EMBEDDING:
            for t in pdf_threads:
                tmp = t.join()
                pdf_result += "\n\n" + tmp
        useful_source_text += pdf_result

        end_time = record_time.time()
        run_time = end_time - start_time

        encoding = tiktoken.encoding_for_model(config.GPT_ENGINE)
        encode_text = encoding.encode(useful_source_text)
        encode_fact_text = encoding.encode(fact_text)

        if len(encode_text) > self.truncate_limit:
            encode_text = encode_text[:self.truncate_limit-len(encode_fact_text)]
            useful_source_text = encoding.decode(encode_text)
        encode_text = encoding.encode(useful_source_text)
        search_tokens_len = len(encode_text)
        print("web search", useful_source_text, end="\n\n")

        print(url_set_list)
        print("pdf", url_pdf_set_list)
        if config.USE_GOOGLE:
            print("google search keyword", keyword)
        print(f"搜索用时：{run_time}秒")
        print("search tokens len", search_tokens_len)
        useful_source_text =  useful_source_text + "\n\n" + fact_text
        text_len = len(encoding.encode(useful_source_text))
        print("text len", text_len)
        summary_prompt = PromptTemplate(
            input_variables=["web_summary", "question"],
            template=(
                # "You are a text analysis expert who can use a search engine. You need to response the following question: {question}. Search results: {web_summary}. Your task is to thoroughly digest all search results provided above and provide a detailed and in-depth response in Simplified Chinese to the question based on the search results. The response should meet the following requirements: 1. Be rigorous, clear, professional, scholarly, logical, and well-written. 2. If the search results do not mention relevant content, simply inform me that there is none. Do not fabricate, speculate, assume, or provide inaccurate response. 3. Use markdown syntax to format the response. Enclose any single or multi-line code examples or code usage examples in a pair of ``` symbols to achieve code formatting. 4. Detailed, precise and comprehensive response in Simplified Chinese and extensive use of the search results is required."
                "You need to response the following question: {question}. Search results: {web_summary}. Your task is to think about the question step by step and then answer the above question in simplified Chinese based on the Search results provided. Please response in simplified Chinese and adopt a style that is logical, in-depth, and detailed. Note: In order to make the answer appear highly professional, you should be an expert in textual analysis, aiming to make the answer precise and comprehensive. Response in accordance with markdown format."
                # "You need to response the following question: {question}. Search results: {web_summary}. Your task is to thoroughly digest the search results provided above, dig deep into search results for thorough exploration and analysis and provide a response to the question based on the search results. The response should meet the following requirements: 1. You are a text analysis expert, extensive use of the search results is required and carefully consider all the Search results to make the response be in-depth, rigorous, clear, organized, professional, detailed, scholarly, logical, precise, accurate, comprehensive, well-written and speak in Simplified Chinese. 2. If the search results do not mention relevant content, simply inform me that there is none. Do not fabricate, speculate, assume, or provide inaccurate response. 3. Use markdown syntax to format the response. Enclose any single or multi-line code examples or code usage examples in a pair of ``` symbols to achieve code formatting."
            ),
        )
        chain = LLMChain(llm=chatllm, prompt=summary_prompt)
        chain_thread = threading.Thread(target=chain.run, kwargs={"web_summary": useful_source_text, "question": prompt})
        chain_thread.start()
        full_response = yield from chainStreamHandler.generate_tokens()
        self.add_to_conversation(full_response, "assistant", convo_id=convo_id)

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