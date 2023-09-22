#!/usr/bin/env python

# import lots of necessary stuff
import PIL
import config
import schedule
import time
from inky.inky_uc8159 import Inky
from gpiozero import Button
from signal import pause
import screen_quacks
import os
from configparser import ConfigParser

print("""I am a Duck

Quack quack!

""")

inky = Inky()
button_a = Button(5)
button_b = Button(6)
button_c = Button(16)
button_d = Button(24)



def show_image(image_to_show):

    if image_to_show == "quacks":
        screen_quacks.update_image()
        inky.set_image(screen_quacks.get_image())
        inky.show()

def show_quacks():
    show_image("quacks")


button_a.when_released = show_quacks
button_b.when_released = show_quacks
button_c.when_released = show_quacks
button_d.when_released = show_quacks

config.setup()
config.dbg("Debugging enabled!")
screen_quacks.setup()
show_quacks()
schedule.every(int(config.ini['screen_quacks']['refresh_interval'])).minutes.do(show_quacks)

while True:
    schedule.run_pending()
    time.sleep(1)
