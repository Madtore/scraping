import wikipedia

class ServiceAPI:
    def __init__(self, palabra):
        self.palabra = palabra
        wikipedia.set_lang("es")

    def fetch_data(self):
        try:
            summary = wikipedia.summary(self.palabra)
            return summary
        except wikipedia.exceptions.PageError:
            return None
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Disambiguation error: {e.options}"
        except Exception as e:
            print(f"Error: {e}")
            return None
