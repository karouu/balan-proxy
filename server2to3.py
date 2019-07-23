#!/usr/bin/env python
# converted from 2to3, python3 now

PORT = 8499
KEY = "foobar!"

import sys
import socket
import select
import socketserver
import struct
import string
import hashlib

def get_table(key):
    m = hashlib.md5()
    m.update(key)
    s = m.digest()
    (a, b) = struct.unpack('<QQ', s)
    table = [c for c in string.maketrans('', '')]
    for i in range(1, 1024):
        table.sort(lambda x, y: int(a % (ord(x) + i) - a % (ord(y) + i)))
    return table


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Socks5Server(socketserver.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if sock in r:
                    if remote.send(self.decrypt(sock.recv(4096))) <= 0:
                        break
                if remote in r:
                    if sock.send(self.encrypt(remote.recv(4096))) <= 0:
                        break
        finally:
            remote.close()

    def encrypt(self, data):
        return data.translate(encrypt_table)

    def decrypt(self, data):
        return data.translate(decrypt_table)

    def send_encrpyt(self, sock, data):
        sock.send(self.encrypt(data))

    def handle(self):
        try:
            print('socks connection from ', self.client_address)
            sock = self.connection
            sock.recv(262)
            self.send_encrpyt(sock, "\x05\x00")
            data = self.decrypt(self.rfile.read(4))
            mode = ord(data[1])
            addrtype = ord(data[3])
            if addrtype == 1:
                addr = socket.inet_ntoa(self.decrypt(self.rfile.read(4)))
            elif addrtype == 3:
                addr = self.decrypt(
                    self.rfile.read(ord(self.decrypt(sock.recv(1)))))
            else:
                # not support
                return
            port = struct.unpack('>H', self.decrypt(self.rfile.read(2)))
            reply = "\x05\x00\x00\x01"
            try:
                if mode == 1:
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote.connect((addr, port[0]))
                    local = remote.getsockname()
                    reply += socket.inet_aton(local[0]) + struct.pack(">H",
                        local[1])
                    print('Tcp connect to', addr, port[0])
                else:
                    reply = "\x05\x07\x00\x01" # Command not supported
                    print('command not supported')
            except socket.error:
                # Connection refused
                reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
            self.send_encrpyt(sock, reply)
            if reply[1] == '\x00':
                if mode == 1:
                    self.handle_tcp(sock, remote)
        except socket.error:
            print('socket error')


def main(host=''):
    server = ThreadingTCPServer((host, PORT), Socks5Server)
    server.allow_reuse_address = True
    print("starting server at port %d ..." % PORT)
    server.serve_forever()

if __name__ == '__main__':
    encrypt_table = ''.join(get_table(KEY))
    decrypt_table = string.maketrans(encrypt_table, string.maketrans('', ''))
    arg = sys.argv
    if len(arg) == 1:
        host = ''
        print("Use default host")
    else:
        host = arg[1]
        print("Use host %s" % host)
    main(host)
