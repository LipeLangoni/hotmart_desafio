import os
import pytest
from unittest.mock import patch, MagicMock
from utils import chunk_in_topics,get_documents,transform_documents
from langchain.schema.document import Document


def test_chunk_in_topics():
    text = "Topic 1##Topic 2##Topic 3"
    chunks = chunk_in_topics(text)
    
    assert len(chunks) == 3
    assert chunks == ["Topic 1", "Topic 2", "Topic 3"]


def test_get_documents():
    topics = ["Chunk 1", "Chunk 2"]
    documents = get_documents(topics)
    
    assert len(documents) == 2
    assert documents[0].page_content == "Chunk 1"
    assert documents[0].metadata == {"source": "hotmart"}


def test_transform_documents():
    html_docs = [
        Document(page_content="<html><body><h1>Title</h1><p>Document content.</p></body></html>"),
    ]
    
    transformed_docs = transform_documents(html_docs)

    assert len(transformed_docs) == 1
    assert transformed_docs[0].page_content == '# Title\n\nDocument content.\n\n'