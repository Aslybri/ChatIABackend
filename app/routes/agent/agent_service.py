import os
from dotenv import load_dotenv
from openai import OpenAI
from app.conversation_memory import memory

# Cargar las variables del archivo .env
load_dotenv()


class AgentService:


    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("No hay una ApiKey configurada")

        self.client = OpenAI(api_key=api_key)

        self.memory = memory


    def generate_text(self, prompt: str, conversation_id: str) -> str:

        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")

        # 1. Crear la memoria si la conversación es nueva
        if conversation_id not in self.memory:
            self.memory[conversation_id] = []

        # 2. Guardar la pregunta del usuario
        self.memory[conversation_id].append({
            "role": "user",
            "content": prompt
        })

        # 3. Enviar la conversación a OpenAI
        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=self.memory[conversation_id]
        )

        # 4. Obtener la respuesta
        response_text = response.output_text

        # 5. Guardar la respuesta en memoria
        self.memory[conversation_id].append({
            "role": "assistant",
            "content": response_text
        })

        # 6. Mostrar la memoria en consola
        print("\nMEMORIA DE LA CONVERSACIÓN")

        for message in self.memory[conversation_id]:
            print(message["role"], ":", message["content"])

        print("--------------------------------")

        # 7. Devolver la respuesta
        return response_text
    
    def get_agents(self):

        agents = [
            {
                "id": "text",
                "name": "Agente de texto",
                "description": "Permite realizar preguntas y mantener conversaciones."
            }
        ]

        return agents