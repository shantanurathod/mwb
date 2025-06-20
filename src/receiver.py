import socket
import pyautogui
import json

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999       # Same as sender

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on port {PORT}...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                movement = json.loads(data.decode())
                dx = movement['dx']
                dy = movement['dy']
                current_x, current_y = pyautogui.position()
                pyautogui.moveTo(current_x + dx, current_y + dy)
            except Exception as e:
                print(f"Error: {e}")
