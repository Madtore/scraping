from bs4 import BeautifulSoup
import requests


class Scraping:
    def __init__(self, url):
        self.url = url
        
    def get_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    
    