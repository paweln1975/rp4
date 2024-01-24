import sys
import RPi.GPIO as gpio
from importlib.metadata import version


def print_rpi_versions():

    if "init_fake_rpi" in sys.modules:
        print("Version printing is not supported")
        return

    print("RPi.GPIO version: {}".format(version('RPi.GPIO')))

    info = gpio.RPI_INFO
    print("P1_REVISION: {}".format(info['P1_REVISION']))
    print("REVISION: {}".format(info['REVISION']))
    print("TYPE: {}".format(info['TYPE']))
    print("MANUFACTURER: {}".format(info['MANUFACTURER']))
    print("PROCESSOR version: {}".format(info['PROCESSOR']))
    print("RAM: {}".format(info['RAM']))
