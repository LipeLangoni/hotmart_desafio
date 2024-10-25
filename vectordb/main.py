from fastapi import FastAPI
from utils import generate_vectorstore_from_url

app = FastAPI()

@app.on_event("startup")
async def startup():
    generate_vectorstore_from_url(["https://hotmart.com/pt-br/blog/como-funciona-hotmart"])

@app.get("/generate_vectorstore")
def generate_vectorstore():
    try:
        generate_vectorstore_from_url(["https://hotmart.com/pt-br/blog/como-funciona-hotmart"])
        return {"status": "200"}
    
    except Exception as e:
        return {"error":e}

@app.get("/health")
def health():
    return "Ok"
