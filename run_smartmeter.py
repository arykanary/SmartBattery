from smart_battery.main import SmartMeter
from time import sleep

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
while True:
    try:
        print(smartm())
    except (KeyError, ValueError):
        print('Failed to get data')

    sleep(1)
