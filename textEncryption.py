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



#------------------------DES/3DES--------------------------
    
PC_ONE = [[57, 49, 41, 33, 25, 17, 9],
          [1, 58, 50, 42, 34, 26, 18],
          [10, 2, 59, 51, 43, 35, 27],
          [19, 11, 3, 60, 52, 44, 36],
          [63, 55, 47, 39, 31, 23, 15],
          [7, 62, 54, 46, 38, 30, 22],
          [14, 6, 61, 53, 45, 37, 29],
          [21, 13, 5, 28, 20, 12, 4]]

SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC_TWO = [[14, 17, 11, 24, 1, 5],
          [3, 28, 15, 6, 21, 10],
          [23, 19, 12, 4, 26, 8],
          [16, 7, 27, 20, 13, 2],
          [41, 52, 31, 37, 47, 55],
          [30, 40, 51, 45, 33, 48],
          [44, 49, 39, 56, 34, 53],
          [46, 42, 50, 36, 29, 32]]

IP = [[58, 50, 42, 34, 26, 18, 10, 2],
      [60, 52, 44, 36, 28, 20, 12, 4],
      [62, 54, 46, 38, 30, 22, 14, 6],
      [64, 56, 48, 40, 32, 24, 16, 8],
      [57, 49, 41, 33, 25, 17, 9, 1],
      [59, 51, 43, 35, 27, 19, 11, 3],
      [61, 53, 45, 37, 29, 21, 13, 5],
      [63, 55, 47, 39, 31, 23, 15, 7]]

IP = [[58, 50, 42, 34, 26, 18, 10, 2],
      [60, 52, 44, 36, 28, 20, 12, 4],
      [62, 54, 46, 38, 30, 22, 14, 6],
      [64, 56, 48, 40, 32, 24, 16, 8],
      [57, 49, 41, 33, 25, 17, 9, 1],
      [59, 51, 43, 35, 27, 19, 11, 3],
      [61, 53, 45, 37, 29, 21, 13, 5],
      [63, 55, 47, 39, 31, 23, 15, 7]]

E_BIT = [[32, 1, 2, 3, 4, 5],
         [4, 5, 6, 7, 8, 9],
         [8, 9, 10, 11, 12, 13],
         [12, 13, 14, 15, 16, 17],
         [16, 17, 18, 19,  20, 21],
         [20, 21, 22, 23, 24, 25],
         [24, 25, 26, 27, 28, 29],
         [28, 29, 30, 31, 32, 1]]

