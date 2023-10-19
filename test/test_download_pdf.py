# import requests
# import urllib.parse
# import os
# import sys
# sys.path.append(os.getcwd())
# import config

# from langchain.chat_models import ChatOpenAI
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.document_loaders import UnstructuredPDFLoader
# from langchain.chains import RetrievalQA


# def get_doc_from_url(url):
#     filename = urllib.parse.unquote(url.split("/")[-1])
#     response = requests.get(url, stream=True)
#     with open(filename, 'wb') as f:
#         for chunk in response.iter_content(chunk_size=1024):
#             f.write(chunk)
#     return filename

# def pdf_search(docurl, query_message, model="gpt-3.5-turbo"):
#     chatllm = ChatOpenAI(temperature=0.5, openai_api_base=config.API_URL.split("chat")[0], model_name=model, openai_api_key=os.environ.get('API', None))
#     embeddings = OpenAIEmbeddings(openai_api_base=config.API_URL.split("chat")[0], openai_api_key=os.environ.get('API', None))
#     filename = get_doc_from_url(docurl)
#     docpath = os.getcwd() + "/" + filename
#     loader = UnstructuredPDFLoader(docpath)
#     print(docpath)
#     documents = loader.load()
#     os.remove(docpath)
#     # 初始化加载器
#     text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=25)
#     # 切割加载的 document
#     split_docs = text_splitter.split_documents(documents)
#     vector_store = Chroma.from_documents(split_docs, embeddings)
#     # 创建问答对象
#     qa = RetrievalQA.from_chain_type(llm=chatllm, chain_type="stuff", retriever=vector_store.as_retriever(),return_source_documents=True)
#     # 进行问答
#     result = qa({"query": query_message})
#     return result['result']

# pdf_search("https://www.nsfc.gov.cn/csc/20345/22468/pdf/2001/%E5%86%BB%E7%BB%93%E8%A3%82%E9%9A%99%E7%A0%82%E5%B2%A9%E4%BD%8E%E5%91%A8%E5%BE%AA%E7%8E%AF%E5%8A%A8%E5%8A%9B%E7%89%B9%E6%80%A7%E8%AF%95%E9%AA%8C%E7%A0%94%E7%A9%B6.pdf", "端水实验的目的是什么？")

from PyPDF2 import PdfReader

def has_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        page = pdf.pages[0]
        text = page.extract_text()
        return text

pdf_path = '/Users/yanyuming/Downloads/GitHub/ChatGPT-Telegram-Bot/冻结裂隙砂岩低周循环动力特性试验研究.pdf'
print(has_text(pdf_path))