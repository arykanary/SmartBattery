from main import SmartMeter
from time import sleep

while True:
    try:
        smartm = SmartMeter(
            '/dev/ttyUSB0',
            115200,
            8,
            'N',
            1,
            5,
            False,
            False
        )
        print(smartm(None))
        sleep(60*10)
    except KeyError:
        print('Failed to get data')
        sleep(1)
