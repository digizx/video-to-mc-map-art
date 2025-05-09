import os
import json

ROOT_DIR = os.path.abspath(os.curdir)
SRC_DIR = os.path.join(ROOT_DIR, 'src')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

class db:
    def __init__(self):
        self.colors = None
        self.initialize_colors()
    
    def initialize_colors(self):
        with open(os.path.join(SRC_DIR, 'map_colors.json')) as file:
            self.colors = json.load(file)