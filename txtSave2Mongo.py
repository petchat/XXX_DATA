__author__ = 'jiusi'

def getDataFromFile(txtPath):
    with open(txtPath, 'r') as f:
        for l in f.readlines():
            print l
    return 'fuck'






