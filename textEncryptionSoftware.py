from tkinter import *
from tkinter import font
import textEncryption
from time import time
from sys import getsizeof
from datetime import datetime

def scoreAllAlgorithms():
    timeTaken = time()
    analysisButton.config(state = "disabled")
    root.update()
    results = {}
    for option in options:
        choice.set(option)
        results[option] = scoreAlgorithm(filename = "Test Cases\\encryptionTestCases100.txt", delay = 0, createDisplayandReport = False)
    analysisButton.config(state = "normal")
    print("Time Taken: " +str(time() - timeTaken) +" seconds")
    f = open("Reports\\Detailed Report.txt", "w")
    fields = ["Key Size", "Key Generation Time", "Encryption Time", "Decryption Time", "Encryption Ratio"]
    units = ["bytes", "seconds", "seconds", "seconds", ""]
    for index, field in enumerate(fields):
        rankings = []
        unit = units[index]
        values = [results[key][index] for key in results.keys()]
        values.sort()
        for value in values:
            for key in results.keys():
                if results[key][index] == value and key not in rankings:
                    rankings.append(key)
        f.write(field+"\n----------------------\n")
        for index, value in enumerate(rankings):
            f.write(str(index+1) +". " +value  +str(values[index]) +" " +unit +"\n")
        f.write("\n\n")

    f.close()
    root.update()
    

def scoreAlgorithm(filename = "Test Cases\\encryptionTestCases10.txt", delay = -1, createDisplayandReport = True):
    scoreButton.config(state = "disabled")
    root.update()
    if delay == -1:
        delay = delayScale.get()
    f = open(filename, "r")
    keysizes = []
    keygentimes = []
    encryptionspeed = []
    decryptionspeed = []
    ratios = []
    lines = f.readlines()
    f.close()
    cases = []
    for line in lines:
        cases.append(line[0:len(line)-1])
    for case in cases:
        a = time()
        GenerateRandomKey()
        b = time()
        key = keychoice.get()
        if choice.get() in ["Caesar Shift", "Rail-Fence Cipher"]:
            key = int(key)
        size = getsizeof(key)
        keysizes.append(size)
        root.update()
        keygentimes.append(b-a)
        root.after(delay)
        plaintext.delete("1.0", END)
        plaintext.insert("1.0", case)
        root.update()
        root.after(delay)
        a = time()
        Encrypt()
        b = time()
        encryptionspeed.append(b-a)
        plaintext.delete("1.0", END)
        root.update()
        root.after(delay)
        a = time()
        Decrypt()
        b = time()
        decryptionspeed.append(b-a)
        cipher = ciphertext.get("1.0", END).strip("\n")
        ratios.append(len(cipher)/len(case))
        ciphertext.delete("1.0", END)
        root.update()
        root.after(delay)
        plaintext.delete("1.0", END)
        keychoice.delete(0,END)
        root.update()
        root.after(delay)
    now = datetime.now()
    total = len(cases)
    if createDisplayandReport:
        f = open("Reports\\"+choice.get().replace(" ", "")+"-"+now.strftime("%d%m%Y%H%M%S")+".txt", "w")
        f.write("Average Values\n")
        f.write("-------------------------------\n")
        f.write("Key Size: " +str(sum(keysizes)/total)+" bytes"+"\n")
        f.write("Key Generation Time: "+str(sum(keygentimes)/total)+" seconds"+"\n")
        f.write("Encryption Time: "+str(sum(encryptionspeed)/total)+" seconds"+"\n")
        f.write("Decryption Time: "+str(sum(decryptionspeed)/total)+" seconds"+"\n")
        f.write("Encryption Ratio: "+str(sum(ratios)/total)+"\n")
        f.write("-------------------------------\n")
        f.write("\n")
        for i in range(10):
            f.write("Cycle " +str(i+1)+"\n")
            f.write("-------------------------------\n")
            f.write("Key Size: " +str(keysizes[i])+" bytes"+"\n")
            f.write("Key Generation Time: "+str(keygentimes[i])+" seconds"+"\n")
            f.write("Encryption Time: "+str(encryptionspeed[i])+" seconds"+"\n")
            f.write("Decryption Time: "+str(decryptionspeed[i])+" seconds"+"\n")
            f.write("Encryption Ratio: "+str(ratios[i])+"\n")
            f.write("-------------------------------\n\n")
        f.close()
        tempRoot = Tk()
        tempRoot.title(choice.get() +" Review")
        f = (fontVar.get(), sizeVar.get(), weightVar.get().lower(), slantVar.get().lower())
        label = Label(tempRoot, font = f, text = "Key Size: " +str(sum(keysizes)/total)+" bytes")
        label.pack()
        label = Label(tempRoot, font = f, text = "Key Generation Time: "+str(sum(keygentimes)/total)+" seconds")
        label.pack()
        label = Label(tempRoot, font = f, text = "Encryption Time: "+str(sum(encryptionspeed)/total)+" seconds")
        label.pack()
        label = Label(tempRoot, font = f, text = "Decryption Time: "+str(sum(decryptionspeed)/total)+" seconds")
        label.pack()
        label = Label(tempRoot, font = f, text = "Encryption Ratio: "+str(sum(ratios)/total))
        label.pack()
        button = Button(tempRoot, font = f, text = "Close", command = lambda tk=tempRoot: closeWindow(tk))
        button.pack()
    scoreButton.config(state = "normal")
    root.update()
    return [sum(keysizes)/total, sum(keygentimes)/total, sum(encryptionspeed)/total, sum(decryptionspeed)/total, sum(ratios)/total]

