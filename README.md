# Video to Minecraft Map Art
Simple CLI App that transforms a video into a bundle of Minecraft maps and a datapack to place the maps.

# 🛠️ Requirements
* Python3 and PIP need to be installed in order to run the script.
* Create a virtual environment with the next command
```
python3 -m venv <VIRTUAL ENVIRONMENT NAME>
```
* Activate the virtual environment and install the requirements with the next command:
```
pip install -r requirements.txt
```
# 🧾 Usage
| Flag  |  Complete Flag | Usage  |
|---|---|---|
| -n | --name | Name for the zip file that is going to be saved |
| -p | --path | Path of the file that is going to be processed into Minecraft format |
| -x | --x | X coordinates in Minecraft |
| -y | --y | Y coordinates in Minecraft |
| -z | --z | Z coordinates in Minecraft |
| -d | --direction | The options are North, East, South and West. If none selected then the datapack won't be generated |
| -i | --index | Indicates the first map number it'll be saved. By default is 0. |
| -f | --frames | Indicates the amount of frames that will be shown in the game. By default is max. |
| -de | --delay | Indicates the amount of seconds that the first frames will be repeated. By default 0. I highly suggest setting it to 25, so you can pick up speed first. |

## In-game preparations
### How to get the coordinates
Press F3 and grab the coordinates from here (if any coord is not an integer, round it up):
![Image displaying where XYZ coordinates are](https://imgur.com/f6RW07F.png)
### Use Example
The next commands generates a Minecraft Map Art Animation of Bad Apple in the coords -43 120 -60, which is going towards west. The first map ID will be 1,000:
```
py main.py -n "bad_apple" -p "Path\src\bad_apple.mp4" -x "-43" -y "120" -z "-60" -d "west" -i "1000"
```
### Files generated
Two files are generated:
###### 1. **The Map Bundle**: It must be moved to the data folder in the Minecraft World the structure wants to be built in, then extracted, so all the .DAT maps can be readable for Minecraft.
###### 2. **Datapack**: Go to the world of your folder and go inside the datapacks folder and just move the .ZIP file generated there and Minecraft will be able to detect it. There's no need to extract it.

### In-game commands
#### Start the whole structure
```
/function <name>:build
```
#### Place initial blocks
```
/function <name>:place_inital_blocks
```
#### Summon item frames
```
/function <name>:summon_item_frames
```
#### Summon a boat in the starting line
```
/function <name>:place_boat
```