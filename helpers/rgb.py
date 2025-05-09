from utils.db import db
from numpy import uint8, int8

def find_share_variation(
    input_rgb : tuple[uint8, uint8, uint8]
    ) -> tuple[
        tuple[uint8, uint8, uint8], # Four possible RGBs
        tuple[uint8, uint8, uint8], 
        tuple[uint8, uint8, uint8], 
        tuple[uint8, uint8, uint8]
    ]:
    """
    Function that receives an input RGB as a parameter and turns it into
    the 4 Minecraft shade variations
    """
    pass

def find_best_suitable_block(
    database : db, 
    input_rgb : tuple[uint8, uint8, uint8]
    ) -> int8:
    """
    Function that iterates through all available block colors and finds
    the most suitable option, then returns the respective ID that fits the best.
    """
    for v in database.colors:
        print(v)
    
if __name__ == '__main__':
    database = db()
    find_best_suitable_block(database, [1, 2, 3])