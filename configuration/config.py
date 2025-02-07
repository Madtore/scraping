import json
from types import SimpleNamespace

class Config:
    def __init__(self):
        with open('configuration/config.json', 'r') as f:
            self.config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
            
    def get_config(self):
        return self.config