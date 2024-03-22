class VertexModel:
    def __init__(self, vertices):
        self.vertices = dict(enumerate(vertices))
        self.values = dict()
        self.strong = dict()
        for ver in vertices.items():
            self.values[self.getIndexOf(ver[0])] = ver[1]
            self.strong[self.getIndexOf(ver[0])] = False

    def getIndexOf(self, ver):
        for v in self.vertices.items():
            if v[1] == ver:
                return v[0]
    
    def getNameOf(self, index):
        return self.vertices[index]
            
    def getValueWithIndex(self, ver):
        return self.values[ver]
    
    def getValueWithName(self, name):
        ver = self.getIndexOf(name)
        return self.values[ver]
    
    def setStrong(self, name):
        ver = self.getIndexOf(name)
        self.strong[ver] = True

    def getAllStrength(self):
        return self.strong
    
    def getStrengthOf(self, index):
        return self.strong[index]