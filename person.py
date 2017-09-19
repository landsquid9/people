import random

class Person:

    def __init__(self, name, gender, locations, knowledge=[]):
        self.name = name
        self.hunger = 100
        self.energy = 100
        self.mood = 100
        self.knowledge = knowledge
        self.potentialLocations = locations
        self.location = self.potentialLocations[0]
        self.others = []
        self.numActions = 2
        self.messages = []
        self.gender = gender

    def setOthers(self, others):
        self.others = others


    def hourlyUpdate(self):

        """ Call each sim phase. Picks random action """
        # clear messages
        self.messages = []

        # random action
        ranAction = random.randint(0, self.numActions-1)
        if ranAction == 0 and len(self.potentialLocations) > 0:
            # move
            ranLoc = random.randint(0, len(self.potentialLocations)-1)
            self.move(self.potentialLocations[ranLoc])
        elif ranAction == 1 and len(self.others) > 0:
            # converse
            ranPerson = random.randint(0, len(self.others)-1)
            self.converse(self.others[ranPerson])

        return self.messages


    def move(self, location):
        self.location = location
        self.message(self.name + " moved to " + self.location.name)

    def converse(self, other):
        ran = random.randint(0, 10)
        if ran < 2:
            if len(other.knowledge) > 0:
                ranK = random.randint(0, len(other.knowledge)-1)
                k = other.knowledge(ranK)
                self.knowledge.append(k)
                self.message(self.name + " discovered about " + k)
        return self.message(self.name + " talked to " + other.name)

    def message(self, s):
        self.messages.append(s)
