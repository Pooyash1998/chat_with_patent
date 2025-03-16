from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_chroma import Chroma
import streamlit as st
import torch
import os

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 
os.environ["TOKENIZERS_PARALLELISM"] = "false"

CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma")
if not os.path.exists(CHROMA_PATH):
     os.makedirs(CHROMA_PATH)

def get_llm():
    api_key = st.session_state.get("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set the API KEY")
        return None
    try:
        return ChatOpenAI(api_key=api_key, model=st.session_state.get("model_name", "gpt-4o"))
    except Exception as e:
        st.error(f"Error with OpenAI API: {str(e)}")
        return None
def load__and_split_docs(document_path):
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
def construct_prompt():
    system_message = """
            You are an expert in patent analysis, and your task is to answer complex questions about a specific patent.

            Assume that all questions relate to the patent linked in the application.

            Keep your answers:
            - Objective and fact-based
            - Limited to the information contained in the provided patent
            - Clearly structured and easy to understand
            - Polite and professional

            Important:
            - You must always respond in English.
            - If a question does not require specific patent details (e.g., general questions about patents), you may rely on your broader knowledge.
            - If you are unsure, openly admit it.
            - Do not invent information.
            - Stick strictly to the content of the patent document.
            - Acknowledge when you do not know something.
            - If in doubt, refer the user to the official patent office or a patent attorney.

            Structure your answers in a clear and readable way.
        """
    prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_message),
    MessagesPlaceholder(variable_name="history"),
    ("system", "Retrieved Information from RAG: {context}"),
    ("user", "User Input: {user_input}")
    ])
    return prompt_template

def get_chain(file_name=None):
    loaded_patent = st.session_state.get("LOADED_PATENT")
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3",
                                          model_kwargs={"device": "cpu"}, 
                                          show_progress=True, encode_kwargs={"batch_size":32})
    vectordb = Chroma(persist_directory=CHROMA_PATH,embedding_function=embedding_model)
    if loaded_patent != file_name and not already_indexed(vectordb, file_name):
        st.write("Indexing new patent...")
        vectordb.delete_collection()
        chunks = load__and_split_docs(file_name)
        vectordb = Chroma.from_documents(documents=chunks, embedding=embedding_model, persist_directory=CHROMA_PATH)
        st.session_state["LOADED_PATENT"] = file_name
    else:
        st.write("Patent already indexed.")
    
    retriever = vectordb.as_retriever()
    st.session_state["retriever"] = retriever
    # Set up memory
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    st.session_state["msgs"] = msgs
    if not msgs.messages:
        msgs.add_ai_message("How can I help you?")


    # Set up the LangChain, passing in Message History
    prompt = construct_prompt()
    llm = get_llm()
    rag_chain = prompt | llm | StrOutputParser()
    chain_with_history = RunnableWithMessageHistory(
    rag_chain,
    lambda session_id: msgs,
    input_messages_key="user_input",
    history_messages_key="history",
    )
    return chain_with_history