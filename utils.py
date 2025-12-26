import init_fake_rpi
import RPi.GPIO as gpio
from importlib.metadata import version


def print_rpi_versions():

    if hasattr(gpio, 'RPI_INFO'):
        info = gpio.RPI_INFO
        print("P1_REVISION: {}".format(info['P1_REVISION']))
        print("REVISION: {}".format(info['REVISION']))
        print("TYPE: {}".format(info['TYPE']))
        print("MANUFACTURER: {}".format(info['MANUFACTURER']))
        print("PROCESSOR version: {}".format(info['PROCESSOR']))
        print("RAM: {}".format(info['RAM']))
        print("RPi.GPIO version: {}".format(version('RPi.GPIO')))
    else:
        print("Printing RPi info is not supported in fake_rpi.")
