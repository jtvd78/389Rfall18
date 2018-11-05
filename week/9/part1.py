#!/usr/bin/env python
#-*- coding:utf-8 -*-

# importing a useful library -- feel free to add any others you find necessary
import hashlib
import string
import binascii

hashes = []
salts = string.ascii_lowercase


with open("hashes") as fp:
    line = fp.readline()
    while line:
        hashes.append(line.replace('\n',''))
        line = fp.readline()

def hash(password, salt):
    input = salt + password
  #  print(input)
    binary = bin(int(binascii.hexlify(input),16))
    return hashlib.sha512(binary).hexdigest()


def bruteforce(password):
    
    for salt in salts:
        result = hash(password, salt)
   #     print(result)
        if result in hashes:
            print("Found password!")


with open("pwd.txt") as fp:
    line = fp.readline()
    while line:
        bruteforce(line.replace('\n', ''))
        line = fp.readline()

