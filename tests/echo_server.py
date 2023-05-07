import socket
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL)

HOST = "192.168.68.58"  # Standard loopback interface address (localhost, RPI 4)
# HOST = "192.168.68.55"  # Standard loopback interface address (localhost, RPI Zero 1)
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
                print(data)
            conn.sendall(b'Hi back')