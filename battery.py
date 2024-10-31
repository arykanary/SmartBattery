from time import sleep
import RPi.GPIO as GPIO
from datetime import timedelta

from main import CheckCharge, RpiBoard, RpiPin


# Pins
charge_min_pin = RpiPin(17)
charge_max_pin = RpiPin(27)
charge_min_pin.function = GPIO.OUT
charge_max_pin.function = GPIO.OUT

bypass_min_pin = RpiPin(5)
bypass_max_pin = RpiPin(6)
bypass_min_pin.function = GPIO.OUT
bypass_max_pin.function = GPIO.OUT

convert_min_pin = RpiPin(23)
convert_max_pin = RpiPin(24)
convert_min_pin.function = GPIO.OUT
convert_max_pin.function = GPIO.OUT

bypass_min_pin.state = bypass_max_pin.state = 1
charge_min_pin.state = charge_max_pin.state = 1
convert_min_pin.state = convert_max_pin.state = 1

# Determine current state each 15 seconds
cc = CheckCharge(
    threshold_bypass=.1,
    threshold_charge=.1,
    history=timedelta(minutes=30)
)

print('Initialization done')

while True:
    bypass, charge, both = cc()

    # State changes
    charge_min_pin.state = charge_max_pin.state = charge
    bypass_min_pin.state = bypass_max_pin.state = both
    
    convert_min_pin.state = convert_max_pin.state = not bypass_min_pin.state

    sleep(15)
