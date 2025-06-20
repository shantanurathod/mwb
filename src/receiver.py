import socket
import pyautogui
import json

HOST = '0.0.0.0'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on port {PORT}...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with conn, conn.makefile() as f:  # makefile() turns socket into line reader
        for line in f:
            try:
                movement = json.loads(line.strip())
                dx = movement['dx']
                dy = movement['dy']
                x, y = pyautogui.position()
                pyautogui.moveTo(x + dx, y + dy)
            except Exception as e:
                print(f"Error: {e}")
