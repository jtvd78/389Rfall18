#!/usr/bin/env python2

import sys
import struct
from datetime import datetime


class Data:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def read_uword(self):
        (uword,) = struct.unpack("<L", self.data[self.offset:self.offset+4])
        self.offset += 4
        return uword

    def read_udword(self):
        (udword,) = struct.unpack("<Q", self.data[self.offset:self.offset+8])
        self.offset += 8
        return udword

    def read_ascii(self, length):
        dat = self.data[self.offset:(self.offset + length)]
        self.offset += length
        return ''.join(i for i in dat)

    def read_utf8(self, length):
        out = ''.join(self.data[self.offset:self.offset+length]).decode("utf8")
        self.offset += length
        return out
   
    def read_flt(self):
        (flt,) = struct.unpack("<d", self.data[self.offset:self.offset+8])
        self.offset += 8
        return flt

    def read_dbl_array(self, length):
        if length % 8 != 0:
            bork("Bad length for read_dbl_array")
        words = length / 8
        for i in range(0, words):
            out.append(self.read_flt())
        return out

    def read_word_array(self, length):
        if length % 4 != 0:
            bork("Bad length for read_word_array")
        words = length / 4
        out = []
        for i in range(0, words):
            out.append(self.read_uword())
        return out

    def read_udword_arr(self, length):
        if length % 8 != 0:
            bork("Bad length for read_udword_arr")
        words = length / 8
        out = []
        for i in range(0, words):
            out.append(self.read_udword())
        return out

    def read_lat_lng(self, length):
        if length != 16:
            bork("Bad length for read_flt_array")
        return (self.read_flt(), self.read_flt())

    def read_png(self, length, filename):
        with open(filename, 'wb') as fp:
            arr = [chr(i) for i in [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]]
            for ch in arr:
                fp.write(ch)
            fp.write(self.data[self.offset : (self.offset + length)])
        self.offset += length

# You can use this method to exit on failure conditions.
def bork(msg):
    sys.exit(msg)

# Some constants. You shouldn't need to change these.
MAGIC = 0xdeadbeef
VERSION = 1

if len(sys.argv) < 2:
    sys.exit("Usage: python2 stub.py input_file.fpff")

# Normally we'd parse a stream to save memory, but the FPFF files in this
# assignment are relatively small.
with open(sys.argv[1], 'rb') as fpff:
    data = fpff.read()

dat = Data(data)

magic = dat.read_uword()
version = dat.read_uword()
timestamp = dat.read_uword()
author = dat.read_ascii(8)
sections = dat.read_uword()

if magic != MAGIC:
    bork("Bad magic! Got %s, expected %s" % (hex(magic), hex(MAGIC)))

if version != VERSION:
    bork("Bad version! Got %d, expected %d" % (int(version), int(VERSION)))

print("------- HEADER -------")
print("MAGIC: %s" % hex(magic))
print("VERSION: %d" % int(version))
print("TIMESTAMP: %s" % datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
print("AUTHOR: %s" % author)
print("SECTION COUNT: %d" % sections)

print("-------  BODY  -------")

def section_type(i):
    return ["PNG", "DWORD ARRAY", "UTF-8", "DOUBLE ARRAY", 
    "WORD ARRAY", "LAT-LNG", "REFERENCE", "", "ASCII"][i - 1]

for i in range(0, 100):

    if dat.offset == len(data):
        print("DONE WITH FILE")
        break

    stype = dat.read_uword()
    slen = dat.read_uword()

    if stype < 0 or stype > 9 or stype == 8:
        bork("Unsupported section type. Found: %d" % stype)

    print "SECTION %d, TYPE: %s, LENGTH: %d"  % (i , section_type(stype), slen)
    
    if stype == 1:
        dat.read_png(slen, "extracted%d.png" % i)
    elif stype == 2:
        print(dat.read_udword_arr(slen))
    elif stype == 3:
        print(dat.read_utf8(slen))
    elif stype == 4:
        print(dat.read_dbl_array(slen))
    elif stype == 5:
        # Word Array
        print(dat.read_word_array(slen))
    elif stype == 6:
        # Coordinate
        print(dat.read_lat_lng(slen))
    elif stype == 7:
        # Section Reference
        if slen != 4:
            bork("slen != 4 for section reference")
        sect = dat.read_uword()
        if sect >=0 and sect < sections:
            print("Section Number: %d" % sect)
        else:
            bork("invalid section number")
    elif stype == 9:
        # ASCII
        print(dat.read_ascii(slen))