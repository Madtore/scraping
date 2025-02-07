import datas.scraping as scraping

class ServiceScraping:
    def __init__(self):
        self.scraping = scraping.Scraping
        
    def get_h1(self, url):
        return self.scraping(url).get_h1
    
    def get_description(self, url):
        return self.scraping(url).get_description
    
    def get_content(self, url):
        return self.scraping(url).get_content
    
    def get_title(self, url):
        return self.scraping(url).get_title
    
    def get_p(self, url):
        return self.scraping(url).get_p