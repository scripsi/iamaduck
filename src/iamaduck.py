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
button_a.was_held = False
button_b.was_held = False
button_c.was_held = False
button_d.was_held = False
indiCat = LED(23)

def toggle_indiCat(btn):
    if not btn.was_held:
      config.dbg("Button A pressed. IndiCat toggled!")
      indiCat.toggle()
    btn.was_held = False

def show_quack(btn):
    if not btn.was_held:
      config.dbg("Button B Pressed. Showing new Quack!")
      inky.set_image(screen_quacks.get_image())
      inky.show()
    btn.was_held = False

def show_cat(btn):
    if not btn.was_held:
      config.dbg("Button C Pressed. Showing new Cat!")
      inky.set_image(screen_cat.get_image())
      inky.show()
    btn.was_held = False

def show_temperature(btn):
    if not btn.was_held:
       config.dbg("Button D Pressed.")
    btn.was_held = False

def turn_off(btn):
    btn.was_held = True
    config.dbg("Button A held. Shutting down.")
    indiCat.blink(on_time=0.2,off_time=0.2)
    time.sleep(2)
    indiCat.on()
    inky.set_image(screen_help.get_image("Shutting down ...\nPlease wait 10 secs after\nIndiCat goes out\nbefore unplugging."))
    inky.show()
    os.system("sudo shutdown now")

def pause_quack(btn):
    btn.was_held = True
    config.dbg("Button B held. Pausing quack!")

def pause_cat(btn):
    btn.was_held = True
    config.dbg("Button C held. Pausing cat!")

def show_help(btn):
    btn.was_held = True
    config.dbg("Button D held. Showing help.")
    inky.set_image(screen_help.get_image())
    inky.show()

button_a.when_released = toggle_indiCat
button_a.when_held = turn_off
button_b.when_released = show_quack
button_b.when_held = pause_quack
button_c.when_released = show_cat
button_c.when_help = pause_cat
button_d.when_released = show_temperature
button_d.when_held = show_help

indiCat.blink()
config.setup()
inky.set_image(screen_help.get_image("Starting. Please wait..."))
inky.show()
time.sleep(5)
show_quack()
indiCat.off()
schedule.every(int(config.ini['screen_quacks']['refresh_interval'])).minutes.do(show_quack)

while True:
    schedule.run_pending()
    time.sleep(1)
