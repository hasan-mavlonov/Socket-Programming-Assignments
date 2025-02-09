from socket import *
import os

serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Allow immediate reuse of the socket
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

print(f'The web server is up on port: {serverPort}')

while True:
    print('Waiting for a connection...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024)  # ✅ No UTF-8 decoding
        print("Received request (raw):", repr(message))

        if not message.strip():
            connectionSocket.close()
            continue

        request_parts = message.split(b' ')  # ✅ Use bytes instead of string operations
        if len(request_parts) < 2:
            print("Malformed request, closing connection.")
            connectionSocket.close()
            continue

        filename = request_parts[1].decode().lstrip("/")  # Decode only where needed

        if os.path.isfile(filename):
            with open(filename, 'rb') as f:  # ✅ Open file in binary mode
                output = f.read()

            response_headers = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: text/html; charset=utf-8\r\n"
                    b"Content-Length: " + str(len(output)).encode() + b"\r\n\r\n"
            )

            connectionSocket.sendall(response_headers + output)
        else:
            error_response = (
                b"HTTP/1.1 404 Not Found\r\n"
                b"Content-Type: text/html; charset=utf-8\r\n\r\n"
                b"<h1>404 Not Found</h1>"
            )
            connectionSocket.sendall(error_response)

    except Exception as e:
        print("Error:", e)
        connectionSocket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")

    connectionSocket.close()

