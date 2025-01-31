from flask import Blueprint, jsonify, request
import logging
from controllers.controller_chatbot import ChatbotBancario

logging.basicConfig(level=logging.INFO)

url_chatbot = Blueprint('url_chatbot', __name__)

chatbot = ChatbotBancario()

@url_chatbot.route('/chat', methods=['POST', 'GET'])
def chat():
    try:
        if request.method == 'GET':
            return jsonify({
                "mensaje": "Bienvenido a la API del chatbot del Banco de Loja. Usa el método POST para enviar consultas.",
                "code": 200
            }), 200

        # Obtiene los datos enviados como JSON
        data = request.get_json()

        # Validar que se reciba un JSON y que tenga la clave 'consulta'
        if not data or 'consulta' not in data or not isinstance(data['consulta'], str) or not data['consulta'].strip():
            return jsonify({
                "error": "Solicitud inválida. Debe incluir un campo 'consulta' no vacío.",
                "code": 400
            }), 400

        # Extrae la consulta y procesa la respuesta
        consulta = data['consulta'].strip()
        respuesta = chatbot.procesar_consulta(consulta)

        logging.info(f"Consulta: {consulta} | Respuesta: {respuesta}")

        return jsonify({
            "respuesta": respuesta,
            "code": 200
        }), 200

    except KeyError:
        return jsonify({
            "error": "Solicitud inválida. Falta el campo 'consulta'.",
            "code": 400
        }), 400

    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}",
            "code": 500
        }), 500
