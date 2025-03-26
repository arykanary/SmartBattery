import os
import requests
import numpy as np
import json
import warnings
from time import sleep
from datetime import datetime, timedelta

# RPI specific stuff
import serial
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3004 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn




class CheckCharge:
    base_date = datetime(1970, 1, 1)
    data_path = os.path.join('_data', 'P1')

    def __init__(self, threshold_bypass: float=.1, threshold_charge: float=.1, history: timedelta=timedelta(minutes=30)):
        self._dates  = []
        self._values = []

        self.t_bypass = threshold_bypass
        self.t_charge = threshold_charge
        self.history  = history
        os.makedirs(self.data_path, exist_ok=True)

    def __call__(self):
        self.get_data()
        self.purge_history()
        bypass, charge, both = self.decide()
        return bypass, charge, both

    def get_data(self):
        resp = requests.request('GET', 'http://192.168.68.59:8000/')
        resp = eval(resp.content.decode())
        with open(os.path.join(self.data_path, datetime.now().strftime(r"%Y%m%d%H%M%S")+'.json'), 'w') as jf:
            json.dump(resp, jf)

        _date = resp.get('DateTimeElectric')
        _tocl = resp.get('ActualElectricityToClient')
        _bycl = resp.get('ActualElectricityByClient')

        if (_date is not None and _tocl is not None and _bycl is not None):
            _date = _date[0]
            _tocl = float(_tocl[0])
            _bycl = float(_bycl[0])
            _date = datetime(2000+int(_date[0:2]), int(_date[2:4]), int(_date[4:6]),
                             int(_date[6:8]), int(_date[8:10]), int(_date[10:12]))

            self._dates.append((_date-self.base_date).total_seconds())
            self._values.append(-_tocl if _tocl > 0 else _bycl)

        return resp

    def purge_history(self):
        try:
            purge_date = self._dates[-1] - self.history.total_seconds()
            self._dates  = [d for d, v in zip(self._dates, self._values) if d > purge_date]
            self._values = [v for d, v in zip(self._dates, self._values) if d > purge_date]
        except IndexError:
            pass

    def decide(self):
        if len(self._values) < 2:
            return False, False, False

        pol = np.polynomial.Polynomial.fit(self._dates, self._values, 1)
        _p = pol((datetime.now()-self.base_date).total_seconds()+self.history.total_seconds())
        _m = np.mean(self._values)
        bypass = (_m - self.t_bypass)>0, _p>0,
        charge = (_m - self.t_charge)>0, _p>0,
        both   = (_m - (self.t_charge + self.t_bypass))>0, _p>0,
        print(
            f'Latest date: {datetime.fromtimestamp(self._dates[-1])} with value {self._values[-1]:.2f} - '
            f'A mean of {_m:.2f} in the over last period and a prediction of {_p:.2f} at the end the coming period - ',
            f'Bypass {bypass}, Charging {charge}, Both {both}'
        )

        return all(bypass), all(charge), all(both)


# == RPI interaction objects ==
class RpiBoard:
    """This class creates a sustainable way of setting up the board.

    https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
    """
    pins = [
    # 'BoardNo', 'BCMNo', 'Type'
        (1,  None, '3.3V'),
        (2,  None, '5.0V'),
        (3,  2,    ('GPIO', 'SDA1', 'I2C')),
        (4,  None, '5.0V'),
        (5,  3,    ('GPIO', 'SDA1', 'I2C')),
        (6,  None, 'GROUND'),
        (7,  4,    ('GPIO', 'GCLK')),
        (8,  14,   ('GPIO', 'TX UART')),
        (9,  None, 'GROUND'),
        (10, 15,   ('GPIO', 'RX UART')),
        (11, 17,   'GPIO'),
        (12, 18,   'GPIO'),
        (13, 27,   'GPIO'),
        (14, None, 'GROUND'),
        (15, 22,   'GPIO'),
        (16, 23,   'GPIO'),
        (17, None, '3.3V'),
        (18, 24,   'GPIO'),
        (19, 20,   ('MOSI', 'SPI')),
        (20, None, 'GROUND'),
        (21, 9,    ('MISO', 'SPI')),
        (22, 25,   'GPIO'),
        (23, 11,   ('SCLK', 'SPI')),
        (24, 8,    ('CEO_N', 'SPI')),
        (25, None, 'GROUND'),
        (26, 7,    ('CE1_N', 'SPI')),
        (27, None, 'RESERVED'),
        (28, None, 'RESERVED'),
        (29, 5,    'GPIO'),
        (30, None, 'GROUND'),
        (31, 6,    'GPIO'),
        (32, 12,   'GPIO'),
        (33, 13,   'GPIO'),
        (34, None, 'GROUND'),
        (35, 19,   'GPIO'),
        (36, 16,   'GPIO'),
        (37, 26,   'GPIO'),
        (38, 20,   'GPIO'),
        (39, None, 'GROUND'),
        (40, 21,   'GPIO'),
    ]

    def __init__(self, mode):
        self.mode = mode
        self.active_pins = {}

    def __enter__(self):
        if not GPIO.getmode():
            GPIO.setmode(self.mode)
        else:
            self.mode = GPIO.getmode()

    def __exit__(self, *args, **kwargs):
        GPIO.cleanup()

    @property
    def board(self):
        return GPIO.RPI_INFO


class RpiPin:
    """This class can be used to easily interact with a pin on a RPI"""
    def __init__(self, pin: int):
        self._pin = pin
        self._func = None

    @property
    def state(self):
        return GPIO.input(self._pin)

    states = [GPIO.IN, GPIO.OUT, GPIO.SPI, GPIO.I2C, GPIO.HARD_PWM, GPIO.SERIAL, GPIO.UNKNOWN]
    @state.setter
    def state(self, state):
        GPIO.output(self._pin, state)

    @property
    def function(self):
        self._func = GPIO.gpio_function(self._pin)
        return self._func

    @function.setter
    def function(self, func):
        self._func = func
        GPIO.setup(self._pin, func)


def mcp3004_chan():
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)  # create the spi bus
    cs = digitalio.DigitalInOut(board.D5)  # create the cs (chip select)
    mcp = MCP.MCP3004(spi, cs, 5.)  # create the mcp object
    return AnalogIn(mcp, MCP.P0)  # create an analog input channel on pin 0


def read_chan(chan, calib=(0., 5.)):
    measurement = 0.
    for n, c in enumerate(calib):
        measurement += c * chan.voltage ** n
    return chan.value, chan.voltage, measurement

    warnings.warn('Not a Raspberry Pi')


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
