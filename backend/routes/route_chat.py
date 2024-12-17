from controllers.controller_chatbot import Chatbot
from flask import Blueprint, jsonify, request

# Define el blueprint para las rutas del chatbot
url_chatbot = Blueprint('url_chatbot', __name__)

# Instancia del chatbot
chatbot = Chatbot()

@url_chatbot.route('/chat', methods=['POST'])
def chat():
    try:
        # Obtiene los datos enviados como JSON
        data = request.get_json()
        
        # Valida que los datos sean correctos
        if not data or 'consulta' not in data:
            return jsonify({
                "error": "Solicitud inválida. Debe incluir el campo 'consulta'.",
                "code": 400
            }), 400

        # Procesa la consulta
        consulta = data['consulta']
        respuesta = chatbot.procesar_consulta(consulta)

        # Devuelve la respuesta en formato JSON
        return jsonify({
            "respuesta": respuesta,
            "code": 200
        }), 200

    except Exception as e:
        # Manejo de errores inesperados
        return jsonify({
            "error": f"Ha ocurrido un error: {str(e)}",
            "code": 500
        }), 500
    