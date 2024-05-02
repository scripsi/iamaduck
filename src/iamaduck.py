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
import screen_cat
import screen_help
import os
from configparser import ConfigParser

print("""I am a Duck

Quack quack!

""")

inky = Inky()
button_a = Button(5,hold_time=2)
button_b = Button(6,hold_time=2)
button_c = Button(16,hold_time=2)
button_d = Button(24,hold_time=2)
indiCat = LED(23)


def show_quack():
    inky.set_image(screen_quacks.get_image())
    inky.show()

def show_cat():
    inky.set_image(screen_cat.get_image())
    inky.show()

def toggle_indiCat():
    config.dbg("indiCat toggled!")
    indiCat.toggle()

def turn_off():
    config.dbg("Button A held. Shutting down.")
    indiCat.blink(on_time=0.2,off_time=0.2)
    inky.set_image(screen_help.get_image("Shutting down ...\nPlease wait 10 secs after\nIndiCat goes out\nbefore unplugging.\n"))
    #time.sleep(2)
    indiCat.on()
    os.system("sudo shutdown now")

def show_help():
    config.dbg("Button D held. Showing help.")
    inky.set_image(screen_help.get_image())
    inky.show()

button_a.when_pressed = toggle_indiCat
button_a.when_held = turn_off
button_b.when_pressed = show_quack
button_c.when_pressed = show_cat
button_d.when_pressed = show_quack
button_d.when_held = show_help

indiCat.blink()
config.setup()
inky.set_image(screen_help.get_image("Starting. Please wait...\n"))
inky.show()
time.sleep(5)
show_quack()
indiCat.off()
schedule.every(int(config.ini['screen_quacks']['refresh_interval'])).minutes.do(show_quack)

while True:
    schedule.run_pending()
    time.sleep(1)
