import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3004 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


def mcp3004_chan():
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)  # create the spi bus
    cs = digitalio.DigitalInOut(board.D5)  # create the cs (chip select)
    mcp = MCP.MCP3004(spi, cs)  # create the mcp object
    return AnalogIn(mcp, MCP.P0)  # create an analog input channel on pin 0
    
    
def read_chan(chan, calib=(0., 5.)):
    measurement = chan.voltage
    for n, c in enumerate(calib):
        if n == 0:
            measurement += c
        else:
            measurement *= c**n
    return chan.value, chan.voltage, measurement


print(*read_chan(mcp3004_chan()))