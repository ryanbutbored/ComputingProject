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

def AES(plaintext, key, mode):
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
            print("ROUND: " +str(10-i))
            printMatrix(plainM)
        plainM = inverseShiftRows(plainM)
        plainM = subBytes(plainM, AES_S_BOX_INVERSE)
        plainM = convertMatrixHToB(plainM)
        plainM = addRoundKey(plainM, keys[10])
    print("FINAL")
    return plainM

def convertMatrixHToB(m):
    temp = [["","","",""],["","","",""],["","","",""],["","","",""]]
    for i in range(4):
        for j in range(4):
            temp[i][j] = hexToBinary(m[i][j])
    return temp

def printMatrix(m):
    for row in m:
        print(" ".join([binaryToHex(c) for c in row]))

key = "5468617473206D79204B756E67204675"
plaintext = "54776F204F6E652043696E252054776F"
ciphertext = "3CEDE758630FB55772C963A9D36CAEDA"


printMatrix(AES(plaintext, key, "encode"))
printMatrix(AES(ciphertext, key, "decode"))
    
##for row in mixColumns([["63", "EB", "9F", "A0"], ["2F", "93", "92", "C0"], ["AF", "C7", "AB", "30"], ["A2", "20", "CB", "2B"]]):
##    print(" ".join(row))

##temp = [["29", "46", "54", "5A"], ["50", "0B", "46", "42"], ["44", "42", "15", "06"], ["52", "10", "01", "16"]]
##newtemp = []
##for i in range(4):
##    newtemp.append([])
##    for j in range(4):
##        newtemp[i].append(hexToBinary(temp[i][j]))
##for row in shiftBytes(subBytes(newtemp)):
##    print(" ".join(row))
