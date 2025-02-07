import datas.scraping as scraping
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
    
    def get_contenido(self):
        datos = self.get_data()

        titulo = datos[0]
        descripcion = datos[1]
        contenido_extraido = datos[2] 

        print(titulo, descripcion)
        for dato in contenido_extraido:
            print(f"Subtítulo: {dato['sub_titulo']}\nContenido: {dato['contenido']}\n")
            try:
                while opz != 1 and opz != 2:
                    opz = int(input("Quieres guarda el contenido en la base de datos? 1.Si 2.No: "))

                if opz == 1:
                    self.db.insert_data(self.url, titulo, descripcion, dato['sub_titulo'], dato['contenido'])
                elif opz == 2:
                    pass
            except Exception as e:
                print(f"Error: {e}")    




    def get_datos_formateados(self , regex):
        os.system("cls")
        data = self.db.get_data_by_regex(regex)
        if data:
            for dato in data:
                url = dato[1]
                titulo = dato[2]
                sub_titulo = dato[3]
                descripcion = dato[4]
                contenido = dato[5]
                print(f"URL: {url}\nTITULO: {titulo}\nSUB-TITULO: {sub_titulo}\nDESCRIPCION: {descripcion}\nCONTENIDO: {contenido}\n")

            while True:
                try:
                    opz = int(input("Quieres generar un archivo html con los datos? 1.Si 2.No: "))
                    while opz != 1 and opz != 2:
                        opz = int(input("Quieres generar un archivo html con los datos? 1.Si 2.No: "))
                    if opz == 1:
                        generado = self.generar_html(data)
                        if generado:
                            print("Archivo generado con exito")
                        else:
                            print("Error al generar el archivo")
                        break
                    elif opz == 2:
                        break
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print("No se encontraron datos que coincidan con el patron")



    def generar_html(self, data, nombre_archivo="datos.html"):
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados de Búsqueda</title>
    <title>Resultados de búsqueda</title>
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
        #results {
            padding: 20px;
        #resultados { 
            padding: 20px; 
        }
        .result {
            border: 1px solid #ddd;
        .resultado { 
            border: 1px solid #ddd; 
            margin-bottom: 20px;
            padding: 15px;
            background-color: white;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            background-color: white; 
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1); 
        }
        .title {
            font-size: 1.2em;
        .titulo {
            font-size: 1.2em;   
            font-weight: bold;
            margin-bottom: 5px;
            margin-bottom: 5px; 
        }
        .description {
            font-style: italic;
            color: #777;
            margin-bottom: 10px;
        .descripcion {
          font-style: italic;
          color: #777;
          margin-bottom: 10px;
        }
        .content {
            text-align: justify;
        .contenido {
          text-align: justify; 
        }
        a {
            color: #007bff;
            text-decoration: none;
        a { /* Estilos para los enlaces */
            color: #007bff; /* Color azul para enlaces */
            text-decoration: none; /* Quitar subrayado */
        }
        a:hover {
            text-decoration: underline;
            text-decoration: underline; 
        }

    </style>
</head>
<body>
    <h1>Resultados de Búsqueda</h1>
    <div id="results">
    </head>
    <body>
        <h1>Resultados de búsqueda</h1>
        <div id="resultados">""")
            for dato in data:
                url = dato[1]
                titulo = dato[2]
                descripcion = dato[4]
                contenido = dato[5]
  
            f.write(f"""<div class="resultado">
                    <div class="titulo">{titulo}</div>
                    <div class="descripcion">{descripcion}</div>
                    <div class="contenido">{contenido}</div>  <a href="{url}" target="_blank">Enlace</a> </div>""")
            f.write("""</div>
</body>
</html>""")
       
            f.write("""</div>
    </body>
    </html>""")

        except Exception as e:
            print(f"Error al generar el archivo: {e}")
            return False
        f.close()
        return True

