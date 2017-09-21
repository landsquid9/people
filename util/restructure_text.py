import argparse
import json
import StringIO

def txtToJSON(tp, name, fromFile, toFile):
        f = open(fromFile)
        fList = list(f)
        f.close()
        jsonObj = {}
        jsonObj["type"] = tp
        jsonObj["name"] = name
        jsonObj["list"] = []

        for line in fList:
            jsonObj["list"].append(line)

        jsonStr = json.dumps(jsonObj)

        f = open(toFile, 'w')
        f.write(jsonStr)
        f.close()


def censusNamesToJSON(tp, name, fromFile, toFile):
    f = open(fromFile)
    fList = list(f)
    f.close()
    jsonObj = {}
    jsonObj["type"] = tp
    jsonObj["name"] = name
    jsonObj["list"] = []

    for line in fList:
        lineList = line.split()
        jsonObj["list"].append(lineList[0])

    jsonStr = json.dumps(jsonObj)

    f = open(toFile, 'w')
    f.write(jsonStr)
    f.close()






parser = argparse.ArgumentParser(description="Process files to JSON")
parser.add_argument('filename')
parser.add_argument('data_name')
parser.add_argument('data_type')
parser.add_argument('--census', action = 'store_true')
parser.add_argument('--txt', action = 'store_true')
options = parser.parse_args()
filename = options.filename
census = options.census
txt = options.txt

if filename[-4:] == ".txt":
    print "txt"
    filenameOut = filename[:-4] + ".json"
else:
    filenameOut = filename + ".json"

if census:
    censusNamesToJSON(options.data_type, options.data_name, filename, filenameOut)
elif txt:
    txtToJSON(options.data_type, options.data_name, filename, filenameOut)
