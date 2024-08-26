import socket
import cv2

# Set up socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.107', 12345))

capture = cv2.VideoCapture(0)

try:
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        # Encode frame as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = frame.tobytes()

        # Send frame size and frame
        client_socket.sendall(str(len(data)).ljust(16).encode('utf-8'))
        client_socket.sendall(data)
finally:
    capture.release()
    client_socket.close()
