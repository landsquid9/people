from item import Item

class Food(Item):

    def __init__(self):

        self.nutrition = 30
        self.weight = 1
        self.name = "food"

    def consume(self):
        return self.nutrition

class Banana(Food):
    def __init__(self):
        self.nutrition = 30
        self.name = "banana"

class Rice(Food):
    def __init__(self):
        self.nutrition = 10
        self.name = "rice"

class Bacon(Food):
    def __init__(self):
        self.nutrition = 40
        self.name = "bacon"

class Pineapple(Food):
    def __init__(self):
        self.nutrition = 20
        self.name = "pineapple"

class Waffle(Food):
    def __init__(self):
        self.nutrition = 15
        self.name = "waffle"
