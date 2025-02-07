import datas.data_base as db

class ServiceDatabase:
    def __init__(self):
        self.database = db.DataBase()
        self.database.create_table()
        
    def insert_data(self, id, url, descripcion, contenido):
        self.database.insert_data(id, url, descripcion, contenido)
        
    def get_data_by_regex(self, regex):
        return self.database.get_data_by_regex(regex)
    
    def close(self):
        self.database.db.close()