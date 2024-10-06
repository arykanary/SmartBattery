import re
import serial
import os
import requests
import yaml
# RPI specific stuff
import RPi.GPIO as GPIO
#import busio
#import digitalio
#import board
#import adafruit_mcp3xxx.mcp3004 as MCP
#from adafruit_mcp3xxx.analog_in import AnalogIn


# == Data-source objects ==
class EexApi:
    """This class handles all interactions with the EEX API to get the data about current prices, volumnes, etc.
    https://www.eex.com/en/market-data/eex-group-datasource/api
    """
    # ToDo: API is fucking expensive
    base_url = "https://api.eex.com/data/spot/power/monthly/auction/nl"

    def __init__(self):
        pass

    def call_api(self):
        response = requests.get(self.base_url)

        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
        
    def retrieve_value(self, name):
        pass
        

class SmartMeter:
    """This class handles all interactions with the local smart meter to get the data about current use, day/night, etc."""
    def __init__(self, port="COM4", baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=5, xonxoff=False, rtscts=False):
        self.port, self.baudrate, self.bytesize, self.parity = port, baudrate, bytesize, parity
        self.stopbits, self.timeout, self.xonxoff, self.rtscts = stopbits, timeout, xonxoff, rtscts

        with open(os.path.join(os.path.dirname(__file__), 'definitions.yaml')) as yf:
            self.defs = yaml.safe_load(yf)['definitions']

    def read_meter(self):
        out = []
        with serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
            timeout=self.timeout,
            xonxoff=self.xonxoff,
            rtscts=self.rtscts,
        ) as ser:
            while True:
                telegram_line = ser.readline()
                out.append(telegram_line.decode('ascii').strip())

                if re.match(b'(?=!)', telegram_line):
                    break

        return out
    
    def transform_item(self, a):
        try:
            ki = a.index('(')
            return (
                self.defs[a[:ki]]['short_name'],
                list(map(lambda x: x.split('*'), re.findall(r'\((.*?)\)', a[ki:])))
            )
        except ValueError:
            return a, ''

    def __call__(self, names=['DateTimeElectric', 'ActualElectricityToClient', 'ActualElectricityByClient'], save=True):
        """"""
        reading = self.read_meter()
        reading = dict(map(self.transform_item, reading))
        print(*reading.items(), sep='\n')
        

class SolarPanel:
    """This class handles all interactions with the solar-panel control system to get the data about current charge, state, etc."""
    # ToDo: Can start this once the solarpanel are in place.
    def __init__(self):
        pass


class Predict:
    """This class can be used to attempt to predict power usage, price, etc."""
    def __init__(self):
        pass


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


if __name__ == "__main__":
    # with RpiBoard(GPIO.BOARD) as rpi_board:
    #     led_pin = RpiPin(40)
    #     led_pin.function = GPIO.OUT

    #     rel_pin = RpiPin(11)
    #     rel_pin.function = GPIO.OUT

    #     print('init state', led_pin.state, rel_pin.state)

    #     while True:
    #         led_pin.state = not led_pin.state
    #         rel_pin.state = not rel_pin.state
    #         print(led_pin.state, rel_pin.state)
    #         c = input('continue?')
    #         if len(c)>0:
    #             break  

    # smartm = SmartMeter(port="COM4", baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=5, xonxoff=False, rtscts=False)  # Windows
    # smartm = SmartMeter(port="/dev/ttyUSB0", baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=5, xonxoff=False, rtscts=False)  # RPI4
    # print(smartm())

    pass  # everything before the pass has been tested and works.
    # run()
