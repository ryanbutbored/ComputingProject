from textEncryption import full
from random import choice

full = list(full)

length = 10

f = open("encryptionTestCases" +str(length)+".txt", "w")
for i in range(length):
    new = ""
    for i in range(1504):
        c = choice(full)
        if i == 1503:
            while c == " ":
                c = choice(new)
        new += c
    f.write(new + "\n")
f.close()
