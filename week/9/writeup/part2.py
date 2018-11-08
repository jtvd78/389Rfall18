#!/usr/bin/python3

import socket
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("142.93.117.193", 7331))
f = s.makefile()

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

    spl2 = line.split('Find me the ')[1].split(' hash of ')
    data = spl2[1].replace('\n', '')
    alg = spl2[0]

    h = hashlib.new(alg)
    h.update(bytes(data, 'UTF-8'))
    s.send(bytes(h.hexdigest() + '\n', 'UTF-8'))
    
    print(h.hexdigest())
    print(f.readline())
    