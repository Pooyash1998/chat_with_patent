from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_docs(document_path):
    loader = PyPDFLoader(document_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    return text_splitter.split_documents(documents)

def already_indexed(vectordb, file_name):
    indexed_sources = set(
        x["source"] for x in vectordb.get(include=["metadatas"])["metadatas"]
    )
    if file_name in indexed_sources:
        return True
    else:
        return False
    
def download_pdf():
    patent_downloader = PatentDownloader()
    patent_downloader.download(patent=patent_number)
    return "{}.pdf".format(patent_number)
