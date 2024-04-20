class IndependentSet:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.tmpindependent = set()
        self.independent = set()
        self.maxindependent = []

    def findStrongEdges(self):
        for edge in self.edges:
            if min(self.vertices.getValueWithName(edge.getFirstVertex()), self.vertices.getValueWithName(edge.getSecondVertex())) / 2 <= edge.getValue():
                edge.setStrong()
                self.vertices.setStrong(edge.getFirstVertex())
                self.vertices.setStrong(edge.getSecondVertex())
    
    def isSafeForIndependentSet(self, vertex, tempSolutionSet):
        if self.vertices.getStrengthOf(vertex):
            for itr in tempSolutionSet:
                for edge in self.edges:
                    if edge.getStrength() and edge.isEdge(self.vertices.getNameOf(itr), self.vertices.getNameOf(vertex)):
                        return False
            return True
        else:
            return False
    
    def findIdependentSets(self, vertexnumber = 1):
        #https://www.geeksforgeeks.org/maximal-independent-set-from-a-given-graph-using-backtracking/
        for i in range(vertexnumber, len(self.vertices.getAllStrength()) + 1):
            if (self.isSafeForIndependentSet(i - 1, self.tmpindependent)) :
                self.tmpindependent.add(i - 1)
                self.findIdependentSets(i + 1)
                self.tmpindependent.remove(i - 1)
            
        self.independent.add(frozenset(self.tmpindependent))
        return
    
    def findAllMaximalSets(self):
        enumeratedset = dict(enumerate(self.independent))
        val = dict()
        for i in range(0, len(self.independent)):
            for j in range(i+1, len(self.independent)):
                set1 = enumeratedset[i]
                set2 = enumeratedset[j]
                if set1.issubset(set2):
                    val[i] = set1
                elif set1 == frozenset():
                    val[i] = frozenset()

        for i in range(len(self.independent)-1, 0, -1):
            for j in range(i-1, -1, -1):
                set1 = enumeratedset[i]
                set2 = enumeratedset[j]
                if set1.issubset(set2):
                    val[i] = set1
                elif set1 == frozenset():
                    val[i] = frozenset()

        for i in val:
            enumeratedset.pop(i)
        
        for a in enumeratedset:
            self.maxindependent.append(enumeratedset[a])
        return self.maxindependent