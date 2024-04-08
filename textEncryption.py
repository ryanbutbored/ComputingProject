from string import ascii_uppercase as up, ascii_lowercase as low
from random import randint, choice
from datetime import datetime

base64 = "0123456789" + low + up +"+/"

full = ". " +low +up +"0123456789"

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

def binaryToDenary(b, length = -1):
    d = 0
    for i in range(len(b)-1, -1, -1):
        d += int(b[i]) * (2 ** (len(b)-1 - i))
    return d

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
    return randint(1, len(full)-1)

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
        new = [encodeb64(x) for x in new]
        return ".".join(new)
    else:
        new = []
        msg = [decodeb64(x) for x in msg.split(".")]
        for c in msg:
            new.append(full[pow(int(c), int(key[1].strip()), int(key[2].strip()))])
        return "".join(new)

def encodeb64(num):
    new = ""
    max = 0
    while pow(64, max+1) < num:
        max += 1
    for i in range(max, -1, -1):
        total = num // pow(64, i)
        new += base64[total]
        num -= pow(64, i) * total
        #print(new)
    return new

def decodeb64(string):
    num = 0
    for i in range(len(string)-1, -1, -1):
        num += base64.index(string[i]) * pow(64, len(string)-1-i)
    return str(num)

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

def permutate(string, p_table):
    newkey = ""
    for row in p_table:
        for n in row:
            newkey += string[n-1]
    return newkey

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
            row = binaryToDenary(data[0]+data[5])
            position = binaryToDenary(data[1:5])
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
    key = key.upper()
    if mode == "encode":
        binary = ""
        for c in plaintext:
            binary += getSixBitFromFull(c)
        binary = binaryToHex(binary)
    else:
        binary = plaintext.upper()
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
                result += full[binaryToDenary(segment)]
    else:
        for segment in segments:
            result += DES(segment, key, mode)
        
        if mode == "decode":
            binary = hexToBinary(result)
            segments = [binary[i:i+6] for i in range(0, len(binary), 6)]
            result = ""
            for segment in segments:
                result += full[binaryToDenary(segment)]
    return result

def getRandomDESKey(triple = False):
    h = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    if triple:
        n = 32
    else:
        n = 16
    key = "".join([choice(h) for i in range(n)])
    return key

#------------------------BLOWFISH--------------------------

