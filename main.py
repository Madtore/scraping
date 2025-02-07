from services.service_database import ServiceDatabase
from services.service_scraping import ServiceScraping
from configuracion.config import Config

if __name__ == "__main__":
    config = Config()
    db = ServiceDatabase()
    
    scraping = ServiceScraping()
    
    