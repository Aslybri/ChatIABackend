from flask import request, jsonify

from .vision_service import VisionService


class VisionController:

    def __init__(self):
        self.vision_service = VisionService()

    def analyze_image_controller(self):

        try:
            # Obtener los datos del formulario
            prompt = request.form.get("prompt")
            image = request.files.get("image")
            conversation_id = request.form.get(
                "conversation_id"
            )

            # Validar el prompt
            if not prompt or not prompt.strip():
                return jsonify({
                    "ok": False,
                    "message": "Debe enviar un prompt"
                }), 400

            # Validar la imagen
            if image is None:
                return jsonify({
                    "ok": False,
                    "message": "Debe enviar una imagen"
                }), 400

            # Validar la conversación
            if not conversation_id or not conversation_id.strip():
                return jsonify({
                    "ok": False,
                    "message": "Debe enviar un conversation_id"
                }), 400

            # Llamar al servicio
            response = self.vision_service.analyze_image(
                image,
                prompt,
                conversation_id
            )

            return jsonify({
                "ok": True,
                "message": "Análisis realizado con éxito",
                "response": response,
                "conversation_id": conversation_id
            }), 200

        except ValueError as error:
            return jsonify({
                "ok": False,
                "message": str(error)
            }), 400

        except Exception:
            return jsonify({
                "ok": False,
                "message": "Ocurrió un error al analizar la imagen"
            }), 500