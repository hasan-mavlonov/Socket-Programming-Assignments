from socket import *
import ssl
import base64

bufferSize = 2048


def create_auth_message(user: str, password: str):
    str = "\x00" + user + "\x00" + password
    base64_str = base64.b64encode(str.encode())
    return "AUTH PLAIN " + base64_str.decode()


sock = socket(AF_INET, SOCK_STREAM)
sock.settimeout(5)
ssl_socket = ssl.wrap_socket(sock)
ssl_socket.connect(('smtp.gmail.com', 465))


def recv_msg():
    try:
        return ssl_socket.recv(bufferSize).decode()
    except timeout:
        pass


def seng_msg(message, expect_return_msg=True):
    ssl_socket.send(f"{message}\r\n".encode())
    if expect_return_msg:
        recv = recv_msg()
        print(recv)
        return recv


def ehlo():
    return send_msg("ehlo Maheen")


def login(user, password):
    auth_msg = create_auth_message(user, password)
    send_msg(auth_msg)


def quit():
    return send_msg("QUIT")
