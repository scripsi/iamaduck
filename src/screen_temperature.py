# import lots of necessary stuff
import config
from PIL import Image,ImageDraw,ImageFont
import random
import math
import socket
import subprocess

LEADING = 2
MARGIN = 20

img = Image.new(mode='P',size=(config.WIDTH,config.HEIGHT), color=config.WHITE)
img_draw = ImageDraw.Draw(img)

font = "/home/anas/iamaduck/assets/fonts/Merriweather/Merriweather-Regular.ttf"

def get_image():
    """Returns an image to be displayed on the screen
    """

    if config.sensor.get_sensor_data():
        output = 'Temperature: {0:.2f} C\nPressure: {1:.2f} hPa\nHumidity{2:.3f} %RH'.format(
                config.sensor.data.temperature,
                config.sensor.data.pressure,
                config.sensor.data.humidity)
    else:
        output = "Can't read temperature!"

    bg,fg = (config.BLUE,config.WHITE)

    output_font = ImageFont.truetype(font, 24)

    ax, ay, bx, by = img_draw.multiline_textbbox((0,0),output,font=output_font,align="left",spacing=LEADING)
    x = ((config.WIDTH - (bx - ax)) / 2) - ax
    y = ((config.HEIGHT - (by - ay)) / 2) - ay
    img_draw.rectangle([0,0,config.WIDTH,config.HEIGHT],fill=bg)
    img_draw.multiline_text((x,y),output,fill=fg,font=output_font,spacing=LEADING,align="left")

    return img
