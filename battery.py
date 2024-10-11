from time import sleep
import RPi.GPIO as GPIO
from datetime import datetime, timedelta

from main import CheckCharge, RpiBoard, RpiPin


# Pins
charge_pin = RpiPin(4)
bypass_pin = RpiPin(5)
charge_pin.function = GPIO.OUT
bypass_pin.function = GPIO.OUT

cc = CheckCharge(
    threshold_bypass=.1,
    threshold_charge=.1,
    history=timedelta(minutes=15)
)

print('Initialization done')

while True:
    bypass, charge, both = cc()

    # State changes
    if both:
        charge_pin.state = 0
        bypass_pin.state = 0
    else:
        charge_pin.state = 1
        bypass_pin.state = 1

    sleep(15)
