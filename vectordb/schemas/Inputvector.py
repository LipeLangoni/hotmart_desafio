from pydantic import BaseModel

class InputGenerate(BaseModel):
    text: str