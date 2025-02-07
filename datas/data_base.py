import sqlite3
from configuration.config import Config
from regex import match_regex
class DataBase:
    def __init__(self):
        self.config = Config.get_config()
        self.db = sqlite3.connect(self.config.database.nombre)
        self.cursor = self.db.cursor()
        
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS {nombre} (
                id {id_tipo},
                url {url_tipo},
                descripcion {descripcion_tipo},
                contenido {contenido_tipo}
            )
        """).format(
            nombre = self.config.database.tabla.nombre,
            id_tipo = self.config.database.tabla.campos.id,
            url_tipo = self.config.database.tabla.campos.url,
            descripcion_tipo = self.config.database.tabla.campos.descripcion,
            contenido_tipo = self.config.database.tabla.campos.contenido
        )
        
        self.db.commit()
        self.db.close()
        
    
        
        
    def insert_data(self, id, url, descripcion, contenido):
        self.cursor.execute("""
            INSERT INTO {nombre} (id, url, descripcion, contenido)
            VALUES (?, ?, ?, ?)
        """, (id, url, descripcion, contenido))
        
        self.db.commit()
        self.db.close()
        
        
    def get_data_by_regex(self, regex):
        self.cursor.execute(f"""
            SELECT *
            FROM ?
            WHERE 
            url LIKE ?
            OR
            descripcion LIKE ?
            OR
            contenido LIKE ?
        """, (
              self.config.database.tabla.nombre,
              regex,
              regex,
              regex))
        
        return self.cursor.fetchall()
                