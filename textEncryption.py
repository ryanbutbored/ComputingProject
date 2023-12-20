from string import ascii_uppercase as up, ascii_lowercase as low
from random import randint, choice

full = '.,?!" ' +low +up +"0123456789"

#----------------------------Caesar Shift----------------------------

def caesarShift(key, msg, mode):
    new = full[key:] + full[:key]
    msg = msg
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
    return randint(1, len(full))

#----------------------------Substitution Cipher----------------------------

def substitutionCipher(key, msg, mode):
    newmsg = ""
    msg = msg
    key = key
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

#----------------------------Vignere Cipher----------------------------

words = []
#text file words_alpha.txt sourced from https://github.com/dwyl/english-words
f = open("words_alpha.txt", "r")
lines = f.readlines()
f.close()
for line in lines:
    words.append(line.strip())

#modified version to allow for encryption of numbers and common punctuation
#as such these characters are allowed to be in the key, however they will not be randomly generated
def vigenereCipher(key, msg, mode):
    msg = msg
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

#----------------------------Rail-Fence Cipher----------------------------

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

#----------------------------Enigma----------------------------

rotors = ['', ['EzavLkPynhG5I.mTS?i0NfBDRW2"6X7xMuZ 9Uw1QOogbAqptJ3K,sC!ejYdr48HVcFl', ['Q']], 
              ['W3qRPV67?nuC9KBNcgaMGJoYjidAeOs,rS!40xvzHhy5f.k"UIXl8DmLE2 ZFTpQwbt1', ['E']], 
              ['phDs3Fw!f.UZG"iM76Pxeb1otKdOyIaErR4Agk?XT5NBn8zVlJquQmLC cjSv29WY,H0', ['V']], 
              ['O,hYwSVqlzHQgrCEoIxZsT85a?iJ1f6UcjPMRBKtbAGpL0.v FDWkduN9n24em"X!73y', ['J']], 
              ['vMlQP9ApdiZWjDwOthC0"STe2FmBs!UHN6x.guor8cYnqyGL1zaK?VI4fb X3Ek,5RJ7', ['Z']], 
              ['WlV2jsxbmL1oGS467a.!9 UZpeBw3q,y"vCNniQkrFcDu0PhOTIAz8fYtJ?EKR5MXdgH', ['Z', 'M']], 
              ['u9DjR6KAH1EQVW7.CiTlXNP"cwx!dn0e,oYB3GUhFtbkOzZmSr?pg 2sq8ya5fIJMLv4', ['Z', 'M']], 
              ['Aha8cjSLT BxN4uvR0gKOIVtP,lHE7Dsi"bq2?M6ydUfw!CZXnFm.3JrepW1oQ5z9kGY', ['Z', 'M']]]

class Rotor:
    def __init__(self, r):
        self.cipher = r[0]
        self.ring = full
        self.notches = r[1]
        self.rotated = False

reflector = Rotor(['KC0SW3JEZ4MFP19IO8Y76X5UDTN2LRQVGH,sbfABja.weukgyx!trz"pmc?hv dqonli', []])
                  #'.,?!" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def Enigma(key, msg):
    settings = stripEnigmaKey(key)
    newmsg = ""
    for l in msg:
        settings[0] = rotateRotors(settings[0])
        l = plugboard(settings[1], l)
        for i in range(4, -1, -1):
            l = getLetter(l, settings[0][i])
        l = getLetterInverse(l, reflector)
        for i in range(5):
            l = getLetterInverse(l, settings[0][i])
        newmsg += plugboard(settings[1], l)
    return newmsg

def getLetterInverse(l,r):
    return r.cipher[r.ring.index(l)]

def getLetter(l,r):
    return r.ring[r.cipher.index(l)]

def plugboard(ps, l):
    for i in range(len(ps)):
        for j in range(2):
            if ps[i][j] == l:
                if j == 0:
                    return ps[i][1]
                else:
                    return ps[i][0]
    return l

def rotateRotor(rotor):
    return rotor[1:]+rotor[0]

def rotateRotors(r):
    for i in range(4, -1, -1):
        if i != 4:
            if r[i].cipher[0] in r[i].notches and not r[i].rotated and not r[i+1].rotated:
                r[i].cipher = rotateRotor(r[i].cipher)
                r[i].rotated = True
                r[i+1].cipher = rotateRotor(r[i+1].cipher)
                r[i+1].rotated = True
            elif r[i].cipher[0] in r[i].notches and not r[i].rotated:
                r[i].cipher = rotateRotor(r[i].cipher)
                r[i].rotated = True
            elif i == 0:
                r[i].cipher = rotateRotor(r[i].cipher)
                r[i].rotated = True
    for i in range(5):
        r[i].rotated = False
    return r

def stripEnigmaKey(key):
    settings = key.split("/")
    positions = settings[0].split("-")
    alignments = settings[1].split("-")
    ringset = settings[2].split("-")
    plugsets = settings[3].split("-")
    r = []
    ps = []
    for position in positions:
        r.append(Rotor(rotors[int(position)]))
    for i in range(5):
        while r[i].cipher[0] != alignments[i]:
            r[i].cipher = rotateRotor(r[i].cipher)
        while r[i].ring[0] != ringset[i]:
            r[i].ring = rotateRotor(r[i].ring)
    for plugset in plugsets:
        ps.append(plugset.split("<>"))
    return [r, ps]

def getRandomEnigmaKey():
    key = ""
    allowed = list(range(1,9))
    for i in range(5):
        c = choice(allowed)
        key += str(c)
        allowed.remove(c)
        if i != 4:
            key += "-"
    key += "/"
    for i in range(2):
        for j in range(5):
            key += choice(full)
            if j != 4:
                key += "-"
        key += "/"
    l = list(full)
    for i in range(10):
        c = choice(l)
        l.remove(c)
        key += c + "<>"
        c = choice(l)
        l.remove(c)
        key += c
        if i != 9:
            key += "-"
    return key


tmp = list(full[0:34])
key = ""
for i in range(len(tmp)):
    c = choice(tmp)
    key += c
    tmp.remove(c)

