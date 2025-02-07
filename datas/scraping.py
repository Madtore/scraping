from bs4 import BeautifulSoup
import requests

class Scraping:
    def __init__(self, url):
        self.url = url
        self.data = self.get_data()
        
    def get_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def get_description(self):
        return self.data.find('meta', property='og:description').get('content')
    
    def get_content(self):
        return self.data.find('meta', property='og:description').get('content')
    
    def get_title(self):
        return self.data.find('meta', property='og:title').get('content')
    
    def get_h1(self):
        return self.data.find('h1').text
    
    def get_h2(self):
        return self.data.find('h2').text
    
    def get_p(self):
        return self.data.find('p').text
    
    
    