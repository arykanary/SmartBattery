# echo-client.py

import socket

HOST = "192.168.68.58"  # Standard loopback interface address (localhost, RPI 4)
# HOST = "192.168.68.55"  # Standard loopback interface address (localhost, RPI Zero 1)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")