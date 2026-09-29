from flask import request, jsonify
from .agent_service import AgentService


class AgentController:

    def __init__(self):
        self.agent_service = AgentService()

    def generate_text_controller(self):

        try:
            # 1. Obtener el JSON enviado por Angular
            data = request.get_json(silent=True)

            # 2. Validar que se enviaron los datos
            if not isinstance(data, dict):
                return jsonify({
                    "error": "Debes enviar un JSON válido"
                }), 400

            # 3. Obtener el prompt y el ID de la conversación
            prompt = data.get("prompt")
            conversation_id = data.get("conversation_id")

            # 4. Validar el prompt
            if not isinstance(prompt, str) or not prompt.strip():
                return jsonify({
                    "error": "El campo 'prompt' es obligatorio"
                }), 400

            # 5. Validar el ID de la conversación
            if not isinstance(conversation_id, str) or not conversation_id.strip():
                return jsonify({
                    "error": "El campo 'conversation_id' es obligatorio"
                }), 400

            # 6. Llamar al servicio
            response_text = self.agent_service.generate_text(
                prompt,
                conversation_id
            )

            # 7. Devolver la respuesta a Angular
            return jsonify({
                "response": response_text,
                "conversation_id": conversation_id
            }), 200

        except ValueError as ve:
            return jsonify({
                "error": str(ve)
            }), 400

        except Exception:
            return jsonify({
                "error": "No se pudo generar la respuesta"
            }), 500