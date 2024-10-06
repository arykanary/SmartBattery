from time import sleep
import RPi.GPIO as GPIO

from main import CheckCharge, RpiBoard, RpiPin


# Pins
charge_pin = RpiPin(4)
bypass_pin = RpiPin(4)
charge_pin.function = GPIO.OUT
bypass_pin.function = GPIO.OUT

cc = CheckCharge()

while True:
    bypass, charge, both = cc()
    print(both)

    # State changes
    if both:
        charge_pin.state = 1
        bypass_pin.state = 1
    # Physical design not sufficient for this
    # elif not both & charge:
    #     charge_pin.state = 1
    #     bypass_pin.state = 0
    # elif not both & bypass:
    #     charge_pin.state = 0
    #     bypass_pin.state = 1
    else:
        charge_pin.state = 0
        bypass_pin.state = 0

    sleep(1)
