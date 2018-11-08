#!/usr/bin/python2

import hashlib
import string

hashes = []

def bruteforce(password):
    for salt in string.ascii_lowercase:
        result = hashlib.sha512(salt+password).hexdigest()
        if result in hashes:
            print("Password: %s, Salt %s" % (password, salt))

with open("hashes") as fp:
    line = fp.readline()
    while line:
        hashes.append(line.replace('\n',''))
        line = fp.readline()

with open("pwd.txt") as fp:
    line = fp.readline()
    while line:
        bruteforce(line.replace('\n', ''))
        line = fp.readline()
