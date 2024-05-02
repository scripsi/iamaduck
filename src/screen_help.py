# import lots of necessary stuff
import config
from PIL import Image,ImageDraw,ImageFont
import random
import math
import socket
import subprocess

LEADING = 2
MARGIN = 20

img = Image.open("home/anas/iamaduck/assets/img/help-page.png")
# img = Image.new(mode='P',size=(config.WIDTH,config.HEIGHT), color=config.WHITE)
img_draw = ImageDraw.Draw(img)

font = "/home/anas/iamaduck/assets/fonts/Merriweather/Merriweather-Regular.ttf"

def get_image():
    """Returns an image to be displayed on the screen
    """

    messages = ["I am a Duck on:\n"]
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

    ax, ay, bx, by = img_draw.multiline_textbbox((0,0),message,font=output_font,align="left",spacing=LEADING)
    x = 310
    y = ((config.HEIGHT - (by - ay)) / 2) - ay
    img_draw.rectangle([0,0,config.WIDTH,config.HEIGHT],fill=bg)
    img_draw.multiline_text((x,y),message,fill=fg,font=output_font,spacing=LEADING,align="center")

    return img
