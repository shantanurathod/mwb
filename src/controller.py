import socket
import json
from pynput import mouse

RECEIVER_IP = '192.168.X.X'  # Change this
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RECEIVER_IP, PORT))

prev_x, prev_y = None, None

def on_move(x, y):
    global prev_x, prev_y
    if prev_x is not None and prev_y is not None:
        dx = x - prev_x
        dy = y - prev_y
        payload = json.dumps({'dx': dx, 'dy': dy}).encode()
        try:
            s.sendall(payload)
        except Exception as e:
            print(f"Send error: {e}")
    prev_x, prev_y = x, y

with mouse.Listener(on_move=on_move) as listener:
    listener.join()
