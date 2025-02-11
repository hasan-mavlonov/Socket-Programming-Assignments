from socket import *
import sys
import os
from urllib.parse import urlparse

if len(sys.argv) != 2:
    print('Usage: python WebProxy.py <server_port>')
    sys.exit(1)

# Create a server socket, bind it to a port, and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerPort = int(sys.argv[1])

try:
    tcpSerSock.bind(("", tcpSerPort))
    tcpSerSock.listen(10)
    print(f"Proxy server running on port {tcpSerPort}...")
except Exception as e:
    print(f"Error binding socket: {e}")
    sys.exit(1)

while True:
    try:
        print("Ready to serve...")
        tcpCliSock, addr = tcpSerSock.accept()
        print("Received a connection from:", addr)

        message = tcpCliSock.recv(4096).decode()
        if not message:
            tcpCliSock.close()
            continue

        request_line = message.split("\n")[0]
        print("Request Line:", request_line)

        if len(request_line.split()) < 2:
            print("Invalid request")
            tcpCliSock.close()
            continue

        # Parse URL correctly
        parsed_url = urlparse(request_line.split()[1])
        host = parsed_url.hostname
        path = parsed_url.path if parsed_url.path else "/"

        if not host:
            print("Invalid request: No hostname found")
            tcpCliSock.close()
            continue

        print(f"Connecting to {host} on port 80")

        # Create cache directory
        cache_path = f"WEB/{host}{path}"
        cache_path = cache_path.rstrip("/")  # Remove trailing slash
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        # Serve from cache if available
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                cached_response = f.read()

            tcpCliSock.send(b"HTTP/1.1 200 OK\r\n")
            tcpCliSock.send(b"Content-Type: text/html\r\n\r\n")
            tcpCliSock.send(cached_response)
            print("Served from cache:", cache_path)
        else:
            try:
                # Connect to the remote server
                c = socket(AF_INET, SOCK_STREAM)
                c.connect((host, 80))

                request_headers = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
                c.send(request_headers.encode())

                response = b""
                while True:
                    data = c.recv(4096)
                    if not data:
                        break
                    response += data
                c.close()

                # Separate headers and body
                header_end = response.find(b"\r\n\r\n") + 4
                headers = response[:header_end]
                body = response[header_end:]

                # Cache the response body only
                with open(cache_path, "wb") as cache_file:
                    cache_file.write(body)

                # Send response to the client
                tcpCliSock.send(headers + body)

            except Exception as e:
                print(f"Error fetching {host}{path}: {e}")
                tcpCliSock.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")

        tcpCliSock.close()

    except KeyboardInterrupt:
        print("\nShutting down the proxy server.")
        tcpSerSock.close()
        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")
        tcpCliSock.close()
