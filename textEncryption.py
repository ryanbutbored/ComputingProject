from string import ascii_uppercase as up
from random import randint, choice

full = ".,?! " +up +"0123456789"
words = []
#text file words_alpha.txt sourced from https://github.com/dwyl/english-words
f = open("words_alpha.txt", "r")
lines = f.readlines()
f.close()
for line in lines:
    words.append(line.strip())
        
def caesarShift(key, msg, mode):
    new = full[key:] + full[:key]
    msg = msg.upper()
    newmsg = ""
    if mode == "encode":
        primary = full
        secondary = new
    else:
        primary = new
        secondary = full
    for c in msg:
        if c in primary:
            newmsg += secondary[primary.index(c)]
    return newmsg

def getRandomCeasarKey():
    return randint(1, 40)

def substitutionCipher(key, msg, mode):
    newmsg = ""
    msg = msg.upper()
    key = key.upper()
    if mode == "encode":
        primary = full
        secondary = key
    else:
        primary = key
        secondary = full
    for c in msg:
        if c in primary:
            newmsg += secondary[primary.index(c)]
    return newmsg

def getRandomSubKey():
    tmp = list(full)
    key = ""
    for i in range(len(tmp)):
        c = choice(tmp)
        key += c
        tmp.remove(c)
    return key
#modified version to allow for encryption of numbers and common punctuation
#as such these characters are allowed to be in the key, however they will not be randomly generated
def vigenereCipher(key, msg, mode):
    msg = msg.upper()
    key = key.upper()
    newmsg = ""
    if mode == "encode":
        j = 0
        for c in msg:
            if j > len(key)-1:
                j = 0
            newmsg += caesarShift(full.index(key[j]), c, "encode")
            j += 1
    else:
        j = 0
        for c in msg.strip():
            if j == len(key):
                j = 0
            row = full[full.index(key[j]):] + full[:full.index(key[j])]
            newmsg += full[row.index(c)]
            j += 1
        
    return newmsg

def getRandomVigKey():
    return choice(words).upper()

def railFenceCipher(key, msg, mode):
    if mode == "encode":
        rails = []
        for i in range(key):
            rails.append([])
        i = 0
        mode = "sub"
        for c in msg:
            if i == key-1 or i == 0:
                if mode == "add":
                    mode = "sub"
                else:
                    mode = "add"
            for j in range(key):
                if i == j:
                    rails[j].append(c)
                else:
                    rails[j].append("@")
            if mode == "add":
                i += 1
            else:
                i -= 1
        newmsg = ""
        for line in rails:
            for c in line:
                if c != "@":
                    newmsg += c
    else:
        msg = list(msg)
        l = len(msg)
        r = []
        for i in range(key):
            r.append([])
            for j in range(l):
                r[i].append("@")
        for i in range(key):
            x=0
            y=0
            f = "a"
            for j in range(l):
                if y == i:
                    r[y][x] = msg.pop(0)
                x += 1
                if f == "a":
                    y += 1
                else:
                    y -= 1
                if y == 0:
                    f = "a"
                elif y == key-1:
                    f = "m"
        newmsg = ""
        x=0
        y=0
        f = "a"
        for i in range(l):
            newmsg += r[y][x]
            x += 1
            if f == "a":
                y += 1
            else:
                y -= 1
            if y == 0:
                f = "a"
            elif y == key-1:
                f = "m"
    return newmsg

def getRandomRailKey():
    return randint(2,50)