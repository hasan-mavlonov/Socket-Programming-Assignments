from socket import *
import os

serverPort = 8080  # Ensure it matches your curl request
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Avoid "Address already in use" error
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

print('The web server is up on port:', serverPort)

while True:
    print('Waiting for a connection...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()

        # 🔍 Debugging: Print the raw request
        print("Received request (raw):", repr(message))

        # If the request is empty, ignore it
        if not message.strip():
            connectionSocket.close()
            continue

        # Extract the requested filename
        request_parts = message.split()
        if len(request_parts) < 2:
            print("Malformed request, closing connection.")
            connectionSocket.close()
            continue

        filename = request_parts[1].lstrip("/")  # Remove leading "/"

        # Ensure file exists
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                output = f.read()

            # Construct HTTP response
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(output)}\r\n\r\n{output}"
            connectionSocket.sendall(response.encode())
        else:
            # If file doesn't exist, send 404 response
            connectionSocket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')

    except Exception as e:
        print("Error:", e)
        connectionSocket.sendall(b'HTTP/1.1 500 Internal Server Error\r\n\r\n')

    connectionSocket.close()

