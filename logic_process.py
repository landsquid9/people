import multiprocessing
import custom_logging as logging
import os
import time
import random

import layout
import person
import location
from data_transfer import DATA_TYPES

class LogicProcess(multiprocessing.Process):

    def __init__(self,pipe, namesM, namesF, namesL, namesLoc, idleActions):
        multiprocessing.Process.__init__(self)
        self.pipeWrite = pipe
        self.namesM = namesM
        self.namesF = namesF
        self.namesL = namesL
        self.namesLoc = namesLoc
        self.idleActions = idleActions

        logging.add("Intiating Logic Process")

        self.message = {}
        self.message["type"] = DATA_TYPES["log"]
        self.message["payload"] = "Creating places"
        self.pipeWrite.send(self.message)

        self.numLocations = 4

        self.message = {}
        self.message["type"] = DATA_TYPES["log"]
        self.message["payload"] = "Setting number of locations to " + str(self.numLocations)
        self.pipeWrite.send(self.message)

        self.locations = []

        for i in range(self.numLocations):
            logging.add(str(self.namesLoc))
            ranName = self.namesLoc[random.randint(0, len(self.namesLoc)-1)]
            self.message = {}
            self.message["type"] = DATA_TYPES["log"]
            self.message["payload"] = "Creating " + ranName
            self.pipeWrite.send(self.message)
            self.locations.append(location.Location(ranName))

        self.message = {}
        self.message["type"] = DATA_TYPES["log"]
        self.message["payload"] = "Creating people"
        self.pipeWrite.send(self.message)
        self.numPpl = 8
        self.message = {}
        self.message["type"] = DATA_TYPES["log"]
        self.message["payload"] = "Setting number of people to " + str(self.numPpl)
        self.pipeWrite.send(self.message)
        self.people = []

        for i in range(self.numPpl):
            ranG = random.randint(0, 2)
            if ranG == 0:
                ranGender = "male"
                ranName = namesM[random.randint(0,
                len(namesM)-1)] + " " + namesL[random.randint(0, len(namesL)-1)]
            else:
                ranGender = "female"
                ranName = namesF[random.randint(0,
                len(namesF)-1)] + " " + namesL[random.randint(0, len(namesL)-1)]

            self.message = {}
            self.message["type"] = DATA_TYPES["log"]
            self.message["payload"] = "Creating " + ranName
            self.pipeWrite.send(self.message)
            self.people.append(person.Person(ranName, ranGender, self.locations,
            self.idleActions))

        for p in self.people:
            p.setOthers(self.people)

        self.highlightTimerStart = 0
        self.highlightTimerMax = 4

        # To visualise, data must be sent to urwid running in separate
        # process. Data is sent in a map
        self.message = {}

    def run(self):
        while True:
            for person in self.people:

                # PEOPLE LOG
                msg = person.hourlyUpdate()
                for m in msg:
                    self.message = {}
                    self.message["type"] = DATA_TYPES["log"]
                    self.message["payload"] = m
                    self.pipeWrite.send(self.message)
                    time.sleep(0.25)

                    if time.time() - self.highlightTimerStart > self.highlightTimerMax:
                        # HIGHLIGHT
                        self.message = {}
                        self.message["type"] = DATA_TYPES["highlight"]
                        self.message["payload"] = m
                        self.pipeWrite.send(self.message)

                        # INFO
                        # name location hunger food
                        self.message = {}
                        self.message["type"] = DATA_TYPES["info"]
                        personInfo = {"name":person.name,
                                      "location":person.location.name,
                                      "hunger":str(person.hunger),
                                      "food":str(person.food)}
                        self.message["payload"] = personInfo
                        self.pipeWrite.send(self.message)

                        self.highlightTimerStart = time.time()
