import RPi.GPIO as gpio
from time import sleep
from utils import key_pressed, consume_key

def blink_led(channel=None):
    if channel is not None:
        print(f"Button pressed on channel {channel}, blinking LED.")

    gpio.output(LED_PIN, gpio.HIGH)
    sleep(1)
    gpio.output(LED_PIN, gpio.LOW)
    sleep(1)

gpio.setmode(gpio.BCM)
LED_PIN = 17
gpio.setup(LED_PIN, gpio.OUT)

blink_led()

BUTTON_PIN = 26

gpio.setup(BUTTON_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.add_event_detect(BUTTON_PIN, gpio.FALLING, bouncetime=300,
                      callback=blink_led)

print("Press any key to exit...")

while True:
    if key_pressed():
        consume_key()
        break
    sleep(0.01)

gpio.cleanup()

