import os
from config import ROOT_DIR, SRC_DIR, OUT_DIR
from enum import Enum

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class DatapackGeneratorUtils():
    def __init__(
        self,
        total_frames: int,
        x: int,
        y: int,
        z: int,
        direction: Direction
        ):
        self.total_frames = total_frames
        self.x = x
        self.y = y
        self.z = z
        self.direction = direction
        # check if it's either x or y
        self.x_axis: bool = True
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            self.x_axis = False

        # {0} the northest, Y decreases more
        # {0} the westest, X decreases more
        # {0} the southest, Y increases more
        # {0} the eastest, X increases more
        self.mult = 1 # My brain isn't brain enough to name this properly
        if self.direction == Direction.NORTH or self.direction == Direction.WEST:
            self.mult = -1


    def generate_datapack(self):
        self.generate_place_initial_blocks()
        self.summon_item_frames()

    def generate_place_initial_blocks(self):
        commands : list[str] = []

        # set commands required for each frame
        if self.direction == Direction.NORTH:
            # top
            commands.append(self.get_command_set_block('quartz_block',  self.x,     '{0}', self.z + 1)) # {0} the northest, Y decreases more
            commands.append(self.get_command_set_block('air',           self.x + 1, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('air',           self.x + 2, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('air',           self.x + 3, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('air',           self.x + 4, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('quartz_block',  self.x + 5, '{0}', self.z + 1))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                        self.x,     '{0}', self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=west,half=top]', self.x + 1, '{0}', self.z))
            commands.append(self.get_command_set_block('air',                                 self.x + 2, '{0}', self.z))
            commands.append(self.get_command_set_block('air',                                 self.x + 3, '{0}', self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=east,half=top]', self.x + 4, '{0}', self.z))
            commands.append(self.get_command_set_block('quartz_block',                        self.x + 5, '{0}', self.z))
            # ice
            commands.append(self.get_command_set_block('packed_ice', self.x + 1, '{0}', self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', self.x + 2, '{0}', self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', self.x + 3, '{0}', self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', self.x + 4, '{0}', self.z - 1))
        if self.direction == Direction.EAST:
            # top
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y,     self.z + 1)) # {0} the westest, X decreases more
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 1, self.z + 1))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 2, self.z + 1))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 3, self.z + 1))
            commands.append(self.get_command_set_block('air',           '{0}', self.y + 4, self.z + 1))
            commands.append(self.get_command_set_block('quartz_block',  '{0}', self.y + 5, self.z + 1))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y,     self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=north,half=top]',  '{0}', self.y + 1, self.z))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y + 2, self.z))
            commands.append(self.get_command_set_block('air',                                   '{0}', self.y + 3, self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=south,half=top]',  '{0}', self.y + 4, self.z))
            commands.append(self.get_command_set_block('quartz_block',                          '{0}', self.y + 5, self.z))
            # ice
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y + 1, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y + 2, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y + 3, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y + 4, self.z - 1))
        if self.direction == Direction.SOUTH:
            # top
            commands.append(self.get_command_set_block('quartz_block',  self.x,     '{0}', self.z + 1)) # {0} the southest, Y increases more
            commands.append(self.get_command_set_block('air',           self.x - 1, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('air',           self.x - 2, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('air',           self.x - 3, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('air',           self.x - 4, '{0}', self.z + 1))
            commands.append(self.get_command_set_block('quartz_block',  self.x - 5, '{0}', self.z + 1))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                        self.x,     '{0}', self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=east,half=top]', self.x - 1, '{0}', self.z))
            commands.append(self.get_command_set_block('air',                                 self.x - 2, '{0}', self.z))
            commands.append(self.get_command_set_block('air',                                 self.x - 3, '{0}', self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=west,half=top]', self.x - 4, '{0}', self.z))
            commands.append(self.get_command_set_block('quartz_block',                        self.x - 5, '{0}', self.z))
            # ice
            commands.append(self.get_command_set_block('packed_ice', self.x - 1, '{0}', self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', self.x - 2, '{0}', self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', self.x - 3, '{0}', self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', self.x - 4, '{0}', self.z - 1))
        if self.direction == Direction.WEST:
            # top
            commands.append(self.get_command_set_block('quartz_block', '{0}', self.y,     self.z + 1)) # {0} the eastest, X increases more
            commands.append(self.get_command_set_block('air',          '{0}', self.y - 1, self.z + 1))
            commands.append(self.get_command_set_block('air',          '{0}', self.y - 2, self.z + 1))
            commands.append(self.get_command_set_block('air',          '{0}', self.y - 3, self.z + 1))
            commands.append(self.get_command_set_block('air',          '{0}', self.y - 4, self.z + 1))
            commands.append(self.get_command_set_block('quartz_block', '{0}', self.y - 5, self.z + 1))
            # bottom
            commands.append(self.get_command_set_block('quartz_block',                         '{0}', self.y,     self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=south,half=top]', '{0}', self.y - 1, self.z))
            commands.append(self.get_command_set_block('air',                                  '{0}', self.y - 2, self.z))
            commands.append(self.get_command_set_block('air',                                  '{0}', self.y - 3, self.z))
            commands.append(self.get_command_set_block('quartz_stairs[facing=north,half=top]', '{0}', self.y - 4, self.z))
            commands.append(self.get_command_set_block('quartz_block',                         '{0}', self.y - 5, self.z))
            # ice
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 1, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 2, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 3, self.z - 1))
            commands.append(self.get_command_set_block('packed_ice', '{0}', self.y - 4, self.z - 1))

        # set the commands
        parsed_commands = []
        for index in range(self.total_frames):
            index *= self.mult
            for command in commands:
                if self.x_axis:
                    parsed_commands.append(command.format(self.x + index))
                else:
                    parsed_commands.append(command.format(self.y + index))

        # store commands in file
        path_place_initial_blocks = os.path.join(OUT_DIR, 'place_initial_blocks.mcfunction')

        with open(path_place_initial_blocks, 'w') as file:
            for command in parsed_commands:
                file.write(command + '\n')

    def summon_item_frames(self):
        if self.direction == Direction.NORTH:
            facing_direction = 5
        if self.direction == Direction.EAST:
            facing_direction = 3
        if self.direction == Direction.SOUTH:
            facing_direction = 4
        if self.direction == Direction.WEST:
            facing_direction = 2
        
        command = (
            'summon item_frame ~ ~ ~ {Facing:' +
            facing_direction +
            'b, Item:{id: "minecraft:filled_map", components:{"minecraft:map_id":0}}}'
        )

        parsed_commands: list[str] = []
        for index in self.total_frames:
            index *= self.mult
            if self.x_axis:
                parsed_command = command.format(self.x + index)
            else:
                parsed_command = command.format(self.y + index)
            parsed_commands.append(parsed_command)

        # store commands in file
        path_place_initial_blocks = os.path.join(OUT_DIR, 'summon_item_frames.mcfunction')

        with open(path_place_initial_blocks, 'w') as file:
            for command in parsed_commands:
                file.write(command + '\n')

    def get_command_set_block(self, block_name, x, y, z):
        return f'setblock {x} {z} {y} {block_name}'

if __name__ == '__main__':
    datapack_utils = DatapackGeneratorUtils(
        total_frames=4,
        x=-43,
        y=122,
        z=-60,
        direction=Direction.WEST
    )

    datapack_utils.generate_place_initial_blocks()