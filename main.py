from services.service_scraping import ServiceScraping
from configuration.config import Config
import datas.data_base as db

global config
config = Config()
def cargar_datos(url):
    scraping = ServiceScraping(url)
    scraping.get_contenido()


def menu_principal():
    print(config.get_config().menu.bienvenido)
    print()
    print(config.get_config().menu.opciones.primera)
    print(config.get_config().menu.opciones.segunda)
    print(config.get_config().menu.opciones.tercera)


def seleccion_opcion():
    menu_principal()
    try:
        opcion = int(input(config.get_config().menu.seleccion))
    except ValueError:
        print("Opción no valida. Por favor, selecciona una opcion valida.")
        return seleccion_opcion()
    return opcion


def buscar_por_regex(regex):
    ServiceScraping().get_datos_formateados(regex) 
    


if __name__ == "__main__":
    
    while True:
        opcion = seleccion_opcion()
        if opcion == 1:
            for guerra in config.get_config().urls.guerras.primera_guera_mundial:
                print(guerra)
                for url in guerra.urls:
                    cargar_datos(url)
        elif opcion == 2:
            regex = input("Ingrese el patron de busqueda: ")
            buscar_por_regex(regex)
        elif opcion == 3:
            break
    

    




    

    