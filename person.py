from random import randint

import custom_logging as logging

class Person:

    def __init__(self, name, gender, locations, idleActions,knowledge=[]):
        # chances out of 100
        self.EXPLORE_CHANCE = 10
        self.name = name
        self.hunger = 100
        self.energy = 100
        self.mood = 100
        self.knowledge = knowledge
        self.globalLocations = locations
        self.knownLocations = [self.globalLocations[0], self.globalLocations[1]]
        self.location = self.knownLocations[0]
        self.unknownLocations = self.globalLocations[2:]
        self.others = []
        self.numActions = 4
        self.messages = []
        self.gender = gender
        self.idleActions = idleActions

    def setOthers(self, others):
        self.others = others


    def hourlyUpdate(self):

        """ Call each sim phase. Picks random action """
        # clear messages
        self.messages = []

        # random action
        ranAction = randint(0, self.numActions-1)
        if ranAction == 0 and len(self.knownLocations) > 1:
            # move
            self.move(self.getOtherLocation())
        elif ranAction == 1 and len(self.others) > 0:
            # converse
            ranPerson = randint(0, len(self.others)-1)
            self.converse(self.others[ranPerson])
        elif ranAction == 2 and len(self.idleActions) > 0:
            logging.add("idle")
            self.idle()
        elif ranAction == 3 and len(self.unknownLocations) > 1:
            self.explore()

        return self.messages

    def explore(self):
        self.message(self.name + """ is curious and has started exploring
                                        unknown lands """)
        r = randint(0, 99)
        if r < self.EXPLORE_CHANCE:
            rLoc = randint(0, len(self.unknownLocations)-1)
            self.message(self.name + " successfully discovered " +
                            self.unknownLocations[rLoc].name + "!")
            self.knownLocations.append(self.unknownLocations[rLoc])
            self.move(self.unknownLocations[rLoc])
            self.unknownLocations.pop(rLoc)
        else:
            self.message(self.name + " found only desolation.")



    def move(self, location):
        self.location = location
        self.message(self.name + " moved to " + self.location.name)

    def converse(self, other):
        ran = randint(0, 10)
        if ran < 2:
            if len(other.knowledge) > 0:
                ranK = randint(0, len(other.knowledge)-1)
                k = other.knowledge(ranK)
                self.knowledge.append(k)
                self.message(self.name + " discovered about " + k)
        self.message(self.name + " talked to " + other.name)

    def message(self, s):
        self.messages.append(s)

    def idle(self):
        ranN = randint(0, len(self.idleActions)-1)
        self.message(self.name + " " + self.idleActions[ranN])

    def getOtherLocation(self):
        lNum = []
        for i in range(0, len(self.knownLocations)):
            if self.knownLocations[i] != self.location:
                lNum.append(i)

        r = randint(0, len(lNum) - 1)
        return self.knownLocations[lNum[r]]
