import json
from types import SimpleNamespace
import os

def dict_to_object(d):
    return SimpleNamespace(**d)

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(self.config_path, 'r') as f:
            self.config = json.load(f, object_hook=dict_to_object)
            
    def get_config(self):
        return self.config