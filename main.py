import socket
sock = socket.socket()
sock.connect(('172.24.1.1', 1080))
sock.send(b'11/1500/90')
sock.close()
