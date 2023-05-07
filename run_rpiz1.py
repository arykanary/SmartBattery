"""
hostname : 192.168.68.55
"""
from main import *
import socket
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL)

HOST = "192.168.68.55"  # Standard loopback interface address (localhost, RPI Zero 1)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if data:
                data = data.decode('ascii')
                print('Client wants', data)

                smartm = SmartMeter(
                    port="/dev/ttyUSB0",
                    baudrate=115200,
                    bytesize=8,
                    parity="N",
                    stopbits=1,
                    timeout=5,
                    xonxoff=False,
                    rtscts=False
                )
                _return = smartm([data]).values[0][0].encode('ascii')

                conn.sendall(_return)

    print(f"Received {data!r}")