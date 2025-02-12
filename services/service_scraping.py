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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #fff;
            text-align: center;
            padding: 20px;
        }

        h1 {
            font-size: 2.5em;
            font-weight: 600;
            margin-bottom: 20px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

        #resultados {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .resultado {
            background: #fff;
            color: #333;
            width: 90%;
            max-width: 800px;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .resultado:hover {
            transform: translateY(-5px);
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
        }

        .titulo {
            font-size: 1.5em;
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
        }

        .sub-titulo {
            font-size: 1.2em;
            font-weight: 600;
            color: #555;
            margin-bottom: 8px;
        }

        .descripcion {
            font-style: italic;
            font-size: 1em;
            color: #666;
            margin-bottom: 12px;
        }

        .contenido {
            font-family: 'Roboto', sans-serif;
            font-size: 1em;
            line-height: 1.6;
            text-align: justify;
            color: #444;
        }

        .ver-pagina {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 15px;
            font-size: 1em;
            font-weight: 600;
            color: #fff;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 8px;
            text-decoration: none;
            transition: background 0.3s ease, transform 0.2s ease;
        }

        .ver-pagina:hover {
            background: linear-gradient(135deg, #5568d9, #6b3f99);
            transform: scale(1.05);
        }
        </style>
    </head>
    <body>
        <h1>Resultados de búsqueda</h1>
        <div id="resultados">""")
    
                for dato in data:                 
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
                <div class="contenido">{contenido}</div>""")
                    if not url.startswith("wikipedia_api"):
                        f.write(f"""<a href="{url}" target="_blank">ver pagina</a></div>""")
                    else:
                        f.write(f"""<p>datos de la api: {url}</p></div>""")    
                
                f.write("""
        </div>
    </body>
    </html>""")
    
            return True
    
        except Exception:
            print(f"Error al generar el HTML")
            return False
    