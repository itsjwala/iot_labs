import socket 
from hashlib import sha1
from base64 import b64encode
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8794
try:
    s.bind(('localhost', port))
except socket.error as e:
    print(str(e))

s.listen(5)

#https://developer.mozilla.org/en-US/docs/Web/HTTP/Protocol_upgrade_mechanism
def upgrade_ws_request(con):
	msg = con.recv(1024)
	for i in msg.decode('utf-8').split('\r\n'):
		# print(i)
		try:
			value = i.split("Sec-WebSocket-Key: ")[1]
			value+="258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
			sha = sha1(value.encode()).digest()
			hash = b64encode(sha)
			resp="HTTP/1.1 101 Switching Protocols\r\n" + \
             "Upgrade: websocket\r\n" + \
             "Connection: Upgrade\r\n" + \
             "Sec-WebSocket-Accept: %s\r\n\r\n"%(hash.decode())
			con.send(resp.encode())
			break
		except:
			pass

def send_data(con, payload):

    # setting fin to 1 and opcpde to 0x1
    frame = [129]
    # adding len. no masking hence not doing +128
    frame += [len(payload)]
    # adding payload
    frame_to_send = bytearray(frame) + payload.encode()

    con.send(frame_to_send)


while True:
	con, addr = s.accept()
	print(addr)
	
	upgrade_ws_request(con)
	for i in range(100):
		send_data(con,str(i%2))
		time.sleep(0.1)
	con.close()