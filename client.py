import socket
import sys
import cv2
import numpy
import pickle
import struct

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

cap = cv2.VideoCapture(0)
my_username = input('Nickname: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    message_size = struct.pack('L', len(data))
    client_socket.sendall(message_size + data)
