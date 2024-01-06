#!/usr/bin/env python

# import lots of necessary stuff
import PIL
import config
import schedule
import time
from inky.inky_uc8159 import Inky
from gpiozero import Button, LED
from signal import pause
import screen_startup
import screen_quacks
import os
from configparser import ConfigParser

print("""I am a Duck

Quack quack!

""")

inky = Inky()
button_a = Button(5,hold_time=2)
button_b = Button(6)
button_c = Button(16)
button_d = Button(24)
indiCat = LED(23)


def show_image(image_to_show):

    if image_to_show == "quacks":
        screen_quacks.update_image()
        inky.set_image(screen_quacks.get_image())
        inky.show()

def show_quacks():
    show_image("quacks")

def toggle_indiCat():
    config.dbg("indiCat toggled!")
    indiCat.toggle()

def turn_off():
    config.dbg("Button A held. Shutting down.")
    indiCat.blink(on_time=0.2,off_time=0.2)
    time.sleep(2)
    indiCat.on()
    os.system("sudo shutdown now")

button_a.when_pressed = toggle_indiCat
button_a.when_held = turn_off
button_b.when_released = show_quacks
button_c.when_released = show_quacks
button_d.when_released = show_quacks

indiCat.blink()
config.setup()
config.dbg("Debugging enabled!")
screen_startup.update_image()
inky.set_image(screen_startup.get_image())
inky.show()
time.sleep(5)
screen_quacks.setup()
show_quacks()
indiCat.off()
schedule.every(int(config.ini['screen_quacks']['refresh_interval'])).minutes.do(show_quacks)

while True:
    schedule.run_pending()
    time.sleep(1)
