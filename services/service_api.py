import wikipedia

class ServiceAPI:
    def __init__(self, palabra):
        self.palabra = palabra
        # Cambiar el idioma a español
        wikipedia.set_lang("es")

    def fetch_data(self):
        try:
            # Obtener el resumen del artículo
            summary = wikipedia.summary(self.palabra)
            return summary
        except wikipedia.exceptions.PageError:
            # En caso de que la página no exista
            return None
        except wikipedia.exceptions.DisambiguationError as e:
            # En caso de que se devuelva una página de desambiguación
            return f"Disambiguation error: {e.options}"
        except Exception as e:
            # Manejo de otras excepciones
            print(f"Error: {e}")
            return None
