import os
import sys

name = "strings_" + sys.argv[1][-5]
new = open("output_" + sys.argv[1][-5] + ".str", "wb")
new.close()
new = open("output_" + sys.argv[1][-5] + ".str", "ab")

new.write((0x0A29).to_bytes(4, "little"))
new.write(bytes(4))
offset = 0
for i in range(63):
    f = open(name + "/" + str(i).zfill(4) + ".txt", "rb")
    data = f.read()
    f.close()
    size = (len(data) + 2) // 2
    offset = offset + size
    new.write(offset.to_bytes(4, "little"))
new.write((0x01EB68).to_bytes(4, "little"))
new.write(bytes(4))
offset = 0
for i in range(2600):
    f = open(name + "/" + str(i).zfill(4) + ".txt", "rb")
    data = f.read()
    f.close()
    size = (len(data) + 2) // 2
    offset = offset + size
    new.write(offset.to_bytes(4, "little"))
for root, dirs, files in os.walk(name):
    for file in files:
        f = open(os.path.join(root, file), "rb")
        data = f.read()
        f.close()
        new.write(data)
        new.write(bytes(2))
new.write(("x\0x\0x\0x\0x\0x\0\0\0").encode("UTF-8"))
new.close()

dataSize = os.stat("output_" + sys.argv[1][-5] + ".str").st_size - 0x29AC
oldD = open("output_" + sys.argv[1][-5] + ".str", "rb")
oldR = oldD.read()
oldD.close()
newD = open("output_" + sys.argv[1][-5] + ".str", "wb")
newD.close()
newD = open("output_" + sys.argv[1][-5] + ".str", "ab")
newD.write(oldR[0:0x104])
newD.write(dataSize.to_bytes(4, "little"))
newD.write(oldR[0x108:])
newD.close()

    