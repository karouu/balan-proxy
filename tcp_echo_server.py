# tcp_echo_server.py
import sys,socket

host = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind( (host,port) )
sock.listen(1)

while True:
	connection, client_address = sock.accept()

	try:
		print >>sys.stderr, 'connection from', client_address

		while True:
			data = connection.recv(20)
			print >>sys.stderr, 'received "%s"' % data
			if data:
				print >>sys.stderr, 'sending data back to the client'
				connection.sendall(data)
			else:
				print >>sys.stderr, 'no more data from', client_address
				break

	finally:
		connection.close()
