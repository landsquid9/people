""" A Simulation of an Island """
import os
from random import randint
import custom_logging as logging
import time
import multiprocessing

import urwid

import load_data as ld
import logic_process
import layout

logging.setup()

projectFolder = os.environ["PYTHON_SIM_DIR"]

""" DATA """
# Male First names
firstNamesM = []
# Female First names
firstNamesF = []
# Family names
familyNames = []
# Town names
placeNames = []
#folders
dataFolder = "/data/"


# load data
ld.loadFile(projectFolder + dataFolder + "first_names_male.txt",
                   firstNamesM)
ld.loadFile(projectFolder + dataFolder + "first_names_female.txt",
                   firstNamesF)
ld.loadFile(projectFolder + dataFolder + "family_names.txt",
                   familyNames)
ld.loadFile(projectFolder + dataFolder + "place_names.txt",
                   placeNames)

(c1, c2) = multiprocessing.Pipe()

log = layout.Log(c2)

logicProcess = logic_process.LogicProcess(c1, firstNamesF, firstNamesM,
                                            familyNames, placeNames)

logicProcess.start()
log.start()

while True:
    if not log.draw():
        break
log.stop()
logicProcess.terminate()
