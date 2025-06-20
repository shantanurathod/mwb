import socket
import json
import time
import threading
from pynput import mouse

RECEIVER_IP = '192.168.24.120'  # replace with actual IP
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RECEIVER_IP, PORT))

# Shared delta values
delta = {'dx': 0, 'dy': 0}
lock = threading.Lock()

def on_move(x, y):
    global prev_x, prev_y
    with lock:
        if hasattr(on_move, "prev_x"):
            delta['dx'] += x - on_move.prev_x
            delta['dy'] += y - on_move.prev_y
        on_move.prev_x = x
        on_move.prev_y = y

def sender_loop():
    while True:
        time.sleep(0.05)  # every 50ms
        with lock:
            if delta['dx'] != 0 or delta['dy'] != 0:
                payload = json.dumps(delta) + "\n"
                try:
                    s.sendall(payload.encode())
                except Exception as e:
                    print(f"Send error: {e}")
                delta['dx'], delta['dy'] = 0, 0  # reset

# Start the sender thread
threading.Thread(target=sender_loop, daemon=True).start()

# Start mouse listener
with mouse.Listener(on_move=on_move) as listener:
    listener.join()
