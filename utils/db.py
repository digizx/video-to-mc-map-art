import os
import json
from typing import final

from numpy import clip, uint8
from models.MinecraftColor import MinecraftColor
from models.RGBColor import RGBColor

ROOT_DIR = os.path.abspath(os.curdir)
SRC_DIR = os.path.join(ROOT_DIR, 'src')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'out')

class db:
    def __init__(self):
        self.colors : list[MinecraftColor] = []
        self.shaded_colors : list[MinecraftColor] = []
        self.initialize_colors()
        self.initialize_shaded_colors()
    
    def initialize_colors(self):
        with open(os.path.join(SRC_DIR, 'map_colors.json')) as file:
            json_data = json.load(file)
            self.colors = [MinecraftColor(**item) for item in json_data] # dict to class
    
    def initialize_shaded_colors(self):
        shaded_colors = []
        for color in self.colors:
            shaded_variations = self.find_shade_variations(
                MinecraftColor(
                    id=color.id,
                    name=color.name,
                    rgb=RGBColor(color.rgb['r'], color.rgb['g'], color.rgb['b']),
                )
            )
            shaded_colors.extend(shaded_variations)
        self.shaded_colors = shaded_colors

    def shade_rgb_color(
        self,
        color : uint8,
        shade : uint8
        ) -> uint8:
        """
        Based on Minecraft Map Art, it turns a color into a certain degre of shade.
        """
        shaded_color = (color * shade) // 255
        return uint8(clip(shaded_color, 0, 255))

    def find_shade_variations(
        self,
        mc_color : MinecraftColor
        ) -> tuple[
            MinecraftColor
        ]:
        """
        Function that receives an input RGB as a parameter and turns it into
        the 4 Minecraft shade variations
        """
        result : list[MinecraftColor] = []
        SHADES : final = [180, 220, 255, 135]

        for index, shade in enumerate(SHADES):
            shaded_r = self.shade_rgb_color(mc_color.rgb.r, shade)
            shaded_g = self.shade_rgb_color(mc_color.rgb.g, shade)
            shaded_b = self.shade_rgb_color(mc_color.rgb.b, shade)

            new_shade = MinecraftColor(
                id=((mc_color.id * 4) + index),
                name=mc_color.name,
                rgb=RGBColor(shaded_r, shaded_g, shaded_b)
            )
            result.append(new_shade)
        
        return result

if __name__ == '__main__':
    database = db()
    for v in database.shaded_colors:
        print(v.id, f'({v.rgb.r}, {v.rgb.g}, {v.rgb.b})')