BLOWFISH_S_BOXES = [[["D1310BA6", "98DFB5AC", "2FFD72DB", "D01ADFB7", "B8E1AFED", "6A267E96", "BA7C9045", "F12C7F99"],
                     ["24A19947", "B3916CF7", "0801F2E2", "858EFC16", "636920D8", "71574E69", "A458FEA3", "F4933D7E"],
                     ["0D95748F", "728EB658", "718BCD58", "82154AEE", "7B54A41D", "C25A59B5", "9C30D539", "2AF26013"],
                     ["C5D1B023", "286085F0", "CA417918", "B8DB38EF", "8E79DCB0", "603A180E", "6C9E0E8B", "B01E8A3E"],
                     ["D71577C1", "BD314B27", "78AF2FDA", "55605C60", "E65525F3", "AA55AB94", "57489862", "63E81440"],
                     ["55CA396A", "2AAB10B6", "B4CC5C34", "1141E8CE", "A15486AF", "7C72E993", "B3EE1411", "636FBC2A"],
                     ["2BA9C55D", "741831F6", "CE5C3E16", "9B87931E", "AFD6BA33", "6C24CF5C", "7A325381", "28958677"],
                     ["3B8F4898", "6B4BB9AF", "C4BFE81B", "66282193", "61D809CC", "FB21A991", "487CAC60", "5DEC8032"],
                     ["EF845D5D", "E98575B1", "DC262302", "EB651B88", "23893E81", "D396ACC5", "0F6D6FF3", "83F44239"],
                     ["2E0B4482", "A4842004", "69C8F04A", "9E1F9B5E", "21C66842", "F6E96C9A", "670C9C61", "ABD388F0"],
                     ["6A51A0D2", "D8542F68", "960FA728", "AB5133A3", "6EEF0B6C", "137A3BE4", "BA3BF050", "7EFB2A98"],
                     ["A1F1651D", "39AF0176", "66CA593E", "82430E88", "8CEE8619", "456F9FB4", "7D84A5C3", "3B8B5EBE"],
                     ["E06F75D8", "85C12073", "401A449F", "56C16AA6", "4ED3AA62", "363F7706", "1BFEDF72", "429B023D"],
                     ["37D0D724", "D00A1248", "DB0FEAD3", "49F1C09B", "075372C9", "80991B7B", "25D479D8", "F6E8DEF7"],
                     ["E3FE501A", "B6794C3B", "976CE0BD", "04C006BA", "C1A94FB6", "409F60C4", "5E5C9EC2", "196A2463"],
                     ["68FB6FAF", "3E6C53B5", "1339B2EB", "3B52EC6F", "6DFC511F", "9B30952C", "CC814544", "AF5EBD09"],
                     ["BEE3D004", "DE334AFD", "660F2807", "192E4BB3", "C0CBA857", "45C8740F", "D20B5F39", "B9D3FBDB"],
                     ["5579C0BD", "1A60320A", "D6A100C6", "402C7279", "679F25FE", "FB1FA3CC", "8EA5E9F8", "DB3222F8"],
                     ["3C7516DF", "FD616B15", "2F501EC8", "AD0552AB", "323DB5FA", "FD238760", "53317B48", "3E00DF82"],
                     ["9E5C57BB", "CA6F8CA0", "1A87562E", "DF1769DB", "D542A8F6", "287EFFC3", "AC6732C6", "8C4F5573"],
                     ["695B27B0", "BBCA58C8", "E1FFA35D", "B8F011A0", "10FA3D98", "FD2183B8", "4AFCB56C", "2DD1D35B"],
                     ["9A53E479", "B6F84565", "D28E49BC", "4BFB9790", "E1DDF2DA", "A4CB7E33", "62FB1341", "CEE4C6E8"],
                     ["EF20CADA", "36774C01", "D07E9EFE", "2BF11FB4", "95DBDA4D", "AE909198", "EAAD8E71", "6B93D5A0"],
                     ["D08ED1D0", "AFC725E0", "8E3C5B2F", "8E7594B7", "8FF6E2FB", "F2122B64", "8888B812", "900DF01C"],
                     ["4FAD5EA0", "688FC31C", "D1CFF191", "B3A8C1AD", "2F2F2218", "BE0E1777", "EA752DFE", "8B021FA1"],
                     ["E5A0CC0F", "B56F74E8", "18ACF3D6", "CE89E299", "B4A84FE0", "FD13E0B7", "7CC43B81", "D2ADA8D9"],
                     ["165FA266", "80957705", "93CC7314", "211A1477", "E6AD2065", "77B5FA86", "C75442F5", "FB9D35CF"],
                     ["EBCDAF0C", "7B3E89A0", "D6411BD3", "AE1E7E49", "00250E2D", "2071B35E", "226800BB", "57B8E0AF"],
                     ["2464369B", "F009B91E", "5563911D", "59DFA6AA", "78C14389", "D95A537F", "207D5BA2", "02E5B9C5"],
                     ["83260376", "6295CFA9", "11C81968", "4E734A41", "B3472DCA", "7B14A94A", "1B510052", "9A532915"],
                     ["D60F573F", "BC9BC6E4", "2B60A476", "81E67400", "08BA6FB5", "571BE91F", "F296EC6B", "2A0DD915"],
                     ["B6636521", "E7B9F9B6", "FF34052E", "C5855664", "53B02D5D", "A99F8FA1", "08BA4799", "6E85076A"]],
                    [["4B7A70E9", "B5B32944", "DB75092E", "C4192623", "AD6EA6B0", "49A7DF7D", "9CEE60B8", "8FEDB266"],
                     ["ECAA8C71", "699A17FF", "5664526C", "C2B19EE1", "193602A5", "75094C29", "A0591340", "E4183A3E"],
                     ["3F54989A", "5B429D65", "6B8FE4D6", "99F73FD6", "A1D29C07", "EFE830F5", "4D2D38E6", "F0255DC1"],
                     ["4CDD2086", "8470EB26", "6382E9C6", "021ECC5E", "09686B3F", "3EBAEFC9", "3C971814", "6B6A70A1"],
                     ["687F3584", "52A0E286", "B79C5305", "AA500737", "3E07841C", "7FDEAE5C", "8E7D44EC", "5716F2B8"],
                     ["B03ADA37", "F0500C0D", "F01C1F04", "0200B3FF", "AE0CF51A", "3CB574B2", "25837A58", "DC0921BD"],
                     ["D19113F9", "7CA92FF6", "94324773", "22F54701", "3AE5E581", "37C2DADC", "C8B57634", "9AF3DDA7"],
                     ["A9446146", "0FD0030E", "ECC8C73E", "A4751E41", "E238CD99", "3BEA0E2F", "3280BBA1", "183EB331"],
                     ["4E548B38", "4F6DB908", "6F420D03", "F60A04BF", "2CB81290", "24977C79", "5679B072", "BCAF89AF"],
                     ["DE9A771F", "D9930810", "B38BAE12", "DCCF3F2E", "5512721F", "2E6B7124", "501ADDE6", "9F84CD87"],
                     ["7A584718", "7408DA17", "BC9F9ABC", "E94B7D8C", "EC7AEC3A", "DB851DFA", "63094366", "C464C3D2"],
                     ["EF1C1847", "3215D908", "DD433B37", "24C2BA16", "12A14D43", "2A65C451", "50940002", "133AE4DD"],
                     ["71DFF89E", "10314E55", "81AC77D6", "5F11199B", "043556F1", "D7A3C76B", "3C11183B", "5924A509"],
                     ["F28FE6ED", "97F1FBFA", "9EBABF2C", "1E153C6E", "86E34570", "EAE96FB1", "860E5E0A", "5A3E2AB3"],
                     ["771FE71C", "4E3D06FA", "2965DCB9", "99E71D0F", "803E89D6", "5266C825", "2E4CC978", "9C10B36A"],
                     ["C6150EBA", "94E2EA78", "A5FC3C53", "1E0A2DF4", "F2F74EA7", "361D2B3D", "1939260F", "19C27960"],
                     ["5223A708", "F71312B6", "EBADFE6E", "EAC31F66", "E3BC4595", "A67BC883", "B17F37D1", "018CFF28"],
                     ["C332DDEF", "BE6C5AA5", "65582185", "68AB9802", "EECEA50F", "DB2F953B", "2AEF7DAD", "5B6E2F84"],
                     ["1521B628", "29076170", "ECDD4775", "619F1510", "13CCA830", "EB61BD96", "0334FE1E", "AA0363CF"],
                     ["B5735C90", "4C70A239", "D59E9E0B", "CBAADE14", "EECC86BC", "60622CA7", "9CAB5CAB", "B2F3846E"],
                     ["648B1EAF", "19BDF0CA", "A02369B9", "655ABB50", "40685A32", "3C2AB4B3", "319EE9D5", "C021B8F7"],
                     ["9B540B19", "875FA099", "95F7997E", "623D7DA8", "F837889A", "97E32D77", "11ED935F", "16681281"],
                     ["0E358829", "C7E61FD6", "96DEDFA1", "7858BA99", "57F584A5", "1B227263", "9B83C3FF", "1AC24696"],
                     ["CDB30AEB", "532E3054", "8FD948E4", "6DBC3128", "58EBF2EF", "34C6FFEA", "FE28ED61", "EE7C3C73"],
                     ["5D4A14D9", "E864B7E3", "42105D14", "203E13E0", "45EEE2B6", "A3AAABEA", "DB6C4F15", "FACB4FD0"],
                     ["C742F442", "EF6ABBB5", "654F3B1D", "41CD2105", "D81E799E", "86854DC7", "E44B476A", "3D816250"],
                     ["CF62A1F2", "5B8D2646", "FC8883A0", "C1C7B6A3", "7F1524C3", "69CB7492", "47848A0B", "5692B285"],
                     ["095BBF00", "AD19489D", "1462B174", "23820E00", "58428D2A", "0C55F5EA", "1DADF43E", "233F7061"],
                     ["3372F092", "8D937E41", "D65FECF1", "6C223BDB", "7CDE3759", "CBEE7460", "4085F2A7", "CE77326E"],
                     ["A6078084", "19F8509E", "E8EFD855", "61D99735", "A969A7AA", "C50C06C2", "5A04ABFC", "800BCADC"],
                     ["9E447A2E", "C3453484", "FDD56705", "0E1E9EC9", "DB73DBD3", "105588CD", "675FDA79", "E3674340"],
                     ["C5C43465", "713E38D8", "3D28F89E", "F16DFF20", "153E21E7", "8FB03D4A", "E6E39F2B", "DB83ADF7"]],
                    [["E93D5A68", "948140F7", "F64C261C", "94692934", "411520F7", "7602D4F7", "BCF46B2E", "D4A20068"],
                     ["D4082471", "3320F46A", "43B7D4B7", "500061AF", "1E39F62E", "97244546", "14214F74", "BF8B8840"],
                     ["4D95FC1D", "96B591AF", "70F4DDD3", "66A02F45", "BFBC09EC", "03BD9785", "7FAC6DD0", "31CB8504"],
                     ["96EB27B3", "55FD3941", "DA2547E6", "ABCA0A9A", "28507825", "530429F4", "0A2C86DA", "E9B66DFB"],
                     ["68DC1462", "D7486900", "680EC0A4", "27A18DEE", "4F3FFEA2", "E887AD8C", "B58CE006", "7AF4D6B6"],
                     ["AACE1E7C", "D3375FEC", "CE78A399", "406B2A42", "20FE9E35", "D9F385B9", "EE39D7AB", "3B124E8B"],
                     ["1DC9FAF7", "4B6D1856", "26A36631", "EAE397B2", "3A6EFA74", "DD5B4332", "6841E7F7", "CA7820FB"],
                     ["FB0AF54E", "D8FEB397", "454056AC", "BA489527", "55533A3A", "20838D87", "FE6BA9B7", "D096954B"],
                     ["55A867BC", "A1159A58", "CCA92963", "99E1DB33", "A62A4A56", "3F3125F9", "5EF47E1C", "9029317C"],
                     ["FDF8E802", "04272F70", "80BB155C", "05282CE3", "95C11548", "E4C66D22", "48C1133F", "C70F86DC"],
                     ["07F9C9EE", "41041F0F", "404779A4", "5D886E17", "325F51EB", "D59BC0D1", "F2BCC18F", "41113564"],
                     ["257B7834", "602A9C60", "DFF8E8A3", "1F636C1B", "0E12B4C2", "02E1329E", "AF664FD1", "CAD18115"],
                     ["6B2395E0", "333E92E1", "3B240B62", "EEBEB922", "85B2A20E", "E6BA0D99", "DE720C8C", "2DA2F728"],
                     ["D0127845", "95B794FD", "647D0862", "E7CCF5F0", "5449A36F", "877D48FA", "C39DFD27", "F33E8D1E"],
                     ["0A476341", "992EFF74", "3A6F6EAB", "F4F8FD37", "A812DC60", "A1EBDDF8", "991BE14C", "DB6E6B0D"],
                     ["C67B5510", "6D672C37", "2765D43B", "DCD0E804", "F1290DC7", "CC00FFA3", "B5390F92", "690FED0B"],
                     ["667B9FFB", "CEDB7D9C", "A091CF0B", "D9155EA3", "BB132F88", "515BAD24", "7B9479BF", "763BD6EB"],
                     ["37392EB3", "CC115979", "8026E297", "F42E312D", "6842ADA7", "C66A2B3B", "12754CCC", "782EF11C"],
                     ["6A124237", "B79251E7", "06A1BBE6", "4BFB6350", "1A6B1018", "11CAEDFA", "3D25BDD8", "E2E1C3C9"],
                     ["44421659", "0A121386", "D90CEC6E", "D5ABEA2A", "64AF674E", "DA86A85F", "BEBFE988", "64E4C3FE"],
                     ["9DBC8057", "F0F7C086", "60787BF8", "6003604D", "D1FD8346", "F6381FB0", "7745AE04", "D736FCCC"],
                     ["83426B33", "F01EAB71", "B0804187", "3C005E5F", "77A057BE", "BDE8AE24", "55464299", "BF582E61"],
                     ["4E58F48F", "F2DDFDA2", "F474EF38", "8789BDC2", "5366F9C3", "C8B38E74", "B475F255", "46FCD9B9"],
                     ["7AEB2661", "8B1DDF84", "846A0E79", "915F95E2", "466E598E", "20B45770", "8CD55591", "C902DE4C"],
                     ["B90BACE1", "BB8205D0", "11A86248", "7574A99E", "B77F19B6", "E0A9DC09", "662D09A1", "C4324633"],
                     ["E85A1F02", "09F0BE8C", "4A99A025", "1D6EFE10", "1AB93D1D", "0BA5A4DF", "A186F20F", "2868F169"],
                     ["DCB7DA83", "573906FE", "A1E2CE9B", "4FCD7F52", "50115E01", "A70683FA", "A002B5C4", "0DE6D027"],
                     ["9AF88C27", "773F8641", "C3604C06", "61A806B5", "F0177A28", "C0F586E0", "006058AA", "30DC7D62"],
                     ["11E69ED7", "2338EA63", "53C2DD94", "C2C21634", "BBCBEE56", "90BCB6DE", "EBFC7DA1", "CE591D76"],
                     ["6F05E409", "4B7C0188", "39720A3D", "7C927C24", "86E3725F", "724D9DB9", "1AC15BB4", "D39EB8FC"],
                     ["ED545578", "08FCA5B5", "D83D7CD3", "4DAD0FC4", "1E50EF5E", "B161E6F8", "A28514D9", "6C51133C"],
                     ["6FD5C7E7", "56E14EC4", "362ABFCE", "DDC6C837", "D79A3234", "92638212", "670EFA8E", "406000E0"]],
                    [["3A39CE37", "D3FAF5CF", "ABC27737", "5AC52D1B", "5CB0679E", "4FA33742", "D3822740", "99BC9BBE"],
                     ["D5118E9D", "BF0F7315", "D62D1C7E", "C700C47B", "B78C1B6B", "21A19045", "B26EB1BE", "6A366EB4"],
                     ["5748AB2F", "BC946E79", "C6A376D2", "6549C2C8", "530FF8EE", "468DDE7D", "D5730A1D", "4CD04DC6"],
                     ["2939BBDB", "A9BA4650", "AC9526E8", "BE5EE304", "A1FAD5F0", "6A2D519A", "63EF8CE2", "9A86EE22"],
                     ["C089C2B8", "43242EF6", "A51E03AA", "9CF2D0A4", "83C061BA", "9BE96A4D", "8FE51550", "BA645BD6"],
                     ["2826A2F9", "A73A3AE1", "4BA99586", "EF5562E9", "C72FEFD3", "F752F7DA", "3F046F69", "77FA0A59"],
                     ["80E4A915", "87B08601", "9B09E6AD", "3B3EE593", "E990FD5A", "9E34D797", "2CF0B7D9", "022B8B51"],
                     ["96D5AC3A", "017DA67D", "D1CF3ED6", "7C7D2D28", "1F9F25CF", "ADF2B89B", "5AD6B472", "5A88F54C"],
                     ["E029AC71", "E019A5E6", "47B0ACFD", "ED93FA9B", "E8D3C48D", "283B57CC", "F8D56629", "79132E28"],
                     ["785F0191", "ED756055", "F7960E44", "E3D35E8C", "15056DD4", "88F46DBA", "03A16125", "0564F0BD"],
                     ["C3EB9E15", "3C9057A2", "97271AEC", "A93A072A", "1B3F6D9B", "1E6321F5", "F59C66FB", "26DCF319"],
                     ["7533D928", "B155FDF5", "03563482", "8ABA3CBB", "28517711", "C20AD9F8", "ABCC5167", "CCAD925F"],
                     ["4DE81751", "3830DC8E", "379D5862", "9320F991", "EA7A90C2", "FB3E7BCE", "5121CE64", "774FBE32"],
                     ["A8B6E37E", "C3293D46", "48DE5369", "6413E680", "A2AE0810", "DD6DB224", "69852DFD", "09072166"],
                     ["B39A460A", "6445C0DD", "586CDECF", "1C20C8AE", "5BBEF7DD", "1B588D40", "CCD2017F", "6BB4E3BB"],
                     ["DDA26A7E", "3A59FF45", "3E350A44", "BCB4CDD5", "72EACEA8", "FA6484BB", "8D6612AE", "BF3C6F47"],
                     ["D29BE463", "542F5D9E", "AEC2771B", "F64E6370", "740E0D8D", "E75B1357", "F8721671", "AF537D5D"],
                     ["4040CB08", "4EB4E2CC", "34D2466A", "0115AF84", "E1B00428", "95983A1D", "06B89FB4", "CE6EA048"],
                     ["6F3F3B82", "3520AB82", "011A1D4B", "277227F8", "611560B1", "E7933FDC", "BB3A792B", "344525BD"],
                     ["A08839E1", "51CE794B", "2F32C9B7", "A01FBAC9", "E01CC87E", "BCC7D1F6", "CF0111C3", "A1E8AAC7"],
                     ["1A908749", "D44FBD9A", "D0DADECB", "D50ADA38", "0339C32A", "C6913667", "8DF9317C", "E0B12B4F"],
                     ["F79E59B7", "43F5BB3A", "F2D519FF", "27D9459C", "BF97222C", "15E6FC2A", "0F91FC71", "9B941525"],
                     ["FAE59361", "CEB69CEB", "C2A86459", "12BAA8D1", "B6C1075E", "E3056A0C", "10D25065", "CB03A442"],
                     ["E0EC6E0E", "1698DB3B", "4C98A0BE", "3278E964", "9F1F9532", "E0D392DF", "D3A0342B", "8971F21E"],
                     ["1B0A7441", "4BA3348C", "C5BE7120", "C37632D8", "DF359F8D", "9B992F2E", "E60B6F47", "0FE3F11D"],
                     ["E54CDA54", "1EDAD891", "CE6279CF", "CD3E7E6F", "1618B166", "FD2C1D05", "848FD2C5", "F6FB2299"],
                     ["F523F357", "A6327623", "93A83531", "56CCCD02", "ACF08162", "5A75EBB5", "6E163697", "88D273CC"],
                     ["DE966292", "81B949D0", "4C50901B", "71C65614", "E6C6C7BD", "327A140A", "45E1D006", "C3F27B9A"],
                     ["C9AA53FD", "62A80F00", "BB25BFE2", "35BDD2F6", "71126905", "B2040222", "B6CBCF7C", "CD769C2B"],
                     ["53113EC0", "1640E3D3", "38ABBD60", "2547ADF0", "BA38209C", "F746CE76", "77AFA1C5", "20756060"],
                     ["85CBFE4E", "8AE88DD8", "7AAAF9B0", "4CF9AA7E", "1948C25C", "02FB8A8C", "01C36AE4", "D6EBE1F9"],
                     ["90D4F869", "A65CDEA0", "3F09252D", "C208E69F", "B74E6132", "CE77E25B", "578FDFE3", "3AC372E6"]]]


