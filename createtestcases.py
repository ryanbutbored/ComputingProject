from textEncryption import full
from random import choice

full = list(full)

length = 10

f = open("encryptionTestCases" +str(length)+".txt", "w")
for i in range(length):
    new = ""
    for i in range(1500):
        c = choice(full)
        if i == 1499:
            while c == " ":
                c = choice(new)
        new += c
    f.write(new + "\n")
f.close()