def closeWindow(tk):
    tk.destroy()

def expandCustom():
    customframe.pack()
    expandMenu.config(text = "Hide Text Customisation", command = hideCustom)

def hideCustom():
    customframe.pack_forget()
    expandMenu.config(text = "Expand Text Customisation", command = expandCustom)

def getChildren(current, node):
    current.append(node)
    for n in node.winfo_children():
        current = getChildren(current, n)
    return current

def customise(*args):
    f = (fontVar.get(), sizeVar.get(), weightVar.get().lower(), slantVar.get().lower())
    for i in getChildren([], root)[1:]:
        if not "frame" in str(i)[len(str(i))-6:]:
            i.config(font = f)

def keyError(msg):
    if msg != "":
        invalid.config(text = "Invalid Key - " + msg)
        invalid.pack()
    else:
        invalid.config(text = "valid")
        invalid.pack_forget()
    root.update()

def handleEmptyKey():
    keyError("key is empty")
    root.after(1000)
    keyError("")


def handleEmptyMessage(msg, entry):
    if entry == "plaintext":
        msgError = plainMsgError
    else:
        msgError = cipherMsgError
    if msg == "":
        msgError.config(text = msgError.cget("text") +entry +" is empty")
        msgError.pack()
        root.update()
        root.after(1000)
        msgError.config(text = "Text Error - ")
        msgError.pack_forget()
        return
    else:
        return msg

def handleInvalidCharacters(entry):
    if entry.edit_modified() == 1:
        if entry == plaintext:
            entryName = "plaintext"
            msgError = plainMsgError
        else:
            entryName = "ciphertext"
            msgError = cipherMsgError
        msg = entry.get("1.0", END).strip()
        validCharacters = textEncryption.full
        if entryName == "ciphertext":
            if choice.get() in ["DES", "Triple DES", "Blowfish"]:
                validCharacters = "0123456789abcdefABCDEF"
            if choice.get() == "RSA":
                validCharacters = textEncryption.base64 + "."
        for c in msg:
            if not c in validCharacters:
                if msgError.cget("text") == "Text Error - ":
                    msgError.config(text = msgError.cget("text") + entryName +" contains invalid character")
                    msgError.pack()
                    entry.edit_modified(False)
                else:
                    entry.edit_modified(False)
                return
        msgError.config(text = "Text Error - ")
        msgError.pack_forget()
        entry.edit_modified(False)
        return 