BLOWFISH_P = ["243F6A88", "85A308D3", "13198A2E", "03707344", "A4093822", "299F31D0",
              "082EFA98", "EC4E6C89", "452821E6", "38D01377", "BE5466CF", "34E90C6C",
              "C0AC29B7", "C97C50DD", "3F84D5B5", "B5470917", "9216D5D9", "8979FB1B"]

def add(b1, b2):
    new = []
    overflow = "0"
    for i in range(len(b1)-1, -1, -1):
        count = {"1":0, "0":0}
        count[overflow] += 1
        count[b1[i]] += 1
        count[b2[i]] += 1
        count = count["1"]
        if count != 0:
            if count == 1:
                new.append("1")
                overflow = "0"
            elif count == 2:
                new.append("0")
                overflow = "1"
            else:
                new.append("1")
                overflow = "1"
        else:
            new.append("0")
            overflow = "0"
    return "".join(new[::-1])

def blowfishF(b):
    values = [b[i:i+8] for i in range(0, 32, 8)]
    sBoxValues = []
    for i, value in enumerate(values):
        row = binaryToDenary(value[0:5])
        column = binaryToDenary(value[5:])
        sBoxValues.append(hexToBinary(BLOWFISH_S_BOXES[i][row][column]))
    result1 = add(sBoxValues[0], sBoxValues[1])
    result2 = doXOR(result1, sBoxValues[2])
    return add(result2, sBoxValues[3])

