import os
import sys

start = 0x29AC
name = "strings_" + sys.argv[1][-5]

try:
    os.mkdir(name)
except:
    pass
    
reading = open(sys.argv[1], "rb").read()
old = 0
new = 0
for i in range(0x10C, start, 4):
    old = new
    new = int.from_bytes(reading[i:(i + 4)], "little") * 2
    data = reading[(start + old):(start + new)]
    file = open(name + "/" + str((i // 4) - 67).zfill(4) + ".txt", "wb")
    file.write(data[0:-2])
    file.close()