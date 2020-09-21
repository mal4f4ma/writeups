#!/usr/bin/python3
#Author: n0tM4l4f4m4
#Title: solver.py

from z3 import *

serial = [BitVec('val_%i'%i,32) for i in range(0,18)]

s = Solver()

s.add(serial[5] == 45)
s.add(serial[11] == 45)
s.add(serial[8] == 95)

s.add(serial[1] > 47, serial[1] <= 57)
s.add(serial[2] > 47, serial[2] <= 57)
s.add(serial[4] > 47, serial[4] <= 57)
s.add(serial[7] > 47, serial[7] <= 57)
s.add(serial[9] > 47, serial[9] <= 57)
s.add(serial[13] > 47, serial[13] <= 57)
s.add(serial[16] > 47, serial[16] <= 57)

s.add(serial[3] > 96, serial[3] <= 122)
s.add(serial[10] > 96, serial[10] <= 122)
s.add(serial[12] > 96, serial[12] <= 122)
s.add(serial[15] > 96, serial[15] <= 122)

s.add(serial[0] > 64, serial[0] <= 90)
s.add(serial[6] > 64, serial[6] <= 90)
s.add(serial[14] > 64, serial[14] <= 90)
s.add(serial[17] > 64, serial[17] <= 90)

#function V
s.add(serial[2] * serial[3] % serial[4] == 44)
s.add(serial[3] + serial[2] + serial[1] + serial[0] - serial[4] == 243)
s.add(serial[0] * serial[1] % serial[2] + serial[3] * serial[4] == 5986)

#function VV
s.add((serial[6] + serial[7]) * (serial[10] - serial[9]) == 9306)
s.add((serial[6] + serial[10]) * (serial[7] + serial[9]) == 20500)

#function VVV
s.add(serial[15] + serial[13] + serial[12] - serial[14] - serial[16] + serial[17] == 218)
s.add(serial[14] + serial[12] - serial[13] - serial[15] + serial[16] * serial[17] == 4199)
s.add(serial[15] * serial[16] % serial[17] == 12)
s.add(serial[12] * serial[13] % serial[14] == 75)

if s.check() == sat:
    m = s.model()
    flag = ''
    for val in range(18):
        num = m[serial[val]].as_long()
        flag += chr(num)
        pass
    print("hackdef{" + flag + "}")
    pass
else:
    print('sorry =(')
    pass