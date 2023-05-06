"""
hostname : 192.168.68.55
"""
from main import *


if __name__ == "__main__":
    # smartm = SmartMeter(port="COM4", baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=5, xonxoff=False, rtscts=False)  # Windows
    smartm = SmartMeter(port="/dev/ttyUSB0", baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=5, xonxoff=False, rtscts=False)  # RPI4
    print(smartm())