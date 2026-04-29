from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader


def build_vector_db():

    loader = DirectoryLoader(
        "knowledge",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectordb = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="./vector_db"
    )

    vectordb.persist()

    print("Vector DB создана")


def get_vector_db():

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectordb = Chroma(
        persist_directory="./vector_db",
        embedding_function=embeddings
    )

    return vectordb