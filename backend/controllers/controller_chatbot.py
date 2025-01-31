import re

class ChatbotBancario:
    def __init__(self):
        # Definición de estados
        self.estados = {
            "inicio": self.estado_inicio,
            "saludo": self.estado_saludo,
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
        self.contexto = {}

    def procesar_consulta(self, texto):
        texto = texto.lower()
        transicion = self.analizar_transicion(texto)
        self.estado_actual = transicion
        return self.estados[self.estado_actual](texto)

    def analizar_transicion(self, texto):
        """ Determina a qué estado debe ir según la entrada del usuario """
        patrones = {
            "saludo": r"\b(hola|buenos días|buenas tardes|buenas noches|qué tal|que tal|hey|saludos|buen día|buenas)\b",
            "ubicacion": r"\b(ubicación|ubicacion|sucursal|dónde están|en dónde|donde están|dirección|direccion)\b",
            "horario": r"\b(horario|hora|a qué hora|cuando abren|cuando cierran|horarios|apertura|cierre)\b",
            "cuenta": r"\b(abrir cuenta|crear cuenta|requisitos cuenta|nueva cuenta|registrar cuenta|cuenta bancaria)\b",
            "tarjeta": r"\b(tarjeta|crédito|credito|visa|mastercard|solicitar tarjeta|tarjeta débito|tarjeta de crédito)\b",
            "prestamo": r"\b(préstamo|prestamo|solicitar préstamo|credito bancario|préstamos personales|hipotecario)\b",
            "transferencia": r"\b(transferencia|enviar dinero|transferir fondos|depósito|transferencia bancaria)\b",
            "bloqueo": r"\b(bloquear tarjeta|robo tarjeta|perdí mi tarjeta|bloqueo cuenta|fraude|clonación)\b",
            "estado_cuenta": r"\b(estado de cuenta|consultar saldo|saldo actual|movimientos bancarios|cuánto tengo)\b",
            "pagos": r"\b(pagar|realizar pago|pagos|facturas|pago de tarjeta|pago de préstamo|deuda)\b",
            "soporte": r"\b(soporte|ayuda|atención al cliente|problema|contactar|error|reclamo)\b"
        }

        for estado, patron in patrones.items():
            if re.search(patron, texto):
                return estado
        return "desconocido"

    def estado_inicio(self, texto):
        return "¡Hola! Soy el asistente del Banco de Loja. ¿En qué puedo ayudarte?"

    def estado_saludo(self, texto):
        return "¡Hola! ¿En qué puedo ayudarte hoy? Puedes preguntarme sobre cuentas, tarjetas, préstamos y más."

    def estado_ubicacion(self, texto):
        return "Las sucursales están ubicadas en Loja, Quito y Guayaquil. ¿Necesitas direcciones exactas?"

    def estado_horario(self, texto):
        return "El horario de atención es de lunes a viernes de 08:00 a 16:00. Los sábados hasta las 12:00 en algunas sucursales."

    def estado_cuenta(self, texto):
        return ("Para abrir una cuenta necesitas: Cédula, planilla de luz, correo electrónico y número de contacto. "
                "Puedes hacerlo en sucursal o en nuestra banca en línea.")

    def estado_tarjeta(self, texto):
        return ("Ofrecemos tarjetas de crédito Visa y Mastercard con beneficios exclusivos. "
                "¿Deseas conocer los requisitos o tipos de tarjeta?")

    def estado_prestamo(self, texto):
        return ("Tenemos préstamos personales, comerciales y para vivienda con tasas competitivas. "
                "Puedes solicitarlo en línea o en una sucursal.")

    def estado_transferencia(self, texto):
        return "Puedes realizar transferencias desde la banca en línea o en una sucursal. ¿Necesitas ayuda con el proceso?"

    def estado_bloqueo(self, texto):
        return ("Para bloquear una tarjeta, llama al 1800-BANCOLO o ingresa a la app móvil. "
                "También puedes acudir a una sucursal.")

    def estado_estado_cuenta(self, texto):
        return "Para consultar tu estado de cuenta, accede a la banca en línea o solicita un resumen en una sucursal."

    def estado_pagos(self, texto):
        return "Puedes realizar pagos de servicios, tarjetas y préstamos desde nuestra app o banca en línea."

    def estado_soporte(self, texto):
        return ("Si necesitas ayuda, puedes contactar a nuestro servicio al cliente llamando al 1800-BANCOLO "
                "o visitando una de nuestras sucursales.")

    def estado_desconocido(self, texto):
        return "Lo siento, no entendí tu consulta. ¿Podrías reformularla? También puedes llamar al 1800-BANCOLO."

