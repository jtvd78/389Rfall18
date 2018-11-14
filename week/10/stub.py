#!/usr/bin/env python2
# from the git repo
import md5py
import socket
import struct
import codecs
import binascii

message = 'CMSC389R Rocks!'    # original message here
malicious = ''  # put your malicious message here

#####################################
### STEP 1: Calculate forged hash ###
#####################################

line_ctr = 1
def readline(f):
    global line_ctr
    s = f.readline().replace('\n','')
    print("%d\t %s" % (line_ctr, s))
    line_ctr = line_ctr + 1
    return s

def readlines(f, num):
    for _ in range(0, num):
        readline(f)

# Connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("142.93.118.186", 1234))
f = s.makefile()

# Select 'Sign some Data'
readlines(f, 6)
s.send("1\n")

# Send data
readlines(f, 8)
s.send(message+"\n")

# Read generated hash
readlines(f, 2)
legit = readline(f).split(':')[1][1:]   # a legit hash of secret + message goes here, obtained from signing a message
print('Hash is "%s"' % legit)

# initialize hash object with state of a vulnerable hash
fake_md5 = md5py.new('A' * 64)
fake_md5.A, fake_md5.B, fake_md5.C, fake_md5.D = md5py._bytelist2long(legit.decode('hex'))

# update legit hash with malicious message
#fake_md5.update(malicious)

# fake_hash is the hash for md5(secret + message + padding + malicious)
fake_hash = fake_md5.hexdigest()
print('Fake hash is "%s"' % fake_hash)

#############################
### STEP 2: Craft payload ###
#############################

# Converts a 4 bit number to a hex string
def hex4(num):
    if num == 10:
        return 'a'
    if num == 11:
        return 'b'
    if num == 12:
        return 'c'
    if num == 13:
        return 'd'
    if num == 14:
        return 'e'
    if num == 15:
        return 'f'
    return str(num)

import sys

# Encode a message with \x
def msg_encode(msg):
    out = ''
    for i in msg:     

        if ord(i) != 0 and ord(i) < 127 and ord(i) > 31:
            out += i
        else:
            (val,) = struct.unpack('B', i)
            out += '\\x'
            out += hex4(val >> 4)
            out += hex4(val & 0xF)

    return out

# Try difference secret sizes. 
for secret_bytes in range(8, 15+1):
   
    # TODO: calculate proper padding based on secret + message
    # secret is <redacted> bytes long (48 bits)
    # each block in MD5 is 512 bits long
    # secret + message is followed by bit 1 then bit 0's (i.e. \x80\x00\x00...)
    # after the 0's is a bye with message length in bits, little endian style
    # (i.e. 20 char msg = 160 bits = 0xa0 = '\xa0\x00\x00\x00\x00\x00\x00\x00\x00')
    # craft padding to align the block as MD5 would do it
    # (i.e. len(secret + message + padding) = 64 bytes = 512 bits

    # Select 'Test a signature's validity'
    readlines(f, 6)
    s.send("2\n")

    # Send fake hash
    readlines(f, 3)
    s.send('%s\n' % fake_hash)   

    # Calculate padding
    # Block Size - (Secret Size) - len(0x80) - len(message) - (8 bytes for message length)
    zero_bytes = 64 - secret_bytes - 1 - len(message) - 8
    padding = '\x80' + '\x00' * zero_bytes + struct.pack('<q', len(message)*8)

    # payload is the message that corresponds to the hash in `fake_hash`
    # server will calculate md5(secret + payload)
    #                     = md5(secret + message + padding + malicious)
    #                     = fake_hash
    payload = message + padding + malicious

    # A bunch of prints I'm using to debug
    # print("MESSAGE LEN")
    # print(len(message))
    # print(len(message) * 8)
    # print( struct.pack('<q', len(message)*8))
    # print(len(struct.pack('<q', len(message)*8)))
    # print(len(message + padding + malicious))
    # print(len(payload))
    # print(payload)
    # print(binascii.hexlify(payload))

    msg = msg_encode(payload)

    # print(msg)
    # print(binascii.hexlify(msg + "\n"))
    # print(len(msg)/4)

    # Sent payload. Wait for user to try next secret size. 
    sent = s.send(msg + "\n")
    # sent = s.send(payload + "\n")
    #  print sent
    readlines(f, 10)
    raw_input()