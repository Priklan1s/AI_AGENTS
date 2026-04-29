from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

def get_retriever():

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectordb = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings
    )

    return vectordb.as_retriever()