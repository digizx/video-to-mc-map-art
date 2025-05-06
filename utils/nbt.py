import gzip
import struct
from collections import OrderedDict

def read_nbt(data, pos=0):
    tag_type = data[pos]
    pos += 1
    
    if tag_type == 0:  # TAG_End
        return None, None, pos
    
    # Read name (TAG_String)
    name_length = struct.unpack('>H', data[pos:pos+2])[0]
    pos += 2
    name = data[pos:pos+name_length].decode('utf-8')
    pos += name_length
    
    # Parse value based on type
    if tag_type == 1:   # TAG_Byte
        value = struct.unpack('>b', data[pos:pos+1])[0]
        pos += 1
    elif tag_type == 2:  # TAG_Short
        value = struct.unpack('>h', data[pos:pos+2])[0]
        pos += 2
    elif tag_type == 3:  # TAG_Int
        value = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
    elif tag_type == 4:  # TAG_Long
        value = struct.unpack('>q', data[pos:pos+8])[0]
        pos += 8
    elif tag_type == 5:  # TAG_Float
        value = struct.unpack('>f', data[pos:pos+4])[0]
        pos += 4
    elif tag_type == 6:  # TAG_Double
        value = struct.unpack('>d', data[pos:pos+8])[0]
        pos += 8
    elif tag_type == 7:  # TAG_Byte_Array
        length = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
        value = list(struct.unpack(f'>{length}b', data[pos:pos+length]))
        pos += length
    elif tag_type == 8:  # TAG_String
        str_len = struct.unpack('>H', data[pos:pos+2])[0]
        pos += 2
        value = data[pos:pos+str_len].decode('utf-8')
        pos += str_len
    elif tag_type == 9:  # TAG_List
        list_type = data[pos]
        pos += 1
        list_length = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
        value = []
        for _ in range(list_length):
            item, pos = read_nbt_value(data, pos, list_type)
            value.append(item)
    elif tag_type == 10:  # TAG_Compound
        value = OrderedDict()
        while True:
            item_type = data[pos]
            if item_type == 0:  # TAG_End
                pos += 1
                break
            item_name, item_value, pos = read_nbt(data, pos)
            value[item_name] = item_value
    elif tag_type == 11:  # TAG_Int_Array
        length = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
        value = list(struct.unpack(f'>{length}i', data[pos:pos+4*length]))
        pos += 4 * length
    elif tag_type == 12:  # TAG_Long_Array
        length = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
        value = list(struct.unpack(f'>{length}q', data[pos:pos+8*length]))
        pos += 8 * length
    else:
        raise ValueError(f"Unknown tag type: {tag_type}")
    
    return name, value, pos

def read_nbt_value(data, pos, tag_type):
    if tag_type == 1:   # TAG_Byte
        value = struct.unpack('>b', data[pos:pos+1])[0]
        pos += 1
    elif tag_type == 2:  # TAG_Short
        value = struct.unpack('>h', data[pos:pos+2])[0]
        pos += 2
    elif tag_type == 3:  # TAG_Int
        value = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
    elif tag_type == 4:  # TAG_Long
        value = struct.unpack('>q', data[pos:pos+8])[0]
        pos += 8
    elif tag_type == 5:  # TAG_Float
        value = struct.unpack('>f', data[pos:pos+4])[0]
        pos += 4
    elif tag_type == 6:  # TAG_Double
        value = struct.unpack('>d', data[pos:pos+8])[0]
        pos += 8
    elif tag_type == 7:  # TAG_Byte_Array
        length = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
        value = list(struct.unpack(f'>{length}b', data[pos:pos+length]))
        pos += length
    elif tag_type == 8:  # TAG_String
        str_len = struct.unpack('>H', data[pos:pos+2])[0]
        pos += 2
        value = data[pos:pos+str_len].decode('utf-8')
        pos += str_len
    elif tag_type == 10:  # TAG_Compound
        value = OrderedDict()
        while True:
            item_type = data[pos]
            if item_type == 0:  # TAG_End
                pos += 1
                break
            item_name, item_value, pos = read_nbt(data, pos)
            value[item_name] = item_value
    elif tag_type == 11:  # TAG_Int_Array
        length = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
        value = list(struct.unpack(f'>{length}i', data[pos:pos+4*length]))
        pos += 4 * length
    elif tag_type == 12:  # TAG_Long_Array
        length = struct.unpack('>i', data[pos:pos+4])[0]
        pos += 4
        value = list(struct.unpack(f'>{length}q', data[pos:pos+8*length]))
        pos += 8 * length
    else:
        raise ValueError(f"Unknown list tag type: {tag_type}")
    
    return value, pos

def print_nbt(data, indent=0):
    if isinstance(data, OrderedDict):
        print(' ' * indent + '{')
        for key, value in data.items():
            print(' ' * (indent + 2) + f'"{key}": ', end='')
            print_nbt(value, indent + 2)
        print(' ' * indent + '}')
    elif isinstance(data, list):
        if data and isinstance(data[0], (int, float)):  # Simple array
            print('[' + ', '.join(map(str, data)) + '],')
        else:  # Complex list
            print('[')
            for item in data:
                print(' ' * (indent + 2), end='')
                print_nbt(item, indent + 2)
            print(' ' * indent + ']')
    else:
        print(f'{data},')

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python nbt_reader.py <file.dat>")
        return
    
    filename = sys.argv[1]
    try:
        with open(filename, 'rb') as f:
            compressed_data = f.read()
        
        # Decompress Gzip
        nbt_data = gzip.decompress(compressed_data)
        
        # Parse NBT
        _, root_data, _ = read_nbt(nbt_data)
        
        # Print in readable format
        print_nbt(root_data)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()