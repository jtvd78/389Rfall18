#!/usr/bin/env python
#-*- coding:utf-8 -*-

# importing useful libraries -- feel free to add any others you find necessary

import socket
import hashlib




def recvall(socket):
    s = ""
    response = ""
    while(True):
        print("recv")
        s = socket.recv(1024)
        print(len(s))
        if len(s) == 0:
            break
        response = response + s.decode("utf-8") 

      #  print(response)
    return response

host = "142.93.117.193"   # IP address or URL
port =   7331   # port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

f = s.makefile()

# First Question
f.readline()
f.readline()
f.readline()

while True:

    line = f.readline()
    while 'Find me' not in line:
        print(line)
        line = f.readline()
        if line == '':
            exit(0)

    print(line)
    spl1 = line.split('Find me the ')
    spl2 = spl1[1].split(' hash of ')

    data = spl2[1].replace('\n', '')

    print('%s %s' % (spl2[0], data))

    h = hashlib.new(spl2[0])
    h.update(bytes(data, 'UTF-8'))

    print(h.hexdigest())

    s.send(bytes(h.hexdigest(), 'UTF-8'))
    s.send(bytes("\n", 'UTF-8'))

    print(f.readline())