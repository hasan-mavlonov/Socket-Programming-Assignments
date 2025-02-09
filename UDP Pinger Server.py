from socket import *
import random

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print(f'Started UDP server on port: {serverPort}')
while True:
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(1024)
    message = message.decode()
    message = message.upper()
    if rand < 4:
        continue
    serverSocket.sendto(message.encode(), address)
