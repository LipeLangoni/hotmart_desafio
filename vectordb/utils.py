import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
import os


def load_documents(urls):
    """Load documents from the given URLs using AsyncHtmlLoader.

    Args:
        urls (list): A list of URLs to load documents from.

    Returns:
        list: A list of loaded documents.
    """
    loader = AsyncHtmlLoader(urls)
    return loader.load()

def transform_documents(docs):
    """Transform HTML documents into plain text.

    Args:
        docs (list): A list of HTML documents.

    Returns:
        list: A list of transformed plain text documents.
    """
    html2text = Html2TextTransformer()
    return html2text.transform_documents(docs)

def split_documents(docs):
    """Split documents into smaller chunks.

    Args:
        docs (list): A list of plain text documents.

    Returns:
        list: A list of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs

def chunk_in_topics(text):
    topics = text.split('##')
    topics = [topic.strip() for topic in topics if topic.strip()]
    
    return topics

def get_documents(topics):
    return [Document(
            page_content=topic,
            metadata={"source": "hotmart"},
            id=index,
        ) for index,topic in enumerate(topics)]

def generate_vector_store(docs, save_directory="data/"):
    """Generate and persist a Chroma database from the given document chunks.

    Args:
        docs (list): A list of document chunks.
        save_directory (str): The directory where the vector store will be saved.

    Returns:
        Chroma: The generated vector store.
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key,model="text-embedding-3-small")
    vector_store = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=save_directory)
    return vector_store

def generate_vectorstore_from_url(urls, save_directory="data/"):
    """Pipeline to generate a Chroma database from the given URLs.

    Args:
        urls (list): A list of URLs to process.
        save_directory (str): The directory where the vector store will be saved.

    Returns:
        Chroma: The generated vector store.
    """
    docs = load_documents(urls)
    docs_transformed = transform_documents(docs)
    combined_content = "\n".join(doc.page_content for doc in docs_transformed)
    chunks = chunk_in_topics(combined_content)
    vector_store = generate_vector_store(get_documents(chunks), save_directory)
    return vector_store

