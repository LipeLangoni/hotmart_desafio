from fastapi import FastAPI
from fastapi import HTTPException
from langchain_ollama.llms import OllamaLLM
from chain import RagChain
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
import logging
import ollama
from langchain_openai import ChatOpenAI
from schemas.chat import ChatInput

openai_api_key = os.getenv('OPENAI_API_KEY')

# client = Client(host='http://ollama:11434')
# client.pull('llama3.2:1b')

# os.environ["OLLAMA_HOST"] = "http://ollama:11434"
#ollama.pull('llama3.2:1b')

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key,model="text-embedding-3-small")

#llm = OllamaLLM(model="llama3.2:1b")
llm = ChatOpenAI(openai_api_key=openai_api_key,model="gpt-4o-mini", temperature=0)

vectorstore = Chroma(embedding_function=embeddings, persist_directory="data/")

chain = RagChain(llm, vectorstore)

app = FastAPI()

@app.post("/chat")
async def chat(input: ChatInput):
    logging.info(f"Received input: {input}")
    try:
        result = await chain.ainvoke(input.text)
        logging.info(f"Response from chain: {result}")
        return {"result": result}
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return "Ok"
