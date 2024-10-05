"""In this module all the fysical objects are represented by a python object."""
import re
import serial
from datetime import datetime
import pandas as pd
import time
import os
import requests
import warnings

try:
    # RPI specific stuff
    import RPi.GPIO as GPIO
    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3004 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn
    import usocket as socket
    import ustruct as struct
    from ubinascii import hexlify
except ImportError:
    warnings.warn('This is not a RPI or not all packages are installed')

from common import Base


class BatteryControl(Base):
    # Feedback methods
    def measure_charge(self):  pass

    # Control methods
    def bypass(self, val: bool):  pass
    def charge(self, val: bool):  pass
    def convert(self, val: bool):  pass


class Charger:
    def status(self): pass


class Converter:
    def status(self): pass
