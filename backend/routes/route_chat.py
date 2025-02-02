from flask import Blueprint, jsonify, request
import logging
from controllers.controller_chatbot import ChatbotBancario

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Crear Blueprint
url_chatbot = Blueprint('url_chatbot', __name__)

# Instanciar el chatbot
chatbot = ChatbotBancario()

@url_chatbot.route('/chat', methods=['POST', 'GET'])
def chat():
    try:
        if request.method == 'GET':
            return jsonify({
                "mensaje": "Bienvenido a la API del chatbot del Banco de Loja. Usa el método POST para enviar consultas.",
                "code": 200
            }), 200

        # Validar que el request tenga JSON válido
        if not request.is_json:
            return jsonify({
                "error": "Solicitud inválida. El cuerpo debe ser un JSON.",
                "code": 400
            }), 400

        # Obtener datos enviados como JSON
        data = request.get_json()

        # Validar estructura del JSON
        if not isinstance(data, dict) or 'consulta' not in data or not isinstance(data['consulta'], str) or not data['consulta'].strip():
            return jsonify({
                "error": "Solicitud inválida. Debe incluir un campo 'consulta' no vacío.",
                "code": 400
            }), 400

        # Extraer la consulta y procesar la respuesta
        consulta = data['consulta'].strip()
        respuesta = chatbot.procesar_consulta(consulta)

        # Log de la consulta y la respuesta
        logging.info(f"Consulta: {consulta} | Respuesta: {respuesta}")

        return jsonify({
            "respuesta": respuesta,
            "code": 200
        }), 200

    except (KeyError, TypeError, ValueError) as e:
        logging.error(f"Error de solicitud: {str(e)}")
        return jsonify({
            "error": "Solicitud inválida. Revisa el formato del JSON.",
            "code": 400
        }), 400

    except Exception as e:
        logging.exception("Error inesperado en el chatbot")
        return jsonify({
            "error": "Error interno del servidor.",
            "detalle": str(e),
            "code": 500
        }), 500
