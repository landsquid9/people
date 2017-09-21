import custom_logging as logging

from time import sleep
import json

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

def loadJSON(fileName, stringVar):
    logging.add("Opening JSON " + fileName)
    f = open(fileName)
    obj = json.loads(f.read())
    for st in obj['list']:
        st = st.strip()
        if obj['type'] == 'names':
            st = st.lower()
            st = st.capitalize()
        stringVar.append(st)
