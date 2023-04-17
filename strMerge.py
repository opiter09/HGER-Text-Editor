import os
import sys
import re

pattern = re.compile("\\\\x..")
name = "strings_" + sys.argv[1][-5]
new = open("output_" + sys.argv[1][-5] + ".str", "wb")
new.close()
new = open("output_" + sys.argv[1][-5] + ".str", "ab")

new.write((0x0A29).to_bytes(4, "little"))
new.write(bytes(4))
offset = 0
for i in range(63):
    f = open(name + "/" + str(i).zfill(4) + ".txt", "rt")
    data = f.read()
    for val in re.findall(pattern, data):
        data = data.replace(val, chr(int(val[2:], 16)))
    f.close()
    size = len(data) + 1
    offset = offset + size
    new.write(offset.to_bytes(4, "little"))
new.write((0x01EB68).to_bytes(4, "little"))
new.write(bytes(4))
offset = 0
for i in range(2600):
    f = open(name + "/" + str(i).zfill(4) + ".txt", "rt")
    data = f.read()
    for val in re.findall(pattern, data):
        data = data.replace(val, chr(int(val[2:], 16)))
    f.close()
    size = len(data) + 1
    edit = []
    if (sys.argv[1][-5] == "E"):
        edit = [1720, 2283, 2285, 2286, 2288, 2290, 2291, 2293, 2325, 2326, 2330]
    elif (sys.argv[1][-5] == "F"):
        edit = [1557, 2283, 2285, 2286, 2288, 2290, 2291, 2293]
    elif (sys.argv[1][-5] == "I"):
        edit = [2283, 2284, 2285, 2286, 2288, 2290, 2291, 2292, 2293, 2558, 2566]
    elif (sys.argv[1][-5] == "S"):
        edit = [2283, 2285, 2286, 2288, 2290, 2291, 2293]
    if (i in edit):
        size = size - 1
    offset = offset + size
    new.write(offset.to_bytes(4, "little"))
for root, dirs, files in os.walk(name):
    for file in files:
        f = open(os.path.join(root, file), "rt")
        data = f.read()
        for val in re.findall(pattern, data):
            data = data.replace(val, chr(int(val[2:], 16)))
        f.close()
        if ((file == "1720.txt") and (sys.argv[1][-5] == "E")):
            for ch in data[0:-2]:
                new.write(ord(ch).to_bytes(1, "little"))
                new.write(bytes(1))
            new.write((0x2026).to_bytes(4, "little"))
        else:
            for i in range(len(data)):
                new.write(ord(data[i]).to_bytes(1, "little"))
                before = int.from_bytes(data[(i - 1):(i + 1)].encode("UTF-8"), "big")
                after = int.from_bytes(data[i:(i + 2)].encode("UTF-8"), "big")
                problems = [0x1320]
                if ((before not in problems) and (after not in problems)):
                    if ((i == (len(data) - 1)) or (ord(data[i + 1]) != 1)):
                        if (ord(data[i]) != 1):
                            new.write(bytes(1))
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

    