from socket import *
import os

serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print('The web server is up on port:', serverPort)

while True:
    print('Waiting for a connection')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        print(message, '::', message.split()[0], ':', message.split()[1])

        filename = message.split()[1]
        filepath = filename[1:]

        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                output = f.read()

            # Send HTTP response header
            connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')
            connectionSocket.sendall(output.encode())  # Send entire file content
        else:
            # Send 404 error if file does not exist
            connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')

    except Exception as e:
        print("Error:", e)
        connectionSocket.send(b'HTTP/1.1 500 Internal Server Error\r\n\r\n')

    connectionSocket.close()
