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
# Idle Actions
idleActions = []
#folders
dataFolder = "/data/"
jsonFolder = dataFolder + "json/";


# load data
ld.loadJSON(projectFolder + jsonFolder + "first_names_male.json",
                   firstNamesM)
ld.loadJSON(projectFolder + jsonFolder + "first_names_female.json",
                   firstNamesF)
ld.loadJSON(projectFolder + jsonFolder + "family_names.json",
                   familyNames)
ld.loadJSON(projectFolder + jsonFolder + "place_names.json",
                   placeNames)
ld.loadJSON(projectFolder + jsonFolder + "idle_actions.json",
                    idleActions)

(c1, c2) = multiprocessing.Pipe()

log = layout.Log(c2)

logicProcess = logic_process.LogicProcess(c1, firstNamesF, firstNamesM,
                                            familyNames, placeNames, idleActions)

logicProcess.start()
log.start()

while True:
    if not log.draw():
        break
log.stop()
logicProcess.terminate()
