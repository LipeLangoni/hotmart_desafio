from locust import HttpUser, TaskSet, task, between
from pydantic import BaseModel
import random

class ChatInput(BaseModel):
    text: str

class ChatUser(HttpUser):
    wait_time = between(1, 2)  

    @task
    def chat(self):

        input_data = ChatInput(text=self.generate_random_text())
        response = self.client.post("/chat", json=input_data.dict())

        if response.status_code == 200:
            print("Chat response:", response.json())
        else:
            print("Error response:", response.text)

    def generate_random_text(self):

        examples = [
            "como vender com a hotmart?",
            "Como funciona a automação de nota fiscal?",
            "Quais são as formas de pagamento?",
            "como funciona o sistema de comissões na Hotmart?"
        ]
        return random.choice(examples)

# Para executar os testes, use o comando:
# locust -f path_to_this_file.py --host=http://localhost:8000
