from socket import *
import time

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = ('localhost', serverPort)
serverSocket.settimeout(1)
try:
    for i in range(1, 11):
        start = time.time()
        message = "Ping # " + str(i) + " " + time.ctime(start)
        try:
            sent = serverSocket.sendto(message.encode(), serverAddress)
            print("Sent: " + message)
            data, server = serverSocket.recvfrom(1024)
            print("Received: " + data.decode())
            end = time.time()
            elapsed = end - start
            print("RTT: " + str(elapsed) + "seconds\n")
        except socket.timeout:
            print("#" + str(i) + " Requested Time out\n")
finally:
    print("Closing socket")
    serverSocket.close()
