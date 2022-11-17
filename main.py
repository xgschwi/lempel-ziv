from sys import argv, stdout
import os
import string
byteSize = os.stat(argv[1]).st_size
inFile = open(argv[1], 'r')
contents = inFile.read()

output = open(argv[1] + '.lwz', 'w')
compFile = None
compContents = ""
decomFile = open('Decompressed-' + argv[1], 'w')

# Dictionary based on Ascii between A to z
def initCodeTable():
    idx = 0
    codeTable = {}
    for c in list(string.ascii_letters):
        codeTable[str(idx)] = c # remember to fully convert to values
        idx += 1
    #print(codeTable)
            
    return idx, codeTable


def compress():
    idx, codeTable = initCodeTable()

    buffer = contents[0]
    for c in contents[1:]:
        #print('Buffer and c: ', buffer, c)
        temp = buffer + c
        if temp in codeTable.values(): # remember to fully convert to values 
            buffer = temp
        else:
            #print('Writing buffer code: ', buffer, str(list(codeTable.values()).index(buffer)))
            output.write(str(list(codeTable.values()).index(buffer)) + ' ')
           # print('Storing: ', temp, idx)
            codeTable[str(idx)] = temp
            idx += 1
            buffer = c

        #print('Buffer is now: ', buffer)
    #print('Writing buffer code', buffer, str(list(codeTable.values()).index(buffer)))
    output.write(str(list(codeTable.values()).index(buffer)))
    #print(codeTable)

def decompress():
    codeTable = {}
    idx, codeTable = initCodeTable()

    listOfContents = compContents.split(' ')

    prior = listOfContents[0]

    s = codeTable[prior]
    temp = ''
    #print(codeTable)
    decoded = ''
    #stdout.write(s)
    decoded += s
    

    for current in listOfContents[1:]:
        #print('Current: ', current)
        #print(current, current in codeTable)
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
    compressedSize = os.stat(argv[1] + '.lwz').st_size
    decompSize = os.stat('Decompressed-' + argv[1]).st_size
    #print("Same After decoding? ", decoded == contents)
    print("Input Filename | # bytes in input file | # bytes in compressed file | # bytes in output file | Matching Files? | Compression Efficiency")
    print(argv[1], '|', byteSize, '|', compressedSize , '|', decompSize, '|', decoded == contents, '|', str(compressedSize/byteSize*100) + '%')
    #s = codeTable.
    #for c in compContents:

    # priorIndex = 0
    # print(prior)
    # current = ""
    # while True:
    #     current = compContents[idx]
    #     idx+= 1
    #     if not current in codeTable.keys():
    #         c = compContents.find(prior, priorIndex)
    #         temp = compContents.find(prior, priorIndex) + c
    #         print(temp)


    

compress()

inFile.close()
output.close()

compFile = open(argv[1] + '.lwz', 'r')
compContents = compFile.read()
compFile.close()

decompress()
