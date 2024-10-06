from fastapi import FastAPI
from time import sleep
from main import SmartMeter


app = FastAPI()

@app.get("/")
async def root():
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
            return smartm()
        except (KeyError, ValueError):
            print('Failed to get data')
            sleep(1)
