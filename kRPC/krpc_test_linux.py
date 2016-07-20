import socket
rpc_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rpc_conn.connect(('192.168.0.2', 50000))
# Send the 12 byte hello message
rpc_conn.sendall(b'\x48\x45\x4C\x4C\x4F\x2D\x52\x50\x43\x00\x00\x00')
# Send the 32 byte client name 'Jeb' padded with zeroes
name = 'Jeb'.encode('utf-8')
name += (b'\x00' * (32-len(name)))
rpc_conn.sendall(name)
# Receive the 16 byte client identifier
identifier = b''
while len(identifier) < 16:
    identifier += rpc_conn.recv(16 - len(identifier))
# Connection successful. Print out a message along with the client identifier.
import binascii
printable_identifier = binascii.hexlify(bytearray(identifier))
print('Connected to RPC server, client idenfitier = %s' % printable_identifier)


stream_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream_conn.connect(('192.168.0.2', 50001))
# Send the 12 byte hello message
stream_conn.sendall(b'\x48\x45\x4C\x4C\x4F\x2D\x53\x54\x52\x45\x41\x4D')
# Send the 16 byte client identifier
stream_conn.sendall(identifier)
# Receive the 2 byte OK message
ok_message = b''
while len(ok_message) < 2:
    ok_message += stream_conn.recv(2 - len(ok_message))
# Connection successful
print('Connected to stream server')