def handleKeyErrors(*args):
    key = keychoice.get()
    keychoice.config(width = len(str(key))+10)
    if key == "":
        return
    match choice.get():
        case "Caesar Shift":
            try:
                key = int(key)
            except:
                keyError("key must be an integer")
                return
            if key < 1 or key > len(textEncryption.full) - 1:
                keyError("key must be in range 1-" +str(len(textEncryption.full) - 1))
                return
            else:
                keyError("")
        case "Substitution Cipher":
            for c in textEncryption.full:
                if not c in key:
                    keyError("key missing characters")
                    return
            for c in key:
                if not c in textEncryption.full:
                    keyError("key contains invalid characters")
                    return
            if not len(set(key)) == len(key):
                keyError("key contains duplicate characters")
                return
            else:
                keyError("")
        case "Vigenère Cipher":
            for c in key:
                if not c in textEncryption.full:
                    keyError("key contains invalid characters")
                    return
            keyError("")
        case "Rail-Fence Cipher":
            try:
                key = int(key)
            except:
                keyError("key must be an integer")
                return
            if key < 2 or key > 50:
                keyError("key must be in range 2-50")
                return
            else:
                keyError("")
        case "Enigma":
            key = key.split("/")
            for i, section in enumerate(key):
                key[i] = section.split("-")
            if len(key[0]) != 5:
                keyError("incorrect number of rotor postions")
                return
            if len(key[1]) != 5:
                keyError("incorrect number of key settings")
                return
            if len(key[2]) != 5:
                keyError("incorrect number of ring settings")
                return
            if len(set(key[0])) != 5:
                keyError("duplicate rotor positions")
            for i in range(5):
                try:
                    n = int(key[0][i])
                    if n < 1 or n > 8:
                        raise(KeyError)
                except:
                    keyError("invalid rotor positions")
                    return
            for i in range(1,3):
                for j in range(5):
                    if not key[i][j] in textEncryption.full:
                        if i == 1:
                            keyError("invalid key settings")
                            return
                        else:
                            keyError("invalid ring settings")
            used = []
            for pair in key[3]:
                pair = pair.split("<>")
                if len(pair) != 2:
                    keyError("invalid plugboard setting")
                    return
                for l in pair:
                    if not l in textEncryption.full or "" in pair:
                        keyError("invalid character in plugboard settings")
                        return
                    if l in used:
                        keyError("duplicate character in plugboard settings")
                        return
                    used.append(l)
            keyError("")
        case "RSA":
            keyError("")
        case "DES":
            if len(key) != 16:
                keyError("invalid length (must be 16)")
                return
            for c in key:
                if not c in "0123456789abcdefABCDEF":
                    keyError("invalid characters")
                    return
            keyError("")
        case "Triple DES":
            if len(key) != 32:
                keyError("invalid length (must be 16)")
                return
            for c in key:
                if not c in "0123456789abcdefABCDEF":
                    keyError("invalid characters")
                    return
            keyError("")
        case "Blowfish":
            if len(key) != 112:
                keyError("invalid length (must be 112)")
                return
            for c in key:
                if not c in "0123456789abcdefABCDEF":
                    keyError("invalid characters")
                    return
            keyError("")
        case "AES":
            if len(key) != 32:
                keyError("invalid length (must be 32)")
                return
            for c in key:
                if not c in "0123456789abcdefABCDEF":
                    keyError("invalid characters")
                    return
            keyError("")
        
