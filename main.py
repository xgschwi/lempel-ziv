from sys import argv
import os
import string
from texttable import Texttable
t = Texttable()

byteSize = 0
inFile = None
contents = ""

output = None
compFile = None
compContents = ""
decomFile = None

# Dictionary based on Ascii between A to z
def initCodeTable():
    idx = 0
    codeTable = {}

    # Accepts only Ascii letters in dictionary
    for c in list(string.ascii_letters):
        codeTable[str(idx)] = c
        idx += 1
            
    return idx, codeTable


def compress():
    idx, codeTable = initCodeTable()

    buffer = contents[0]
    for c in contents[1:]:
        temp = buffer + c
        if temp in codeTable.values():
            buffer = temp
        else:
            output.write(str(list(codeTable.values()).index(buffer)) + ' ')
            codeTable[str(idx)] = temp
            idx += 1
            buffer = c

    output.write(str(list(codeTable.values()).index(buffer)))

def decompress(file):
    codeTable = {}
    idx, codeTable = initCodeTable()

    listOfContents = compContents.split(' ')

    prior = listOfContents[0]

    s = codeTable[prior]
    temp = ''
    decoded = '' # Replaces print steps of algorithm

    #stdout.write(s)
    decoded += s
    

    for current in listOfContents[1:]:
        if not current in codeTable:
            c = codeTable[prior][0]
            temp = codeTable[prior] + c
            codeTable[str(idx)] = temp
            idx += 1
            #stdout.write(temp)
            decoded += temp
        else:
            c = codeTable[current][0]
            temp = codeTable[prior] + c
            codeTable[str(idx)] = temp
            idx += 1
            #stdout.write(codeTable[current])
            decoded += codeTable[current]

        prior = current
        
    decomFile.write(decoded)

    decomFile.close()
    compressedSize = os.stat(file + '.lwz').st_size
    decompSize = os.stat('Decompressed-' + file).st_size
   
    status = 'yes' if decoded == contents else 'no'
    t.add_row([file, byteSize, compressedSize , decompSize, status, str(round(compressedSize/byteSize*100, 4)) + '%'])



t.add_row(['Input Filename', '# bytes in input file', '# bytes in compressed file', '# bytes in output file', 'Matching Files?', 'Compression Efficiency'])

for file in argv[1:]:

    byteSize = os.stat(file).st_size
    inFile = open(file, 'r') 
    contents = inFile.read()

    output = open(file + '.lwz', 'w')
    decomFile = open('Decompressed-' + file, 'w')

    compress()

    inFile.close()
    output.close()

    compFile = open(file + '.lwz', 'r')
    compContents = compFile.read()
    compFile.close()

    decompress(file)
    
print(t.draw())
