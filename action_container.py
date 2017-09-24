import custom_logging as logging
class ActionContainer:
    def __init__(self, action, req, weight, essential=False):
        self.action = action
        self.req = req
        self.weight = weight
        self.essential = essential

    def reqFulfilled(self, person):
        logging.add(person.name + " " + str(person.food))
        return self.req(person)

    def executeAction(self, person):
        self.action(person)
