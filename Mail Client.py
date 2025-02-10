from socket import *
import ssl
import base64

bufferSize = 2048


def create_auth_message(user: str, password: str):
    auth_str = f"\x00{user}\x00{password}"
    base64_str = base64.b64encode(auth_str.encode()).decode()
    return f"AUTH PLAIN {base64_str}"


sock = socket(AF_INET, SOCK_STREAM)
sock.settimeout(5)
ssl_socket = ssl.create_default_context().wrap_socket(sock, server_hostname='smtp.gmail.com')
ssl_socket.connect(('smtp.gmail.com', 465))


def recv_msg():
    try:
        return ssl_socket.recv(bufferSize).decode()
    except timeout:
        return None


def send_msg(message, expect_return_msg=True):
    ssl_socket.send(f"{message}\r\n".encode())
    if expect_return_msg:
        recv = recv_msg()
        print(recv)
        return recv


def ehlo():
    return send_msg("EHLO Maheen")


def login(user, password):
    auth_msg = create_auth_message(user, password)
    send_msg(auth_msg)


def quit():
    return send_msg("QUIT")


def send_mail(msg, from_addr, to_addr):
    send_msg(f"MAIL FROM: <{from_addr}>")
    send_msg(f"RCPT TO: <{to_addr}>")
    send_msg("DATA")

    # Properly formatted email headers
    email_headers = f"""\
From: {from_addr}
To: {to_addr}
Subject: Hi! Hasan here

{msg}
""".replace("\n", "\r\n")  # Ensure CRLF line endings

    send_msg(email_headers, expect_return_msg=False)

    # End the DATA section properly
    send_msg(".", expect_return_msg=True)


ehlo()
login("hasanmavlonov79@gmail.com", "habr vyvv hjsx yiom")  # Use an app password
send_mail("I am Hasan", "hasanmavlonov79@gmail.com", "h.mavlonov@newuu.uz")
quit()
