import gzip
import io


class DatUtils():
    def __init__(self):
        pass

    def nbt_to_dat(self, nbt_file):
        """
        Function that turns NBT information into a DAT file
        """
        try:
            buffer = io.BytesIO() # We're going to these depths to not early safe the nbt lol
            nbt_file.write(buffer)
            uncompressed_data = buffer.getvalue()
        except:
            print('There was a problem with the uncompressed data buffer!')
        
        return gzip.compress(uncompressed_data)

    def save_dat_file(self, dat_file, path):
        """
        Saves DAT file in a determined path
        """
        try:
            with open(path, 'wb') as f:
                f.write(dat_file)
                print('The .dat file was saved successfully!')
        except Exception as e:
            print('Error saving .dat file:', e)

if __name__ == '__main__':
    
    from utils.NbtUtils import encode_into_map_nbt
    from numpy import int8
    from config import ROOT_DIR, SRC_DIR, OUT_DIR

    dat_utils = DatUtils()

    colors : int8 = []

    colors.append(1)
    colors.append(2)
    colors.append(3)
    colors.append(4)
    colors.append(5)

    nbt_file = encode_into_map_nbt(colors)

    # print(nbt_file)

    dat_file = dat_utils.nbt_to_dat(nbt_file)

    print(dat_file)