from sys import argv
import os

byteSize = os.stat(argv[1]).st_size
inFile = open(argv[1], 'r')
contents = inFile.read()

output = open(argv[1] + '.lwz', 'w')
codeTable = {}
compFile = None
compContents = ""

def initCodeTable(fileContents):
    idx = 0
    for c in fileContents:
        if not c in codeTable.keys():
            codeTable[c] = idx
            idx += 1
    return idx


def compress():
    idx = initCodeTable(contents)

    buffer = contents[0]
    for c in contents[1:]:
        #print('Buffer and c: ', buffer, c)
        temp = buffer + c
        if temp in codeTable.keys():
            buffer = temp
        else:
           # print('Writing buffer code: ', buffer)
            output.write(str(codeTable[buffer]))
           # print('Storing: ', temp)
            codeTable[temp] = idx
            idx += 1
            buffer = c

        #print('Buffer is now: ', buffer)

    output.write(str(codeTable[buffer]))
    #print(codeTable)

def decompress():
    initCodeTable(compContents)
    idx = 1
    prior = compContents[0]
    priorIndex = 0
    print(prior)
    current = ""
    while True:
        current = compContents[idx]
        idx+= 1
        if not current in codeTable.keys():
            c = compContents.find(prior, priorIndex)
            temp = compContents.find(prior, priorIndex) + c
            print(temp)


    

compress()

inFile.close()
output.close()

compFile = open(argv[1] + '.lwz')
compContents = compFile.read()

codeTable = {}
decompress()
compFile.close()