import socket

ip = "127.0.0.1"
port = 8910
msg = b"hello world"
print(f"Sending {msg} to {ip}:{port}")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


for i in range(4):
    sock.sendto(msg, (ip, port))
