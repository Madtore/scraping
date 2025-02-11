import datas.scraping as scraping
import html
import datas.data_base as db
import os
  


class ServiceScraping:
    def __init__(self, url = None):
        self.url = url
        self.scraping = scraping.Scraping(url)
        self.db = db.DataBase()
        
    def get_data(self):
        data = self.scraping.get_data()

        titulo = data.find("h1").text
        descripcion = data.find("p").text
        sub_titulo = None
        contenido = ""
        datos = []

        for elemento in data.find_all(["h2", "h3", "h4", "h5", "h6", "p"]):
            if elemento.name in ["h2", "h3", "h4", "h5", "h6"]:
                sub_titulo = elemento.text.strip()  
            elif elemento.name == "p":
                contenido = elemento.text.strip()
                if sub_titulo: 
                    datos.append({"sub_titulo": sub_titulo, "contenido": contenido})
                contenido = ""

        return titulo, descripcion, datos
    

    def generar_html(self, data, nombre_archivo="datos.html"):
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("""<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resultados de Búsqueda</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                margin: 0;
                padding: 0;
            }
            h1 {
                text-align: center;
                margin-top: 20px;
            }
            #resultados { 
                padding: 20px; 
            }
            .resultado { 
                border: 1px solid #ddd; 
                margin-bottom: 20px;
                padding: 15px;
                background-color: white; 
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1); 
            }
            .titulo {
                font-size: 1.2em;   
                font-weight: bold;
                margin-bottom: 5px; 
            }
            .sub-titulo {
                font-size: 1em;
                font-weight: bold;
                color: #555;
                margin-bottom: 5px;
            }
            .descripcion {
                font-style: italic;
                color: #777;
                margin-bottom: 10px;
            }
            .contenido {
                text-align: justify; 
            }
            a { 
                color: #007bff;
                text-decoration: none; 
            }
            a:hover {
                text-decoration: underline; 
            }
        </style>
    </head>
    <body>
        <h1>Resultados de búsqueda</h1>
        <div id="resultados">""")
    
                for dato in data:
                    print("Dato recibido:", dato)
                    
                    if len(dato) < 6:
                        print("Advertencia: el dato no tiene suficientes elementos")
                        continue  # O podrías llenar los valores faltantes con strings vacíos
                    
                    url = html.escape(dato[1])
                    titulo = html.escape(dato[2])
                    sub_titulo = html.escape(dato[3])
                    descripcion = html.escape(dato[4])
                    contenido = html.escape(dato[5])
    
                    f.write(f"""
            <div class="resultado">
                <div class="titulo">{titulo}</div>
                <div class="sub-titulo">{sub_titulo}</div>
                <div class="descripcion">{descripcion}</div>
                <div class="contenido">{contenido}</div>
                <a href="{url}" target="_blank">Ver fuente original</a>
            </div>""")
    
                # Cerrar etiquetas HTML
                f.write("""
        </div>
    </body>
    </html>""")
    
            return True
    
        except Exception as e:
            print(f"Error al generar el archivo: {e}")
            return False
    