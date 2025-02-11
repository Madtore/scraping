import sqlite3

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("datas/database.db")
        self.cursor = self.db.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS datos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                titulo TEXT,
                sub_titulo TEXT,
                descripcion TEXT,
                contenido LONG TEXT
            )
        """)  
        self.db.commit()

        
        
    def insert_data(self, url, titulo, descripcion , sub_titulo,contenido):
        try:
            self.cursor.execute("""
                INSERT INTO datos (url, titulo, descripcion, sub_titulo, contenido)
                VALUES (?, ?, ?, ?, ?)
            """, (url, titulo, descripcion, sub_titulo, contenido))
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")
            self.db.rollback()

        
        
    def get_data_by_regex(self, regex):
        regex = f"%{regex}%"
        self.cursor.execute(f"""
            SELECT *
            FROM datos
            WHERE 
            url LIKE ?
            OR
            titulo LIKE ?
            OR
            descripcion LIKE ?
            OR
            contenido LIKE ?
        """, (
             regex,
              regex,
              regex,
              regex))
        
        return self.cursor.fetchall()
    
    def get_all_data(self):
        self.cursor = self.db.cursor()
        self.cursor.execute(f"""
            SELECT *
            FROM datos
        """)
        return self.cursor.fetchall()
                