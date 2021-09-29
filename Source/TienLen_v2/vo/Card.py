# from _typeshed import Self


class Card:
    id = 0
    N = 0
    S = 0
    
    def __init__(self, id):
        self.id = id
        self.N = (id - 1)%13 + 1
        self.S = (id - 1) // 13 + 1
        pass

    def getN(self):
        return self.N
        
    def getS(self):
        return self.S

    def getId(self):
        return self.id

