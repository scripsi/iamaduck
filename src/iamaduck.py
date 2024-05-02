#!/usr/bin/env python

# import lots of necessary stuff
import config
import schedule
import time
from inky.inky_uc8159 import Inky
from gpiozero import Button, LED
import screen_quacks
import screen_cat
import screen_temperature
import screen_help
import os

print("""I am a Duck

Quack quack!

""")

inky = Inky()

Button.was_held = False

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

def show_temperature():
    inky.set_image(screen_temperature.get_image())
    inky.show()

def show_help(message=""):
    inky.set_image(screen_help.get_image(message))
    inky.show()

def toggle_indiCat(btn):
    if not btn.was_held:
      config.dbg("Button A pressed. IndiCat toggled!")
      indiCat.toggle()
    btn.was_held = False

def select_quack(btn):
    if not btn.was_held:
      config.dbg("Button B Pressed. Showing new Quack!")
      show_quack()
    btn.was_held = False

def select_cat(btn):
    if not btn.was_held:
      config.dbg("Button C Pressed. Showing new Cat!")
      show_cat()
    btn.was_held = False

def select_temperature(btn):
    if not btn.was_held:
      config.dbg("Button D Pressed. Showing temperature!")
      show_temperature()
    btn.was_held = False

def select_shutdown(btn):
    btn.was_held = True
    config.dbg("Button A held. Shutting down.")
    indiCat.blink(on_time=0.2,off_time=0.2)
    time.sleep(2)
    indiCat.on()
    show_help("Shutting down ...\nPlease wait 10 secs after\nIndiCat goes out\nbefore unplugging.")
    os.system("sudo shutdown now")

def save_quack(btn):
    btn.was_held = True
    config.dbg("Button B held. Pausing quack!")

def save_cat(btn):
    btn.was_held = True
    config.dbg("Button C held. Pausing cat!")

def select_help(btn):
    btn.was_held = True
    config.dbg("Button D held. Showing help.")
    show_help("Showing help.\nPress another button to exit.")
    
button_a.when_released = toggle_indiCat
button_a.when_held = select_shutdown
button_b.when_released = select_quack
button_b.when_held = save_quack
button_c.when_released = select_cat
button_c.when_held = save_cat
button_d.when_released = select_temperature
button_d.when_held = select_help

indiCat.blink()
config.setup()
show_help("Starting. Please wait...")
time.sleep(5)
show_quack()
indiCat.off()
schedule.every(int(config.ini['screen_quacks']['refresh_interval'])).minutes.do(show_quack)

while True:
    schedule.run_pending()
    time.sleep(1)
