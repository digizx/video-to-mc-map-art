from models.rgb import RGBColor

class MinecraftColor:
    def __init__(
            self,
            id : int, 
            name : str, 
            rgb : RGBColor
        ):
        self.id = id
        self.name = name
        self.rgb = rgb
