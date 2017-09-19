import custom_logging as logging

from time import sleep

def loadFile(fileName, stringVar):
    logging.add("Opening " + fileName)
    f = open(fileName)
    fList = list(f)
    i = 0
    tp = fList[i].strip()
    logging.add(tp)
    i += 1
    while i < len(fList):
        line = fList[i].strip()
        if line != "": 
            if tp == "type-names":
                lineList = line.split(" ")
                line = lineList[0]
                line.lower()
                line.capitalize()
            stringVar.append(line)
        i+=1
