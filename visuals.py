import python_avatars as pa
import constants


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




def initialize(cast):
    generate_icons(cast)



def generate_icons(cast):

    colors = list(palette.values()) 
    for index, player in enumerate(cast):
     av = pa.Avatar.random(background_color=colors[index%len(colors)])
     av.render(f"{save_dir}{player.name.replace(' ','_')}.svg")
