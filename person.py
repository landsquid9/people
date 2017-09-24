import random

import custom_logging as logging

import food
from action_container import ActionContainer


class Person:

    def __init__(self, name, gender, locations, idleActions, knowledge=[]):
        # chances out of 100
        self.EXPLORE_CHANCE = 10

        # life signs
        self.name = name
        self.hunger = 50
        self.energy = 100
        self.mood = 100
        self.dying = False
        self.dyingMeter = 100
        self.dead = False

        # material
        self.food = []
        self.genFood(4)

        self.knowledge = knowledge
        self.globalLocations = locations
        self.knownLocations = [
            self.globalLocations[0], self.globalLocations[1]]

        self.location = self.knownLocations[0]
        self.unknownLocations = self.globalLocations[2:]
        self.others = []
        self.messages = []
        self.gender = gender

        self.idleActions = idleActions

        # ACTION SYSTEM
        # all actions = all actions that it is possible for
        # a person to carry out in any given situation
        # Every action has requirements to be possibly triggered. If
        # an action's requirement is met, it is added to potential actions
        self.allActions = []
        self.potentialActions = []
        self.weightList = []
        self.essentialActions = []
        self.setUpActions()

    def setUpActions(self):
        def eat(p):
            p.message(p.name + " is hungry.")
            if len(p.food) > 0:
                p.hunger += p.food[-1].consume()
                p.message(p.name + " ate a " + p.food[-1].name)
                p.food.pop(-1)
            else:
                p.message(p.name + " has no food.")

        def eat_req(p):
            return p.hunger < 50 and len(p.food) > 0

        def move(p):
            p.location = p.getOtherLocation()
            p.message(p.name + " moved to " + p.location.name)

        def move_req(p):
            return len(p.knownLocations) > 1

        def explore(p):
            r = random.randint(0, 10)
            if r < 5:
                p.message("Out of desperation, " + p.name +
                " started exploring unknown lands")
            else:
                p.message("Out of boredom, " + p.name +
                " started exploring unknown lands")

            r = random.randint(0, 99)
            if r < p.EXPLORE_CHANCE:
                rLoc = random.choice(p.unknownLocations)
                p.message(p.name + " successfully discovered " +
                                rLoc.name + "!")
                p.knownLocations.append(rLoc)
                p.location = p.getOtherLocation()
                p.message(p.name + " moved to " + p.location.name)
                p.unknownLocations.remove(rLoc)
            else:
                p.message(p.name + " found only desolation.")

        def explore_req(p):
            return True

        def converse(p):
            other = random.choice(p.others)
            ran = random.randint(0, 10)
            if ran < 2:
                if len(other.knowledge) > 0:
                    k = random.choice(other.knowledge)
                    p.knowledge.append(k)
                    p.message(p.name + " discovered about " + k)
            p.message(p.name + " talked to " + other.name)

        def converse_req(p):
            return True

        eatAction       = ActionContainer(eat, eat_req, 1, True)
        moveAction      = ActionContainer(move, move_req, 1)
        exploreAction   = ActionContainer(explore, explore_req, 1)
        converseAction  = ActionContainer(converse, converse_req, 3)
        self.allActions.append(eatAction)
        self.allActions.append(moveAction)
        self.allActions.append(exploreAction)
        self.allActions.append(converseAction)



    def setOthers(self, others):
        self.others = others

    def hourlyUpdate(self):
        """ Call each sim phase. Picks random action """
        # clear messages
        self.messages = []

        # hunger etc
        self.updateLifeSigns()

        # random action
        """
        ranAction = randint(0, self.numActions - 1)
        if ranAction == 0 and len(self.knownLocations) > 1:
            # move
            self.move(self.getOtherLocation())
        elif ranAction == 1 and len(self.others) > 0:
            # converse
            ranPerson = randint(0, len(self.others) - 1)
            self.converse(self.others[ranPerson])
        elif ranAction == 2 and len(self.idleActions) > 0:
            logging.add("idle")
            self.idle()
        elif ranAction == 3 and len(self.unknownLocations) > 1:
            self.explore()
        elif ranAction == 4 and self.hunger < 50:
            self.eat()
        """

        self.potentialActions = []
        self.weightList = []
        self.essentialActions = []

        pActionInc = 0
        for a in self.allActions:
            if a.reqFulfilled(self):
                if a.essential:
                    self.essentialActions.append(a)
                else:
                    self.potentialActions.append(a)
                    for i in range(a.weight):
                        self.weightList.append(pActionInc)
                    pActionInc += 1

        if len(self.essentialActions) > 0:
            random.choice(self.essentialActions).executeAction(self)
        elif len(self.potentialActions) > 0:
            weightedNdx = random.choice(self.weightList)
            self.potentialActions[weightedNdx].executeAction(self)


        return self.messages

    def updateLifeSigns(self):
        if self.hunger > 0:
            self.hunger -= 1
        else:
            self.dying = True

        if self.dying:
            if self.dyingMeter > 0:
                self.dyingMeter -= 1
            else:
                self.dead = True

    def genFood(self, numFood):
        for i in range(numFood):
            ranF = random.randint(0, 4)
            if ranF == 0: self.food.append(food.Banana())
            elif ranF == 1: self.food.append(food.Rice())
            elif ranF == 2: self.food.append(food.Bacon())
            elif ranF == 3: self.food.append(food.Waffle())
            elif ranF == 4: self.food.append(food.Pineapple())








    def message(self, s):
        self.messages.append(s)

    def idle(self):
        self.message(self.name + " " + random.choice(self.idleActions))

    def getOtherLocation(self):
        otherL = []
        for l in self.knownLocations:
            if l != self.location:
                otherL.append(l)

        return random.choice(otherL)
