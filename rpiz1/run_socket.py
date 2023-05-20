import socket
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL)

# HOST = "192.168.68.58"  # Standard loopback interface address (localhost, RPI 4)
HOST = "192.168.68.60"  # Standard loopback interface address (localhost, RPI Zero 1)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def get_latest(names):
    '''Get the latest data in ready to send via socket'''
    import pandas as pd
    from glob import glob
    latest = sorted(glob('_data/P1_log/*.csv'), reverse=True)[0]
    df = pd.read_csv(latest, index_col=0).T[names]
    bit = ','.join(df.values[0]).encode('ascii')
    print(bit)
    return bit


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if data:
                print('Client wants the current: ', data)
                _return = get_latest(data.decode('ascii').split(','))
                conn.sendall(_return)
            else:
                conn.sendall(b'I have no idea')