def Encrypt():
    if not "plaintext" in plainMsgError.cget("text"):
        msg = plaintext.get("1.0", END).strip()
        msg = handleEmptyMessage(msg, "plaintext")
        if msg == None:
            return
        key = keychoice.get()
        if key == "":
            handleEmptyKey()
            return
        if invalid.cget("text") != "valid":
            return
        match choice.get():
            case "Caesar Shift":
                newmsg = textEncryption.caesarShift(int(key), msg, "encode")
            case "Substitution Cipher":
                newmsg = textEncryption.substitutionCipher(key, msg, "encode")
            case "Vigenère Cipher":
                newmsg = textEncryption.vigenereCipher(key, msg, "encode")
            case "Rail-Fence Cipher":
                newmsg = textEncryption.railFenceCipher(int(key), msg, "encode")
            case "Enigma":
                newmsg = textEncryption.Enigma(key, msg)
            case "RSA":
                newmsg = textEncryption.RSA(key, msg, "encode")
            case "DES":
                if len(msg) % 32 != 0:
                    msg += " " * (32 - len(msg) % 32)
                newmsg = textEncryption.doDES(key, msg, "encode")
            case "Triple DES":
                if len(msg) % 32 != 0:
                    msg += " " * (32 - len(msg) % 32)
                newmsg = textEncryption.doDES(key, msg, "encode", triple = True)
            case "Blowfish":
                if len(msg) % 32 != 0:
                    msg += " " * (32 - len(msg) % 32)
                newmsg = textEncryption.blowfish(key, msg, "encode")
            case "AES":
                if len(msg) % 64 != 0:
                    msg += " " * (64 - len(msg) % 64)
                newmsg = textEncryption.AES(key, msg, "encode")
            case _:
                print(choice.get())
        ciphertext.delete("1.0", END)
        ciphertext.insert("1.0", newmsg)

def Decrypt():
    if not "ciphertext" in cipherMsgError.cget("text"):
        msg = ciphertext.get("1.0", END).strip()
        msg = handleEmptyMessage(msg, "ciphertext")
        if msg == None:
            return
        key = keychoice.get()
        if key == "":
            handleEmptyKey()
            return
        if invalid.cget("text") != "valid":
            return
        match choice.get():
            case "Caesar Shift":
                newmsg = textEncryption.caesarShift(int(key), msg, "decode")
            case "Substitution Cipher":
                newmsg = textEncryption.substitutionCipher(key, msg, "decode")
            case "Vigenère Cipher":
                newmsg = textEncryption.vigenereCipher(key, msg, "decode")
            case "Rail-Fence Cipher":
                newmsg = textEncryption.railFenceCipher(int(key), msg, "decode")
            case "Enigma":
                newmsg = textEncryption.Enigma(key, msg)
            case "RSA":
                newmsg = textEncryption.RSA(key, msg, "decode")
            case "DES":
                newmsg = textEncryption.doDES(key, msg, "decode")
            case "Triple DES":
                newmsg = textEncryption.doDES(key, msg, "decode", triple = True)
            case "Blowfish":
                newmsg = textEncryption.blowfish(key, msg, "decode")
            case "AES":
                newmsg = textEncryption.AES(key, msg, "decode")
        plaintext.delete("1.0", END)
        plaintext.insert("1.0", newmsg)

def GenerateRandomKey():
    match choice.get():
        case "Caesar Shift":
            key = textEncryption.getRandomCeasarKey()
        case "Substitution Cipher":
            key = textEncryption.getRandomSubKey()
        case "Vigenère Cipher":
            key = textEncryption.getRandomVigKey()
        case "Rail-Fence Cipher":
            key = textEncryption.getRandomRailKey()
        case "Enigma":
            key = textEncryption.getRandomEnigmaKey()
        case "RSA":
            key = textEncryption.getRandomRSAKey()
        case "DES":
            key = textEncryption.getRandomDESKey()
        case "Triple DES":
            key = textEncryption.getRandomDESKey(triple = True)
        case "Blowfish":
            key = textEncryption.getRandomBlowfishKey()
        case "AES":
            key = textEncryption.getRandomAESKey()
    keychoice.delete(0,END)
    keychoice.insert(0, str(key))
    keychoice.config(width = len(str(key))+10)
    
root = Tk()

##----- customisation options
bigframe = Frame()
bigframe.pack()
expandMenu = Button(bigframe, text = "Expand Text Customisation", command = expandCustom)
expandMenu.pack()

customframe = Frame(bigframe, highlightbackground = "light grey", highlightthickness = 1)
label = Label(customframe, text = "Text Customisation ")
label.pack()

