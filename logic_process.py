import multiprocessing
import custom_logging as logging
import os
import time
import random

import layout
import person
import location

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

        self.pipeWrite.send("Creating places")
        self.numLocations = 4
        self.pipeWrite.send("Setting number of locations to " + str(self.numLocations))
        self.locations = []

        for i in range(self.numLocations):
            logging.add(str(self.namesLoc))
            ranName = self.namesLoc[random.randint(0, len(self.namesLoc)-1)]
            self.pipeWrite.send("Creating " + ranName)
            self.locations.append(location.Location(ranName))


        self.pipeWrite.send("Creating people")
        self.numPpl = 8
        self.pipeWrite.send("Setting number of people to " + str(self.numPpl))
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

            self.pipeWrite.send("Creating " + ranName)
            self.people.append(person.Person(ranName, ranGender, self.locations,
            self.idleActions))

        for p in self.people:
            p.setOthers(self.people)

    def run(self):
        #self.pipeWrite.send("hello")
        while True:
            time.sleep(1)
            for person in self.people:
                msg = person.hourlyUpdate()

                for m in msg:
                    self.pipeWrite.send(m)
                    time.sleep(1)
            #self.pipeWrite.send(str(time.time()))
