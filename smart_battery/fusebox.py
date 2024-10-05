"""In this module all the fysical objects are represented by a python object."""
import re

from machine import Pin, Timer, UART

from common import Base


class FuseBoxReadout(Base):
    def main(self, timer):
        _ = self.wifi_connect()
        out = self.read_uart()
        print(out)
        self.blink(2)

    def read_uart(self):
        uart1 = UART(
            1,  # id
            baudrate=115200,
            bits=8,
            parity=None,
            stop=1,
            timeout=5000,
            tx=Pin(4),
            rx=Pin(5)
        )
        out = []
        while True:
            line = uart1.readline()
            out.append(line.decode('ascii').strip())
            if re.match(b'(?=!)', line):
                break
        return out
    

fbro = FuseBoxReadout()
fbro(True)
