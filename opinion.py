""" Class: Opinion
    This is used to track a persons opinion of others
    It holds a list of all other people
    and a history of their interactions
    Also how those interactions affected their relationship
"""

class Opinions
{
    MIN_RELATION = 0;
    MAX_RELATION = 100;
    def __init__(self, lsOfPeople):

        self.l_ppl = l_people # list of obj ref
        self.d_rating = {}
        for p in d_people:
            # go through each other person and
            # create default opinion rating
            self.rating[p.id] = 50 # 0 - 100
        self.history = []

    def addEvent(self, otherID, mod, event):
        # mode is number. pos increases relations and neg decreases.
        self.rating[otherID] = self.rating[otherID]  + mod
        self.rating[otherID] = min(self.rating[otherID], MAX_RELATION)
        self.rating[otherID] = max(self.rating[otherID], MIN_RELATION)
        self.history.append(event)
}
