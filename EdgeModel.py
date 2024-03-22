class EdgeModel:
    def __init__(self, edge):
        s = sorted(edge["vertices"])
        self.v1 = s[0]
        self.v2 = s[1]
        self.value = edge["value"]
        self.strong = False

    def isEdge(self, v1, v2):
        return (self.v1 == v1 and self.v2 == v2) or (self.v1 == v2 and self.v2 == v1)
    
    def getValue(self):
        return self.value
    
    def getFirstVertex(self):
        return self.v1
    
    def getSecondVertex(self):
        return self.v2
    
    def setStrong(self):
        self.strong = True

    def getStrength(self):
        return self.strong