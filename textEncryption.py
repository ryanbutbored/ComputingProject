from string import ascii_uppercase as up, ascii_lowercase as low
from random import randint, choice
from datetime import datetime

full = ". " +low +up +"0123456789"

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

rotors = ["", ["qHXpMIAV8ucEywgRr9GDvY4ZFf1B CPmWOl.05T6teJKona7Lbdk3NUjQhSzsix2", ["Q"]], 
              ["n 1h8H25XwYqFLaR6cPogpDt.Im9Kre43Gb0Z7lOTCBJQzWsAduyxNMSfkVvUjEi", ["E"]], 
              ["2zwCG6lOpZrf. q7uaNT0vVWJscKMjFHtn9gdeyDoPSmEX5kAYQ84xI1hiBU3RbL", ["V"]], 
              ["WicLrSx8nFeqM2XZfJYOlQGdH BgzE3sC9p1mTP5oj6ubNyR4wKkU7at0IvV.ADh", ["J"]], 
              ["ZW3AqzG08fbuiERHav9KTlVpmcXC2rFdDxjLwtk s.PNJo17neQBO6IUh4gMYyS5", ["Z"]], 
              ["D51a0dQtSg8RNxVfqyzWbhnHc3pI7JZiTOCBu2G4slEPLFMYo Xk.rwm9A6jeUKv", ["Z", "M"]], 
              ["5CH6PmYfBGI TnpMqAos2VhvEyr8UtO74WFizX01KuNDl3xcadZbgQ9Je.SkwLjR", ["Z", "M"]], 
              ["Iy58sLlCPvXR6ozbhjUgO.SKxrFdqHnaBQ30ETY2 V7uGZANf9tiewpWJD1ck4mM", ["Z", "M"]]]

class Rotor:
    def __init__(self, r):
        self.cipher = r[0]
        self.ring = full
        self.notches = r[1]
        self.rotated = False

reflector = Rotor(["I4X5U9YVK7ZMW26O3TFGSQ0HR8ENLJ1Pyqrv.BgAjznDtwspcfkaeiuClo bmhxd", []])
                  #".,?!" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

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

#----------------------RSA-----------------------

def gcd(a,b):
    if a < b:
        s = a
        l = b
    else:
        l = a
        s = b
    r = l % s
    while r != 0:
        l = s
        s = r
        r = l % s
    return s

def millerRabin(n):
    if n % 2 == 0:
        return False
    elif n % 3 == 0:
        return False
    elif n % 5 == 0:
        return False
    else:
        k = 128
        s = 0
        d = n - 1
        while d % 2 == 0:
            s += 1
            d = d // 2
        for i in range(k):
            a = randint(2,n-2)
            x = pow(a,d,n)
            for j in range(s):
                y = pow(x,2,n)
                if y == 1 and x != 1 and x != n-1:
                    return False
                x = y
            if y != 1:
                return False
        return True

def EEA(a, b):
    if a == 0:
        return (b, 0 , 1)
    else:
        g, x, y = EEA(b % a, a)
        return (g, y - (b // a) * x, x)

def modularInverse(e, phi):
    g, x, _ = EEA(e, phi)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % phi
    
def getRandomRSAKey():
    bitsize = 1024
    n = randint(pow(2, (bitsize-1))+1, pow(2, bitsize)-1)
    while not millerRabin(n):
        n = randint(pow(2, (bitsize-1))+1, pow(2, bitsize)-1)
    p = n
    n = randint(pow(2, (bitsize-1))+1, pow(2, bitsize)-1)
    while not millerRabin(n):
        n = randint(pow(2, (bitsize-1))+1, pow(2, bitsize)-1)
    q = n
    n = p*q
    phi = (p - 1) * (q - 1)
    e = randint(2**15+1, 2**16-1)
    while gcd(e,phi) != 1:
        e = randint(2**15+1, 2**16-1)
    d = modularInverse(e, phi)
    filename = datetime.now().strftime("%d%m%Y%H%M%S")+".txt"
    f = open("Keys\\RSA\\"+filename, "w")
    f.write(str(e) + "\n")
    f.write(str(d) + "\n")
    f.write(str(n))
    return filename

def RSA(key, msg, mode):
    f = open("Keys\\RSA\\" + key, "r")
    key = f.readlines()
    f.close()
    if mode == "encode":
        new = []
        for c in msg:
            new.append(pow(full.index(c), int(key[0].strip()), int(key[2].strip())))
        new = [str(x) for x in new]
        return ".".join(new)
    else:
        new = []
        for c in msg.split("."):
            new.append(full[pow(int(c), int(key[1].strip()), int(key[2].strip()))])
        return "".join(new)
