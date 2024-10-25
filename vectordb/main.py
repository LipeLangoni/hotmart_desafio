from fastapi import FastAPI
from utils import generate_vectorstore_from_url, chunk_in_topics, generate_vector_store
from schemas.Inputvector import InputGenerate

app = FastAPI()

@app.on_event("startup")
async def startup():
    generate_vectorstore_from_url(["https://hotmart.com/pt-br/blog/como-funciona-hotmart"])

@app.post("/generate_vectorstore")
def chat(input:InputGenerate):
    chunks = chunk_in_topics(input.text)
    try:
        generate_vector_store(chunks)
        return {"status": "200"}
    except Exception as e:
        return {"error":e}

@app.get("/health")
def health():
    return "Ok"
