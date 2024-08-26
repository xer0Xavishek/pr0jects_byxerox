import socket
import cv2
import numpy as np
import subprocess

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(0)
    print("Server listening on port 12345")

    connection, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    ffmpeg_command = [
        'ffmpeg',
        '-f', 'rawvideo',
        '-pixel_format', 'bgr24',
        '-video_size', '640x480',
        '-framerate', '30',
        '-i', '-',
        '-f', 'mpegts',
        'udp://127.0.0.1:12346'
    ]

    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    try:
        while True:
            length = recvall(connection, 16)
            if length is None:
                print("No data received. Closing connection.")
                break
            stringData = recvall(connection, int(length))
            if stringData is None:
                print("No data received. Closing connection.")
                break
            data = np.frombuffer(stringData, dtype='uint8')
            frame = cv2.imdecode(data, 1)
            if frame is None:
                print("Frame decoding failed. Closing connection.")
                break
            process.stdin.write(frame.tobytes())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()
        process.stdin.close()
        process.wait()
        print("Connection closed.")

if __name__ == "__main__":
    start_server()