def blowfish(key, msg, mode):
    key = hexToBinary(key)
    p_array = [hexToBinary(p) for p in BLOWFISH_P]
    key = [key[i:i+32] for i in range(0, len(key), 32)]
    subkeys = []
    i = 0
    for j in range(18):
        if i == len(key):
            i = 0
        newSubkey = doXOR(key[i], p_array[j])
        subkeys.append(newSubkey)
        i += 1
    if mode == "decode":
        subkeys = subkeys[::-1]
        msg = hexToBinary(msg)
    else:
        new = ""
        for c in msg:
            new += getSixBitFromFull(c)
        msg = new
    msg = [msg[i:i+64] for i in range(0, len(msg), 64)]
    #do rounds
    new = ""
    for part in msg:
        lefts = [part[0:32]]
        rights = [part[32:]]
        for i in range(16):
            result1 = doXOR(lefts[-1], subkeys[i])
            result2 = blowfishF(result1)
            result3 = doXOR(result2, rights[-1])
            rights.append(result1)
            lefts.append(result3)
        finalLeft = doXOR(rights[-1], subkeys[17])
        finalRight = doXOR(lefts[-1], subkeys[16])
        new += binaryToHex(finalLeft + finalRight)
    if mode == "decode":
        new = hexToBinary(new)
        newmsg = ""
        for i in range(len(new) // 6):
            newmsg += full[binaryToDenary(new[i*6:(i + 1) * 6])]
        new = newmsg
    return new

def getRandomBlowfishKey():
    h = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    key = "".join([choice(h) for i in range(112)])
    return key

#------------------------AES--------------------------
#https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf

def getRandomAESKey():
    h = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    key = "".join([choice(h) for i in range(32)])
    return key

AES_S_BOX = [["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
             ["CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"],
             ["B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15"],
             ["04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75"],
             ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84"],
             ["53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"],
             ["D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8"],
             ["51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"],
             ["CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73"],
             ["60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"],
             ["E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79"],
             ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08"],
             ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"],
             ["70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E"],
             ["E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF"],
             ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]]

AES_S_BOX_INVERSE = [["52", "09", "6A", "D5", "30", "36", "A5", "38", "BF", "40", "A3", "9E", "81", "F3", "D7", "FB"],
                     ["7C", "E3", "39", "82", "9B", "2F", "FF", "87", "34", "8E", "43", "44", "C4", "DE", "E9", "CB"],
                     ["54", "7B", "94", "32", "A6", "C2", "23", "3D", "EE", "4C", "95", "0B", "42", "FA", "C3", "4E"],
                     ["08", "2E", "A1", "66", "28", "D9", "24", "B2", "76", "5B", "A2", "49", "6D", "8B", "D1", "25"],
                     ["72", "F8", "F6", "64", "86", "68", "98", "16", "D4", "A4", "5C", "CC", "5D", "65", "B6", "92"],
                     ["6C", "70", "48", "50", "FD", "ED", "B9", "DA", "5E", "15", "46", "57", "A7", "8D", "9D", "84"],
                     ["90", "D8", "AB", "00", "8C", "BC", "D3", "0A", "F7", "E4", "58", "05", "B8", "B3", "45", "06"],
                     ["D0", "2C", "1E", "8F", "CA", "3F", "0F", "02", "C1", "AF", "BD", "03", "01", "13", "8A", "6B"],
                     ["3A", "91", "11", "41", "4F", "67", "DC", "EA", "97", "F2", "CF", "CE", "F0", "B4", "E6", "73"],
                     ["96", "AC", "74", "22", "E7", "AD", "35", "85", "E2", "F9", "37", "E8", "1C", "75", "DF", "6E"],
                     ["47", "F1", "1A", "71", "1D", "29", "C5", "89", "6F", "B7", "62", "0E", "AA", "18", "BE", "1B"],
                     ["FC", "56", "3E", "4B", "C6", "D2", "79", "20", "9A", "DB", "C0", "FE", "78", "CD", "5A", "F4"],
                     ["1F", "DD", "A8", "33", "88", "07", "C7", "31", "B1", "12", "10", "59", "27", "80", "EC", "5F"],
                     ["60", "51", "7F", "A9", "19", "B5", "4A", "0D", "2D", "E5", "7A", "9F", "93", "C9", "9C", "EF"],
                     ["A0", "E0", "3B", "4D", "AE", "2A", "F5", "B0", "C8", "EB", "BB", "3C", "83", "53", "99", "61"],
                     ["17", "2B", "04", "7E", "BA", "77", "D6", "26", "E1", "69", "14", "63", "55", "21", "0C", "7D"]]

AES_CONSTANT = [[2, 3, 1, 1],
                [1, 2, 3, 1],
                [1, 1, 2, 3],
                [3, 1, 1, 2]]

AES_CONSTANT_INVERSE = [[14, 11, 13, 9],
                        [9, 14, 11, 13],
                        [13, 9, 14, 11],
                        [11, 13, 9, 14]]

RCI = ["01", "02", "04", "08", "10", "20", "40", "80", "1B", "36"]

def addRoundKey(plainM, keyM):
    newStateM = [["","","",""],["","","",""],["","","",""],["","","",""]]
    for i in range(4):
        for j in range(4):
            newStateM[i][j] = doXOR(plainM[i][j], keyM[i][j])
    return newStateM

def subBytes(initialM, s_box):
    finalM = [["","","",""],["","","",""],["","","",""],["","","",""]]
    for i in range(4):
        for j in range(4):
            row = binaryToDenary(initialM[i][j][0:4])
            column = binaryToDenary(initialM[i][j][4:])
            finalM[i][j] = s_box[row][column]
    return finalM

def shiftRows(oldStateM):
    newStateM = [oldStateM[0]]
    newStateM.append(oldStateM[1][1:] + [oldStateM[1][0]])
    newStateM.append(oldStateM[2][2:] + oldStateM[2][0:2])
    newStateM.append([oldStateM[3][3]] + oldStateM[3][0:3])
    return newStateM

def inverseShiftRows(oldStateM):
    newStateM = [oldStateM[0]]
    newStateM.append([oldStateM[1][3]] + oldStateM[1][0:3])
    newStateM.append(oldStateM[2][2:] + oldStateM[2][0:2])
    newStateM.append(oldStateM[3][1:] + [oldStateM[3][0]])
    return newStateM

def calculateValue(b, d):
    if d == 2:
        first = b[0]
        b = b[1:] + "0"
        if first == "1":
            b = doXOR(b, "00011011")
    if d == 3:
        temp = calculateValue(b, 2)
        b = doXOR(b, temp)
    if d == 9:
        temp = calculateValue(b, 2)
        temp = calculateValue(temp, 2)
        temp = calculateValue(temp, 2)
        b = doXOR(b, temp)
    if d == 11:
        temp = calculateValue(b, 2)
        temp = calculateValue(temp, 2)
        temp = doXOR(b, temp)
        temp = calculateValue(temp, 2)
        b = doXOR(b, temp)
    if d == 13:
        temp = calculateValue(b, 2)
        temp = doXOR(b, temp)
        temp = calculateValue(temp, 2)
        temp = calculateValue(temp, 2)
        b = doXOR(b, temp)
    if d == 14:
        temp = calculateValue(b, 2)
        temp = doXOR(b, temp)
        temp = calculateValue(temp, 2)
        b = doXOR(b, temp)
        b = calculateValue(b, 2)
    return b

def mixColumn(column, constantState):
    newColumn = []
    for i in range(4):
        tempColumn  = []
        for j in range(4):
            tempColumn.append(calculateValue(column[j], constantState[i][j]))
        value = tempColumn[0]
        for j in range(1, 4):
            value = doXOR(value, tempColumn[j])
        newColumn.append(value)
    return newColumn

def mixColumns(oldState, constantState):
    newState = [[], [], [], []]
    for i in range(4):
        column = [oldState[0][i], oldState[1][i], oldState[2][i], oldState[3][i]] 
        column = mixColumn(column, constantState)
        for j in range(4):
            newState[j].append(column[j])
    return newState

def genKeys(keyM):
    keys = [keyM]
    for i in range(10):
        words = []
        for j in range(4):
            words.append([keys[i][0][j], keys[i][1][j], keys[i][2][j], keys[i][3][j]])
        processedWord = rotWord(words[3])
        processedWord = subWord(processedWord)
        processedWord = rcon(processedWord, i)
        newKey = [[],[],[],[]]
        for j in range(4):
            newKey[j].append(doXOR(processedWord[j], words[0][j]))
        for j in range(1,4):
            for k in range(4):
                newKey[k].append(doXOR(newKey[k][j-1], words[j][k]))
        keys.append(newKey)
    return keys
        
def rotWord(word):
    return word[1:] + [word[0]]

def subWord(word):
    for i in range(4):
        row = binaryToDenary(word[i][0:4])
        column = binaryToDenary(word[i][4:])
        word[i] = AES_S_BOX[row][column]
    return word
        
def rcon(word, i):
    return [doXOR(hexToBinary(word[0]), hexToBinary(RCI[i]))] + [hexToBinary(c) for c in word[1:]]

def AES(key, plaintext, mode):
    if mode == "encode":
        new = ""
        for c in plaintext:
            new += getSixBitFromFull(c)
            plaintext = new
        plaintext = binaryToHex(plaintext)
    plaintexts = [plaintext[i:i+32] for i in range(0, len(plaintext), 32)]
    new = ""
    for plaintext in plaintexts:
        keyM = [[],[],[],[]]
        plainM = [[],[],[],[]]
        for i in range(4):
            for j in range(4):
                index = ((i*4) + j) * 2
                keyM[j].append(hexToBinary(key[index:index+2]))
                plainM[j].append(hexToBinary(plaintext[index:index+2]))
        keys = genKeys(keyM)
        #initial round
        if mode == "encode":
            plainM = addRoundKey(plainM, keys[0])
            #9 rounds
            for i in range(1,10):
                plainM = subBytes(plainM, AES_S_BOX)
                plainM = shiftRows(plainM)
                plainM = convertMatrixHToB(plainM)
                plainM = mixColumns(plainM, AES_CONSTANT)
                plainM = addRoundKey(plainM, keys[i])
            #final round
            plainM = subBytes(plainM, AES_S_BOX)
            plainM = shiftRows(plainM)
            plainM = convertMatrixHToB(plainM)
            plainM = addRoundKey(plainM, keys[10])
        else:
            keys = keys[::-1]
            plainM = addRoundKey(plainM, keys[0])
            for i in range(1,10):
                plainM = inverseShiftRows(plainM)
                plainM = subBytes(plainM, AES_S_BOX_INVERSE)
                plainM = convertMatrixHToB(plainM)
                plainM = addRoundKey(plainM, keys[i])
                plainM = mixColumns(plainM, AES_CONSTANT_INVERSE)
            plainM = inverseShiftRows(plainM)
            plainM = subBytes(plainM, AES_S_BOX_INVERSE)
            plainM = convertMatrixHToB(plainM)
            plainM = addRoundKey(plainM, keys[10])
        for x in range(4):
            for y in range(4):
                new += plainM[y][x]
    if mode == "encode":
        return binaryToHex(new)
    else:
        temp = [new[i:i+6] for i in range(0, len(new), 6)]
        new = ""
        for value in temp:
            new += full[binaryToDenary(value)]
        return new

def convertMatrixHToB(m):
    temp = [["","","",""],["","","",""],["","","",""],["","","",""]]
    for i in range(4):
        for j in range(4):
            temp[i][j] = hexToBinary(m[i][j])
    return temp