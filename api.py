from fastapi import FastAPI
from time import sleep


class SmartMeter:
    """This class handles all interactions with the local smart meter to get the data about current use, day/night, etc."""

    defs = {
        '1-3:0.2.8': {
            'short_name': 'P1Version',
            'long_name': 'Version information for P1 output',
            'attribute': '2',
            'class_id': '1 Data',
            'value_format': 'S2, tag 9',
            'value_unit': ''
        },
        '0-0:1.0.0': {
            'short_name': 'DateTimeElectric',
            'long_name': 'Date-time stamp of the P1 message',
            'attribute': '2',
            'class_id': '8',
            'value_formaTSTt': '',
            'value_unit': 'YYMMDDhhmmssX'
        },
        '0-0:96.1.1': {
            'short_name': 'EquipmentIDElectric',
            'long_name': 'Equipment identifier',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'Sn (n=0..96), tag 9',
            'value_unit': ''
        },
        '1-0:1.8.1': {
            'short_name': 'ElectricityToClient(1)',
            'long_name': 'Meter Reading electricity delivered to client (Tariff 1) in 0,001 kWh',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F9(3,3), tag 6',
            'value_unit': 'kWh'
        },
        '1-0:1.8.2': {
            'short_name': 'ElectricityToClient(2)',
            'long_name': 'Meter Reading electricity delivered to client (Tariff 2) in 0,001 kWh',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F9(3,3), tag 6',
            'value_unit': 'kWh'
        },
        '1-0:2.8.1': {
            'short_name': 'ElectricityByClient(1)',
            'long_name': 'Meter Reading electricity delivered by client (Tariff 1) in 0,001 kWh',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F9(3,3), tag 6',
            'value_unit': 'kWh'
        },
        '1-0:2.8.2': {
            'short_name': 'ElectricityByClient(2)',
            'long_name': 'Meter Reading electricity delivered by client (Tariff 2) in 0,001 kWh',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F9(3,3), tag 6',
            'value_unit': 'kWh'
        },
        '0-0:96.14.0': {
            'short_name': 'TariffIndicator',
            'long_name': 'Tariff indicator elec- tricity. The tariff in- dicator can also be used to switch tariff dependent loads e.g boilers. This is the responsibility of the P1 user',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'S4, tag 9',
            'value_unit': ''
        },
        '1-0:1.7.0': {
            'short_name': 'ActualElectricityToClient',
            'long_name': 'Actual electricity power delivered (+P) in 1 Watt resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '1-0:2.7.0': {
            'short_name': 'ActualElectricityByClient',
            'long_name': 'Actual electricity power received (-P) in 1 Watt resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '0-0:96.7.21': {
            'short_name': 'NPowerFailuresAny',
            'long_name': 'Number of power failures in any phase',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '0-0:96.7.9': {
            'short_name': 'NLongPowerFailuresAny',
            'long_name': 'Number of long power failures in any phase',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '1-0:99.97.0': {
            'short_name': 'LongPowerFailureLog',
            'long_name': 'Power Failure Event Log (long power failures)',
            'attribute': '2 Buffer',
            'class_id': '7 Profile Ge- neric',
            'value_format': 'TST, F10(0,0), tag 6 Format applicable for the value within the log (OBIS code 0-0:96.7.19.255)',
            'value_unit': 'Timestamp (end of failure), duration in seconds'
        },
        '1-0:32.32.0': {
            'short_name': 'NSagsL1',
            'long_name': 'Number of voltage sags in phase L1',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '1-0:52.32.0': {
            'short_name': 'NSagsL2',
            'long_name': 'Number of voltage sags in phase L2',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '1-0:72.32.0': {
            'short_name': 'NSagsL3',
            'long_name': 'Number of voltage sags in phase L3',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '1-0:32.36.0': {
            'short_name': 'NSwellsL1',
            'long_name': 'Number of voltage swells in phase L1',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '1-0:52.36.0': {
            'short_name': 'NSwellsL2',
            'long_name': 'Number of voltage swells in phase L2',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '1-0:72.36.0': {
            'short_name': 'NSwellsL3',
            'long_name': 'Number of voltage swells in phase L3',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'F5(0,0), tag 18',
            'value_unit': ''
        },
        '0-0:96.13.0': {
            'short_name': 'Message',
            'long_name': 'Text message max 1024 characters.',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'Sn (n=0..2048), tag 9',
            'value_unit': ''
        },
        '1-0:32.7.0': {
            'short_name': 'InstantVoltageL1',
            'long_name': 'Instantaneous voltage L1 in V resolution',
            'attribute': '2 Value',
            'class_id': '',
            'value_formF4(1,1), tag 18at': '',
            'value_unit': 'V'
        },
        '1-0:52.7.0': {
            'short_name': 'InstantVoltageL2',
            'long_name': 'Instantaneous voltage L2 in V resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F4(1,1), tag 18',
            'value_unit': 'V'
        },
        '1-0:72.7.0': {
            'short_name': 'InstantVoltageL3',
            'long_name': 'Instantaneous voltage L3 in V resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F4(1,1), tag 18',
            'value_unit': 'V'
        },
        '1-0:31.7.0': {
            'short_name': 'InstantCurrentL1',
            'long_name': 'Instantaneous current L1 in A resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F3(0,0), tag 18',
            'value_unit': 'A'
        },
        '1-0:51.7.0': {
            'short_name': 'InstantCurrentL2',
            'long_name': 'Instantaneous current L2 in A resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F3(0,0), tag 18',
            'value_unit': 'A'
        },
        '1-0:71.7.0': {
            'short_name': 'InstantCurrentL3',
            'long_name': 'Instantaneous current L3 in A resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F3(0,0), tag 18',
            'value_unit': 'A'
        },
        '1-0:21.7.0': {
            'short_name': 'Instant+PowerL1',
            'long_name': 'Instantaneous active power L1 (+P) in W resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '1-0:41.7.0': {
            'short_name': 'Instant+PowerL2',
            'long_name': 'Instantaneous active power L2 (+P) in W resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '1-0:61.7.0': {
            'short_name': 'Instant+PowerL3',
            'long_name': 'Instantaneous active power L3 (+P) in W resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '1-0:22.7.0': {
            'short_name': 'Instant-PowerL1',
            'long_name': 'Instantaneous active power L1 (-P) in W resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '1-0:42.7.0': {
            'short_name': 'Instant-PowerL2',
            'long_name': 'Instantaneous active power L2 (-P) in W resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '1-0:62.7.0': {
            'short_name': 'Instant-PowerL3',
            'long_name': 'Instantaneous active power L3 (-P) in W resolution',
            'attribute': '2 Value',
            'class_id': '3 Register',
            'value_format': 'F5(3,3), tag 18',
            'value_unit': 'kW'
        },
        '0-1:24.1.0': {
            'short_name': 'DeviceTypeGas',
            'long_name': 'Device-Type',
            'attribute': '9 Device type',
            'class_id': '72 M-Bus client',
            'value_format': 'F3(0,0), tag 17',
            'value_unit': ''
        },
        '0-1:96.1.0': {
            'short_name': 'EquipmentIDGas',
            'long_name': 'Equipment identifier (Gas)',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'Sn (n=0..96), tag 9',
            'value_unit': ''
        },
        '0-1:24.2.1': {
            'short_name': 'GasToClient',
            'long_name': '',
            'attribute': '2 Value""',
            'class_id': '4 Extended Register',
            'value_format': 'F8(2,2)/F8(3,3), tag 18 (See note 2)',
            'value_unit': 'm3'
        },
        '0-2:24.1.0': {
            'short_name': 'DeviceTypeThermal',
            'long_name': 'Device-Type',
            'attribute': '9 Device type',
            'class_id': '72 M-Bus cli- ent',
            'value_format': 'F3(0,0), tag 17',
            'value_unit': ''
        },
        '0-2:96.1.0': {
            'short_name': 'EquipmentIDThermal',
            'long_name': 'Equipment identifier (Thermal: Heat or Cold)',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'Sn (n=0..96), tag 9',
            'value_unit': ''
        },
        '0-2:24.2.1': {
            'short_name': 'ThermalToClient',
            'long_name': '',
            'attribute': '2 Value""',
            'class_id': '4 Extended Register',
            'value_format': 'Fn(2,2) (See note 1)',
            'value_unit': 'GJ'
        },
        '0-3:24.1.0': {
            'short_name': 'DeviceTypeWater',
            'long_name': 'Device-Type',
            'attribute': '9 Device type',
            'class_id': '72 M-Bus cli- ent',
            'value_format': 'F3(0,0), tag 17',
            'value_unit': ''
        },
        '0-3:96.1.0': {
            'short_name': 'EquipmentIDWater',
            'long_name': 'Equipment identifier (Water)',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'Sn (n=0..96), tag 9',
            'value_unit': ''
        },
        '0-3:24.2.1': {
            'short_name': 'WaterToClient',
            'long_name': '',
            'attribute': '2 Value""',
            'class_id': '4 Extended Register',
            'value_format': 'Fn(2,2) (See note 1)',
            'value_unit': 'm3'
        },
        '0-4:24.1.0': {
            'short_name': 'DeviceTypeSlave',
            'long_name': 'Device-Type',
            'attribute': '9 Device type',
            'class_id': '72 M-Bus cli- ent',
            'value_format': 'F3(0,0), tag 17',
            'value_unit': ''
        },
        '0-4:96.1.0': {
            'short_name': 'EquipmentIDSlave',
            'long_name': 'Equipment identifier',
            'attribute': '2 Value',
            'class_id': '1 Data',
            'value_format': 'Sn (n=0..96), tag 9',
            'value_unit': ''
        },
        '0-4:24.2.1': {
            'short_name': 'SlaveToClient',
            'long_name': '',
            'attribute': '2 Value""',
            'class_id': '4 Extended Register',
            'value_format': 'Fn(2,2) (See note 1)',
            'value_unit': 'kWh'
        },
    }

    def __init__(self, port="COM4", baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=5, xonxoff=False, rtscts=False):
        self.port, self.baudrate, self.bytesize, self.parity = port, baudrate, bytesize, parity
        self.stopbits, self.timeout, self.xonxoff, self.rtscts = stopbits, timeout, xonxoff, rtscts

    def transform_item(self, a):
        try:
            ki = a.index('(')
            c = list(map(lambda x: x.split('*'), re.findall(r'\((.*?)\)', a[ki:])))
            return (
                self.defs[a[:ki]]['short_name'],
                [b for a in c for b in a]
            )
        except ValueError:
            return '', ''

    def __call__(self):
        reading = self.read_meter()
        reading = map(self.transform_item, reading)
        reading = filter(lambda x: any(len(y)!=0 for y in x), reading)
        reading = dict(reading)
        return reading


# App
app = FastAPI()

@app.get("/")
async def root():
    smartm = SmartMeter(
        '/dev/ttyUSB0',
        115200, 8, 'N', 1, 5,
        False, False,
    )
    while True:
        try:
            return smartm()
        except (KeyError, ValueError):
            print('Failed to get data')
            sleep(1)
