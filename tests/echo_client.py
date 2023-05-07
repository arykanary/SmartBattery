# echo-client.py

import socket

# HOST = "192.168.68.58"  # Standard loopback interface address (localhost, RPI 4)
HOST = "192.168.68.55"  # Standard loopback interface address (localhost, RPI Zero 1)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # P1Version, DateTimeElectric, EquipmentIDElectric,
    # ElectricityToClient(1), ElectricityToClient(2), ElectricityByClient(1), ElectricityByClient(2),
    # TariffIndicator, ActualElectricityToClient, ActualElectricityByClient,
    # NPowerFailuresAny, NLongPowerFailuresAny, LongPowerFailureLog, NSagsL1, NSagsL2, NSagsL3,
    # NSwellsL1, NSwellsL2, NSwellsL3, Message, InstantVoltageL1, InstantVoltageL2, InstantVoltageL3,
    # InstantCurrentL1, InstantCurrentL2, InstantCurrentL3,
    # Instant+PowerL1, Instant+PowerL2, Instant+PowerL3,
    # Instant-PowerL1, Instant-PowerL2, Instant-PowerL3,
    # DeviceTypeGas, EquipmentIDGas, DateTimeGas, GasToClient, DeviceTypeThermal, EquipmentIDThermal,
    # DateTimeThermal, ThermalToClient, DeviceTypeWater, EquipmentIDWater, DateTimeWater,
    # WaterToClient, DeviceTypeSlave, EquipmentIDSlave, DateTimeSlave, SlaveToClient

    s.sendall(b"ElectricityToClient(1)")
    data = s.recv(1024)

print(f"Received {data!r}")