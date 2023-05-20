import socket
import pandas as pd
import numpy as np
from main import read_chan, mcp3004_chan, RpiPin
import RPi.GPIO as GPIO
from time import sleep


while True:
    HOST = "192.168.68.60"  # Standard loopback interface address (localhost, RPI Zero 1)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        names = "DateTimeElectric", "ActualElectricityToClient", "ActualElectricityByClient", "TariffIndicator"
        s.sendall(','.join(names).encode('ascii'))
        data = s.recv(1024).decode('ascii').split(',')
        data = pd.Series(dict(zip(names, data)))
        data.name = data.pop(names[0])
        data = data.astype(float)

    def switch_relay(new):
        relpin = RpiPin(4)
        relpin.function = GPIO.OUT
        if relpin.state != new:
            relpin.state = new
        return relpin.state

    _, _, charge = read_chan(mcp3004_chan())
    data['Charge'] = charge
    data['ActualSurplusFromClient'] = data['ActualElectricityByClient'] - data['ActualElectricityToClient']
    data.drop(['ActualElectricityByClient', 'ActualElectricityToClient'], inplace=True)

    print(data)

    data['ActualSurplusFromClient'] = 2 * data['ActualSurplusFromClient']
    data['Charge']                  = 2 / data['Charge']
    data['TariffIndicator']         = 6 * data['TariffIndicator']
    
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.fillna(0., inplace=True)
    
    print(data)
    print(data.sum())

    if data.sum() > 2.2:
        relay = switch_relay(0)
    else:
        relay = switch_relay(1)

    sleep(5)
