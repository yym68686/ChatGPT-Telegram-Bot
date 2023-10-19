import g4f
from typing import Optional, List
from langchain.llms.base import LLM
from langchain.agents import AgentType, load_tools, initialize_agent

class EducationalLLM(LLM):

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        out = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
        )  #
        if stop:
            stop_indexes = (out.find(s) for s in stop if s in out)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                out = out[:min_stop]
        return out


llm = EducationalLLM()
# print(llm("今天的微博热搜有哪些？"))
tools = load_tools(["ddg-search", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("今天的微博热搜有哪些？")


# def duckduckgo_search(searchtext, model="gpt-3.5-turbo", temperature=0.5):
#     llm = ChatOpenAI(temperature=temperature, openai_api_base='https://api.ohmygpt.com/v1/', model_name=model, openai_api_key=API)
#     tools = load_tools(["ddg-search", "llm-math"], llm=llm)
#     agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
#     result = agent.run(searchtext)

#     en2zh_prompt = PromptTemplate(
#         input_variables=["targetlang", "text"],
#         template="You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {targetlang}, please do not explain any sentences, just translate or leave them as they are.: {text}",
#     )
#     chain = LLMChain(llm=llm, prompt=en2zh_prompt)
#     return chain.run({"targetlang": "simplified chinese", "text": result})

# if __name__ == "__main__":
#     os.system("clear")
#     print(duckduckgo_search("夏威夷火灾死了多少人？"))
 

# prompt = PromptTemplate(
#     input_variables=["product"],
#     template="What is a good name for a company that makes {product}? Just tell one and only the name",
# )

# chain = LLMChain(llm=llm, prompt=prompt)

# print(chain.run("colorful socks"))