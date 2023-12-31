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

def setup():
    """Initialises values
    """
    
    
    config.dbg("screen_startup: setup")
    
    # print(quacks)

def get_image():
    """Returns an image to be displayed on the screen
    """

    return img

def update_image():
    """Updates the image in preparation for display
    """

    messages = ["I am a Duck is starting on:\n"]
    hostcmd = ('hostname')
    hostresult = subprocess.run(hostcmd, capture_output=True, text=True)
    hostname = hostresult.stdout
    ipcmd = ('hostname', '-I')
    ipresult = wifiresult = subprocess.run(ipcmd, capture_output=True, text=True)
    ipaddr = ipresult.stdout
    wificmd = ('iwgetid', '-r')
    wifiresult = subprocess.run(wificmd, capture_output=True, text=True)
    wifi=wifiresult.stdout
    messages.append(hostname)
    messages.append(ipaddr)
    messages.append(wifi)
    message='\n'.join(messages)
    bg,fg = (config.BLACK,config.WHITE)

    output_font = ImageFont.truetype(font, 24)

    ax, ay, bx, by = img_draw.multiline_textbbox((0,0),message,font=output_font,align="center",spacing=LEADING)
    x = ((config.WIDTH - (bx - ax)) / 2) - ax
    y = ((config.HEIGHT - (by - ay)) / 2) - ay
    img_draw.rectangle([0,0,config.WIDTH,config.HEIGHT],fill=bg)
    img_draw.multiline_text((x,y),message,fill=fg,font=output_font,spacing=LEADING,align="center")
