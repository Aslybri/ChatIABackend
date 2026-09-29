import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.conversation_memory import memory

load_dotenv()


class VisionService:

    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    MAX_IMAGE_SIZE = 10 * 1024 * 1024

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("No hay una API Key configurada")

        self.client = OpenAI(api_key=api_key)
        self.memory = memory

    def analyze_image(
        self,
        image_file,
        prompt: str,
        conversation_id: str
    ) -> str:

        # 1. Validar el prompt
        if not prompt or not prompt.strip():
            raise ValueError("Debe enviar un prompt")

        # 2. Validar la imagen
        if image_file is None:
            raise ValueError("Debe enviar una imagen")

        # 3. Validar la conversación
        if not conversation_id or not conversation_id.strip():
            raise ValueError("Debe enviar un conversation_id")

        # 4. Validar el formato
        mime_type = image_file.mimetype

        if mime_type not in self.ALLOWED_MIME_TYPES:
            raise ValueError(
                "Formato no permitido. Use JPG, PNG o WEBP."
            )

        # 5. Leer la imagen
        image_bytes = image_file.read()

        if not image_bytes:
            raise ValueError("La imagen está vacía")

        if len(image_bytes) > self.MAX_IMAGE_SIZE:
            raise ValueError(
                "La imagen excede el límite de 10 MB"
            )

        # 6. Convertir la imagen a Base64
        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        data_url = f"data:{mime_type};base64,{image_base64}"

        # 7. Preparar el mensaje
        user_message = {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": prompt
                },
                {
                    "type": "input_image",
                    "image_url": data_url
                }
            ]
        }

        # 8. Recuperar el historial
        history = self.memory.get(
            conversation_id, []
        )

        # 9. Enviar el historial y la imagen a OpenAI
        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=history + [user_message]
        )

        response_text = response.output_text

        # 10. Guardar la conversación
        if conversation_id not in self.memory:
            self.memory[conversation_id] = []

        self.memory[conversation_id].append(
            user_message
        )

        self.memory[conversation_id].append({
            "role": "assistant",
            "content": response_text
        })

        # 11. Mostrar la memoria en consola
        print("\nMEMORIA DE LA CONVERSACIÓN")

        for message in self.memory[conversation_id]:
            if message["role"] == "user":
                print("Usuario:", "[Mensaje o imagen]")
            else:
                print("Asistente:", message["content"])

        print("--------------------------------")

        return response_text