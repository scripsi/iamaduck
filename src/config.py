import os,sys
from configparser import ConfigParser
import bme680

ini = ConfigParser()
progname = os.path.basename(sys.argv[0])
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

# Inky Impression Parameters
PALETTE = [57, 48, 57, 255, 255, 255, 58, 91, 70, 61, 59, 94, 156, 72, 75, 208, 190, 71,77, 106, 73, 255, 255, 255]
BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
CLEAN = 7

WIDTH = 600
HEIGHT = 448

def setup():
    """Read and set up config
    """
    ini_file = "/mnt/iamaduck/iamaduck.ini"
    ini.read(ini_file)

    sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

def dbg(dbg_message):
    """Show a debug message if enabled
    """
    if ini['default']['debug']:
      print(progname + ": " + dbg_message)
      with open("/dev/ttyAMA0","w") as tty:
        tty.write(progname + ": " + dbg_message + "\n")
