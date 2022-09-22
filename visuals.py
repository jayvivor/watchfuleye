import python_avatars as pa
import constants
from cairosvg import svg2png
import os
import shutil

palette = {
    "darkslategray":"#2f4f4f",
    "maroon":"#800000",
    "midnightblue":"#191970",
    "darkgreen":"#006400",
    "darkkhaki":"#bdb76b",
    "red":"#ff0000",
    "darkturquoise":"#00ced1",
    "orange":"#ffa500",
    "yellow":"#ffff00",
    "lime":"#00ff00",
    "mediumspringgreen":"#00fa9a",
    "blue":"#0000ff",
    "fuchsia":"#ff00ff",
    "cornflower":"#6495ed",
    "deeppink":"#ff1493",
    "lightpink":"#ffb6c1"
}

save_dir = "avatars/"

player_avs = {}


def initialize(cast):
    generate_icons(cast)

def generate_icons(cast):
    colors = list(palette.values()) 
    for index, player in enumerate(cast):
     av = pa.Avatar.random(background_color=colors[index%len(colors)])
     savename = f"{save_dir}{player.name.replace(' ','_')}.png"
     svg_string = av.render()
     svg2png(bytestring=svg_string, write_to=savename)
     player_avs.update({player:savename})

def clean_up():
    for filename in os.listdir(save_dir):
        file_path = os.path.join(save_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))