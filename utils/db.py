import os
import json
from models.MinecraftColor import MinecraftColor

ROOT_DIR = os.path.abspath(os.curdir)
SRC_DIR = os.path.join(ROOT_DIR, 'src')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

class db:
    def __init__(self):
        self.colors : list[MinecraftColor] = []
        self.initialize_colors()
    
    def initialize_colors(self):
        with open(os.path.join(SRC_DIR, 'map_colors.json')) as file:
            json_data = json.load(file)
            self.colors = [MinecraftColor(**item) for item in json_data] # dict to class

if __name__ == '__main__':
    database = db()
    for v in database.colors:
        print(v["id"])