fontframe = Frame(customframe)
fontframe.pack()
label = Label(fontframe, text = "Font: ")
label.pack(side = "left")
fonts = ["Courier", "Helvetica", "Segoe UI", "Times", "Wingdings"]
fontVar = StringVar()
fontVar.set("Segoe UI")
fontMenu = OptionMenu(fontframe, fontVar, *fonts)
fontMenu.pack(side = "left")

sizeframe = Frame(customframe)
sizeframe.pack()
label = Label(sizeframe, text = "Size: ")
label.pack(side = "left")
sizes = [1,3,4,5,6,7,8,9,10,11,12]
sizeVar = IntVar()
sizeVar.set(9)
sizeMenu = OptionMenu(sizeframe, sizeVar, *sizes)
sizeMenu.pack(side = "left")

weightframe = Frame(customframe)
weightframe.pack()
label = Label(weightframe, text = "Weight: ")
label.pack(side = "left")
weights = ["Bold", "Normal"]
weightVar = StringVar()
weightVar.set("Normal")
weightMenu = OptionMenu(weightframe, weightVar, *weights)
weightMenu.pack(side = "left")

slantframe = Frame(customframe)
slantframe.pack()
label = Label(slantframe, text = "Slant: ")
label.pack(side = "left")
slants = ["Italic", "#Roman"]
slantVar = StringVar()
slantVar.set("Roman")
weightMenu = OptionMenu(slantframe, slantVar, *slants)
weightMenu.pack(side = "left")

fontVar.trace_add("write", customise)
sizeVar.trace_add("write", customise)
weightVar.trace_add("write", customise)
slantVar.trace_add("write", customise)

choiceframe = Frame()
choiceframe.pack()
label = Label(choiceframe, text = "Encryption Method:")
label.pack(side = "left")
options = ["Caesar Shift", "Substitution Cipher", "Vigenère Cipher", "Rail-Fence Cipher", "Enigma", "RSA", "DES", "Triple DES", "Blowfish", "AES"]
choice = StringVar()
choice.set("Caesar Shift")
drop = OptionMenu(choiceframe, choice, *options)
drop.pack(side = "left")

keyframe = Frame()
keyframe.pack()
label = Label(keyframe, text = "Key: ")
label.pack(side = "left")
keyvalue = StringVar()
keyvalue.trace_add("write", handleKeyErrors)
keychoice = Entry(keyframe, justify = CENTER, textvariable = keyvalue)
keychoice.pack(side = "left")
randomKey = Button(keyframe, text = "Generate Random Key", command = GenerateRandomKey)
randomKey.pack(side = "left")

errorframe = Frame()
errorframe.pack()
invalid = Label(errorframe, text = "Invalid Key - ", fg = "red")

scoreButton = Button(text = "Score Algorithm", command = scoreAlgorithm)
scoreButton.pack()
smallframe = Frame()
smallframe.pack()
delayScale = Scale(smallframe, orient = HORIZONTAL, to = 1000, resolution = 10, length = 200)
delayScale.set(500)
delayScale.pack(side = "left")

analysisButton = Button(text = "Detailed Analysis", command = scoreAllAlgorithms)
analysisButton.pack()

bigframe = Frame()
bigframe.pack()

plainframe = Frame(bigframe)
plainframe.pack(side = "left")
label = Label(plainframe,text = "Plain Text")
label.pack()
plaintext = Text(plainframe, height = 20, width = 80)
plaintext.pack()
plaintext.bind("<<Modified>>", lambda event, entry=plaintext: handleInvalidCharacters(entry))
encrypt = Button(plainframe, text = "Encrypt", command = Encrypt)
encrypt.pack()

cipherframe = Frame(bigframe)
cipherframe.pack(side = "left")
label = Label(cipherframe,text = "Cipher Text")
label.pack()
ciphertext = Text(cipherframe, height = 20, width = 80)
ciphertext.pack()
ciphertext.bind("<<Modified>>", lambda event, entry=ciphertext: handleInvalidCharacters(entry))
decrypt = Button(cipherframe, text = "Decrypt", command = Decrypt)
decrypt.pack()

plainMsgError = Label(text = "Text Error - ", fg = "red")
cipherMsgError = Label(text = "Text Error - ", fg = "red")

root.mainloop()