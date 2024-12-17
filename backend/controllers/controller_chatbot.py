import re

class Chatbot:
    def __init__(self):
        self.lexico = AnalizadorLexico()
        self.sintactico = AnalizadorSintactico()
        self.semantico = AnalizadorSemantico()
        self.generador_respuesta = GeneradorRespuesta()
        self.contexto = {}  # Almacena información relevante para el contexto

    def procesar_consulta(self, texto):
        palabras_clave = self.lexico.analizar(texto)
        if self.sintactico.analizar(texto):
            intencion, detalles = self.semantico.analizar(palabras_clave, texto)
            
            # Actualiza el contexto con los detalles de la consulta
            if detalles:
                self.contexto.update(detalles)

            respuesta = self.generador_respuesta.generar(intencion, self.contexto)

            # Guardar consulta temporalmente
            self.contexto["ultima_consulta"] = texto
            self.contexto["ultima_respuesta"] = respuesta

            return respuesta
        return "Lo siento, la consulta no tiene una estructura válida."


class AnalizadorLexico:
    def analizar(self, texto):
        # Detecta palabras clave y posibles parámetros como ubicaciones u horas
        palabras = re.findall(r'\b\w+\b', texto.lower())
        palabras_referentes = ["ubicación", "ubicacion", "horario", "sucursal", "hora", "abrir", "crear"]
        return [palabra for palabra in palabras if palabra in palabras_referentes]


class AnalizadorSintactico:
    def analizar(self, texto):
        # Valida si el texto sigue patrones básicos de preguntas o comandos
        patrones_validos = [
            r"\b( en dónde|cómo|cuándo|como|cuando|a que|donde|en donde)\b",  # Preguntas básicas
            r"\b(necesito|quiero|puedo)\b",  # Declaraciones comunes
        ]
        return any(re.search(patron, texto.lower()) for patron in patrones_validos)


class AnalizadorSemantico:
    def analizar(self, palabras_clave, texto):
        # Analiza las palabras clave junto con el texto completo para extraer la intención y detalles
        detalles = {}

        if "ubicación" in palabras_clave or "ubicacion" in palabras_clave:
            if "sucursal" in texto:
                detalles["consulta"] = "sucursales"
            return "consultar_ubicacion", detalles
        elif "horario" in palabras_clave or "hora" in palabras_clave:
            return "consultar_horario", detalles
        elif "crear" in palabras_clave or "abrir" in palabras_clave:
            return "crear_cuenta", detalles

        return "intencion_desconocida", detalles


class GeneradorRespuesta:
    def __init__(self):
        self.respuestas = {
            "consultar_ubicacion": "Las sucursales están ubicadas en Loja, Quito, y Guayaquil.",
            "consultar_horario": "El horario de atención es de 8:00 a 16:00.",
            "intencion_desconocida": "No entendí tu consulta. Por favor, reformúlala.",
            "crear_cuenta": (
                "Para crear una cuenta los requisitos necesarios son:\n"
                "- Cédula\n- Planilla de luz\n- Un correo electrónico\n- Contacto"
            ),
        }

    def generar(self, intencion, contexto):
        # Genera respuestas basadas en la intención y el contexto
        if intencion == "consultar_ubicacion" and "consulta" in contexto:
            return f"Las sucursales disponibles son: {self.respuestas['consultar_ubicacion']}"
        
        return self.respuestas.get(intencion, "Error al procesar la consulta.")
