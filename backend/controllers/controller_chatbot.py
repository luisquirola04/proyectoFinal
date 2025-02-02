import spacy
import re
import logging
#python3 -m spacy download es_core_news_lg

class ChatbotBancario:
    def __init__(self):
        # Configuración del logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("ChatbotBancario")

        # Cargar modelo de lenguaje de spaCy para español
        self.nlp = spacy.load("es_core_news_lg")
        
        # Definición de estados
        self.estados = {
            "inicio": self.estado_inicio,
            "ubicacion": self.estado_ubicacion,
            "horario": self.estado_horario,
            "cuenta": self.estado_cuenta,
            "tarjeta": self.estado_tarjeta,
            "prestamo": self.estado_prestamo,
            "transferencia": self.estado_transferencia,
            "bloqueo": self.estado_bloqueo,
            "estado_cuenta": self.estado_estado_cuenta,
            "pagos": self.estado_pagos,
            "soporte": self.estado_soporte,
            "desconocido": self.estado_desconocido,
        }
        self.estado_actual = "inicio"
        
        # Palabras clave por estado y subcategorías
        self.patrones = {
            "ubicacion": {
                "direccion": [
                    "dónde están ubicados", "dónde", "sucursal", "dirección", "ubicación", "cómo llegar",
                    "oficinas", "están en", "donde puedo encontrarlos", "sucursales cerca", "tiendas", 
                    "donde queda", "donde están", "donde tienen oficinas", "direcciones disponibles"
                ]
            },
            "horario": {
                "horas_atencion": [
                    "horario", "hora de apertura", "hora de cierre", "apertura", "cierre", "horarios",
                    "qué horario tienen", "horas de atención", "atención al cliente", "a qué hora abren",
                    "a qué hora cierran", "horarios disponibles", "días y horarios", "cuando abren",
                    "cuando cierran", "horario atención", "horario del banco"
                ]
            },
            "cuenta": {
                "abrir": [
                    "abrir cuenta", "registrar cuenta", "cómo abrir una cuenta", "nueva cuenta", 
                    "qué necesito para una cuenta", "requisitos cuenta", "registrarme", "crear cuenta", 
                    "necesito una cuenta", "quiero abrir una cuenta", "hacer una cuenta", 
                    "registrar una nueva cuenta", "qué requisitos tienen para abrir cuenta"
                ],
                "cerrar": [
                    "cerrar cuenta", "cómo cerrar mi cuenta", "quiero eliminar mi cuenta", "cancelar cuenta",
                    "dar de baja cuenta", "terminar cuenta", "cómo cierro mi cuenta"
                ]
            },
            "tarjeta": {
                "informacion": [
                    "información tarjeta", "detalles tarjeta", "qué tarjetas tienen", "tipos de tarjeta"
                ],
                "solicitud": [
                    "solicitar tarjeta", "quiero una tarjeta", "cómo consigo una tarjeta", "necesito tarjeta"
                ],
                "pagos": [
                    "pagar tarjeta", "cómo pagar tarjeta", "quiero pagar mi tarjeta", "pago de tarjeta"
                ]
            },
            "prestamo": {
                "informacion": [
                    "préstamo", "crédito", "financiamiento", "hipoteca", "información préstamo", "detalles préstamo"
                ],
                "solicitud": [
                    "cómo pedir préstamo", "solicitar préstamo", "quiero un crédito", "pedir préstamo", "necesito un préstamo"
                ],
                "requisitos": [
                    "requisitos préstamo", "qué necesito para un préstamo", "documentos para préstamo"
                ]
            },
            "transferencia": {
                "hacer": [
                    "transferencia", "enviar dinero", "hacer una transferencia", "cómo enviar dinero", 
                    "transferir", "mandar dinero", "transferencia bancaria", "cómo transferir dinero"
                ],
                "estado": [
                    "estado de transferencia", "ver transferencia", "detalle de transferencia", "seguimiento transferencia"
                ]
            },
            "bloqueo": {
                "tarjeta": [
                    "bloquear tarjeta", "perdí mi tarjeta", "bloqueo por robo", "suspender tarjeta", 
                    "me robaron la tarjeta", "bloquear tarjeta de crédito", "bloquear tarjeta débito"
                ],
                "cuenta": [
                    "bloquear cuenta", "suspender cuenta", "quiero bloquear mi cuenta", "cómo bloqueo mi cuenta"
                ]
            },
            "estado_cuenta": {
                "saldo": [
                    "estado de cuenta", "saldo", "consultar saldo", "cuánto dinero tengo", 
                    "quiero saber mi saldo", "cómo va mi cuenta", "ver mi saldo", "saber cuánto tengo"
                ],
                "movimientos": [
                    "movimientos", "detalles de mi cuenta", "movimientos de mi cuenta", 
                    "estado actual de mi cuenta", "detalle de movimientos"
                ]
            },
            "pagos": {
                "realizar": [
                    "pago", "realizar pago", "cómo pagar", "hacer un pago", "pagos pendientes", 
                    "cómo hacer un pago", "quiero pagar algo"
                ],
                "facturas": [
                    "pago de facturas", "pagar servicio", "facturas a pagar", "cancelar deuda"
                ]
            },
            "soporte": {
                "reclamo": [
                    "hacer un reclamo", "quiero hacer un reclamo", "problema con el banco", "problema con mi cuenta", 
                    "necesito soporte", "tengo un problema", "cómo hago un reclamo"
                ],
                "contactar": [
                    "contactar soporte", "hablar con atención al cliente", "dónde puedo pedir ayuda", 
                    "quiero hablar con alguien", "atención al cliente"
                ]
            }
        }

    def normalizar_texto(self, texto):
        texto = texto.lower().strip()
        texto = re.sub(r"[¿?¡!.,;]", "", texto)  # Eliminar caracteres especiales para dejar limpia la consulta
        return texto

    def procesar_consulta(self, texto):
        texto = self.normalizar_texto(texto)
        transicion = self.analizar_transicion(texto)
        self.estado_actual = transicion
        return self.estados[self.estado_actual[0]](texto)

    def analizar_transicion(self, texto):
        # Procesar la entrada del usuario con spacy
        doc = self.nlp(texto)
        
        # Calcular similitud para cada patrón, si se baja puede que haga match con mas cosas pero falle en las respuestas
        max_similitud = 0
        estado_seleccionado = ("desconocido", None)
        for estado, subcategorias in self.patrones.items():
            for subcategoria, frases in subcategorias.items():
                for frase in frases:
                    frase_doc = self.nlp(frase)
                    similitud = doc.similarity(frase_doc)
                    self.logger.info(f"Similitud entre '{texto}' y '{frase}' (subcategoría {subcategoria}): {similitud}")
                    if similitud > max_similitud and similitud > 0.8:
                        max_similitud = similitud
                        estado_seleccionado = (estado, subcategoria)
        return estado_seleccionado
    def estado_inicio(self, texto):
        return "Hola, soy tu asistente bancario. ¿En qué puedo ayudarte?"

    def estado_tarjeta(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "informacion":
            return "Ofrecemos tarjetas Visa y Mastercard con múltiples beneficios."
        elif subcategoria == "solicitud":
            return "Puedes solicitar una tarjeta en línea o visitando una sucursal."
        elif subcategoria == "pagos":
            return "Puedes pagar tu tarjeta desde nuestra app o banca en línea."
        return "¿En qué más puedo ayudarte con tus tarjetas?"

    def estado_cuenta(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "abrir":
            return "Para abrir una cuenta necesitas cédula, planilla de luz y número de contacto."
        elif subcategoria == "cerrar":
            return "Para cerrar tu cuenta, visita una sucursal con tu identificación."
        return "¿En qué más puedo ayudarte con tu cuenta?"

    def estado_prestamo(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "informacion":
            return "Nuestros préstamos incluyen opciones personales, hipotecarios y más."
        elif subcategoria == "solicitud":
            return "Puedes solicitar un préstamo en línea o en una sucursal."
        elif subcategoria == "requisitos":
            return "Para un préstamo necesitas cédula, historial crediticio y comprobante de ingresos."
        return "¿En qué más puedo ayudarte con los préstamos?"

    def estado_transferencia(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "hacer":
            return "Puedes hacer transferencias desde nuestra banca en línea o en la app móvil."
        elif subcategoria == "estado":
            return "Consulta el estado de tus transferencias en la sección de historial de la app."
        return "¿En qué más puedo ayudarte con transferencias?"

    def estado_bloqueo(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "tarjeta":
            return "Para bloquear tu tarjeta, llama al 1800-BANCOLO o usa nuestra app móvil."
        elif subcategoria == "cuenta":
            return "Para bloquear tu cuenta, visita una sucursal o llama al 1800-BANCOLO."
        return "¿En qué más puedo ayudarte con bloqueos?"

    def estado_estado_cuenta(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "saldo":
            return "Consulta tu saldo desde nuestra app o banca en línea."
        elif subcategoria == "movimientos":
            return "Revisa los movimientos de tu cuenta desde nuestra app o sucursal."
        return "¿En qué más puedo ayudarte con tu estado de cuenta?"

    def estado_pagos(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "realizar":
            return "Puedes realizar pagos desde nuestra app o banca en línea."
        elif subcategoria == "facturas":
            return "Paga tus facturas desde la opción de pagos en nuestra app."
        return "¿En qué más puedo ayudarte con pagos?"

    def estado_soporte(self, texto):
        subcategoria = self.estado_actual[1]
        if subcategoria == "reclamo":
            return "Para hacer un reclamo, visita una sucursal o llama al 1800-BANCOLO."
        elif subcategoria == "contactar":
            return "Contacta a soporte llamando al 1800-BANCOLO o escribiendo en nuestra app."
        return "¿En qué más puedo ayudarte con soporte?"

    def estado_ubicacion(self, texto):
        return "Las sucursales están en Loja, Quito y Guayaquil. ¿Necesitas direcciones exactas?"

    def estado_horario(self, texto):
        return "Nuestro horario es de lunes a viernes de 08:00 a 16:00. Sábados hasta las 12:00."

    def estado_desconocido(self, texto):
        return "Lo siento, no entendí tu consulta. ¿Podrías reformularla?"

# Prueba en consola
if __name__ == "__main__":
    chatbot = ChatbotBancario()
    while True:
        consulta = input("Usuario: ")
        if consulta.lower() in ["salir", "adiós", "bye"]:
            print("Chatbot: ¡Hasta luego!")
            break
        respuesta = chatbot.procesar_consulta(consulta)
        print(f"Chatbot: {respuesta}")