S_BOXES = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
           [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
           [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
           [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
           [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
           [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
           [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
           [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

P = [[16, 7, 20, 21],
     [29, 12, 28, 17],
     [1, 15, 23, 26],
     [5, 18, 31, 10],
     [2, 8, 24, 14],
     [32, 27, 3, 9],
     [19, 13, 30, 6],
     [22, 11, 4, 25]]

FINAL = [[40, 8, 48, 16, 56, 24, 64, 32],
         [39, 7, 47, 15, 55, 23, 63, 31],
         [38, 6, 46, 14, 54, 22, 62, 30],
         [37, 5, 45, 13, 53, 21, 61, 29],
         [36, 4, 44, 12, 52, 20, 60, 28],
         [35, 3, 43, 11, 51, 19, 59, 27],
         [34, 2, 42, 10, 50, 18, 58, 26],
         [33, 1, 41, 9, 49, 17, 57, 25]]

def getSixBitFromFull(c):
    index = full.index(c)
    data = ""
    values = [32, 16, 8, 4, 2, 1]
    for n in values:
        if index >= n:
            data += "1"
            index -= n
        else:
            data += "0"
    return data

def permutate(string, p_table):
    newkey = ""
    for row in p_table:
        for n in row:
            newkey += string[n-1]
    return newkey

def hexToBinary(h):
    conversion_table = {"0":"0000", "1":"0001", "2":"0010", "3":"0011",
                        "4":"0100", "5":"0101", "6":"0110", "7":"0111",
                        "8":"1000", "9":"1001", "A":"1010", "B":"1011",
                        "C":"1100", "D":"1101", "E":"1110", "F":"1111"}
    b = ""
    for l in h:
        b += conversion_table[l]
    return b

def binaryToHex(b):
    conversion_table = {"0000":"0", "0001":"1", "0010":"2", "0011":"3",
                        "0100":"4", "0101":"5", "0110":"6", "0111":"7",
                        "1000":"8", "1001":"9", "1010":"A", "1011":"B",
                        "1100":"C", "1101":"D", "1110":"E", "1111":"F"}
    b = [b[i:i+4] for i in range(0, len(b), 4)]
    h = ""
    for data in b:
        h += conversion_table[data]
    return h

def XOR(b1, b2):
    if b1 != b2:
        return "1"
    else:
        return "0"

def doXOR(data1, data2):
    new_data = ""
    for i, b1 in enumerate(data1):
        new_data += XOR(b1, data2[i])
    return new_data

def fourBitToDenary(data):
    return int(data[0])*8 + int(data[1])*4 + int(data[2])*2 + int(data[3])

def sixBitToDenary(data):
    return int(data[0])*32 + int(data[1])*16 + int(data[2])*8 + int(data[3])*4 + int(data[4])*2 + int(data[5])

def twoBitToDenary(data):
    return int(data[0])*2 + int(data[1])

def denaryToFourBit(num):
    data = ""
    values = [8, 4, 2, 1]
    for n in values:
        if num >= n:
            data += "1"
            num -= n
        else:
            data += "0"
    return data

def parseKey(key):
    key = hexToBinary(key)
    key_plus = permutate(key, PC_ONE)
    c = [key_plus[0:28]]
    d = [key_plus[28:]]
    for i, n in enumerate(SCHEDULE):
        c.append(c[-1][n:]+c[-1][0:n])
        d.append(d[-1][n:]+d[-1][0:n])
    subkeys = []
    for i in range(1, 17):
        subkeys.append(permutate(c[i]+d[i], PC_TWO))
    return subkeys


def Encode(plaintext, subkeys):
    plaintext = hexToBinary(plaintext)
    plaintext = permutate(plaintext, IP)
    left = [plaintext[0:32]]
    right = [plaintext[32:]]
    for i in range(16):
        left.append(right[-1])
        expanded_right = permutate(right[-1], E_BIT)
        expanded_right = doXOR(expanded_right, subkeys[i])
        expanded_right = [expanded_right[i:i+6] for i in range(0, 48, 6)]
        new_r = ""
        for s_number, data in enumerate(expanded_right):
            row = twoBitToDenary(data[0]+data[5])
            position = fourBitToDenary(data[1:5])
            new_r += denaryToFourBit(S_BOXES[s_number][row][position])
        new_r = permutate(new_r, P)
        right.append(doXOR(new_r, left[-2]))
    reverse = right[-1] + left[-1]
    reverse = permutate(reverse, FINAL)
    return binaryToHex(reverse)

def DES (plaintext, key, mode):
    subkeys = parseKey(key)
    if mode == "decode":
        subkeys = subkeys[::-1]
    return Encode(plaintext, subkeys)

def TDES(plaintext, key1, key2, mode):
    keys = [key1, key2, key1]
    r = [0, 1, 2]
    if mode == "decode":
        r = [2, 1, 0]
    for i in r:
        subkeys = parseKey(keys[i])
        if mode == "decode":
            subkeys = subkeys[::-1]
        plaintext = Encode(plaintext, subkeys)
    return plaintext

def doDES(key, plaintext, mode, triple = False):
    if mode == "encode":
        binary = ""
        for c in plaintext:
            binary += getSixBitFromFull(c)
        binary = binaryToHex(binary)
    else:
        binary = plaintext
    segments = [binary[i:i+16] for i in range(0, len(binary), 16)]
    result = ""
    if triple:
        key1, key2 = key[:16], key[16:]
        for segment in segments:
            result += TDES(segment, key1, key2, mode)
        if mode == "decode":
            binary = hexToBinary(result)
            segments = [binary[i:i+6] for i in range(0, len(binary), 6)]
            result = ""
            for segment in segments:
                result += full[sixBitToDenary(segment)]
    else:
        for segment in segments:
            result += DES(segment, key, mode)
        
        if mode == "decode":
            binary = hexToBinary(result)
            segments = [binary[i:i+6] for i in range(0, len(binary), 6)]
            result = ""
            for segment in segments:
                result += full[sixBitToDenary(segment)]
    return result

def getRandomDESKey(triple = False):
    h = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    if triple:
        n = 32
    else:
        n = 16
    key = "".join([choice(h) for i in range(n)])
    return key