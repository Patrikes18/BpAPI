class IndependentSet:
    def __init__(self, vertices):
        edges = [{'vertices': ['a', 'b'], 'value': 0}, {'vertices': ['a', 'f'], 'value': 0}, {'vertices': ['b', 'c'], 'value': 0}, {'vertices': ['b', 'd'], 'value': 0}, {'vertices': ['d', 'e'], 'value': 0}, {'vertices': ['e', 'f'], 'value': 0}]
        self.vertices = dict(enumerate(vertices))
        self.independent = set()
        self.maxindependent = []
        self.edgelist = []
        self.temp = set()
        for edge in edges:
            index1 = self.getIndexOf(edge["vertices"][0])
            index2 = self.getIndexOf(edge["vertices"][1])
            val = (index1, index2)
            self.edgelist.append(val)


    def getIndexOf(self, ver):
        for v in self.vertices.items():
            if v[1] == ver:
                return v[0]

    def isSafeForIndependentSet(self, vertex, tempSolutionSet):
        for itr in tempSolutionSet:
            if (itr, vertex) in self.edgelist:
                return False
        return True
    
    def findIdependentSets(self, vertexnumber = 1):
        for i in range(vertexnumber, len(self.vertices) + 1):
            if (self.isSafeForIndependentSet(i - 1, self.temp)) :
                self.temp.add(i - 1)
                self.findIdependentSets(i + 1)
                self.temp.remove(i - 1)
            
        self.independent.add(frozenset(self.temp))
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
        # print(self.maxindependent)
        return self.maxindependent
    
    def printAllIndependentSets(self):
        for itr in self.independent:
            print("{",end=" ")
            for itr2 in itr:
                print(itr2,end= " ")
            
            print("}",end='')
        
        print()
    
if __name__ == '__main__':
    vertices = ["a", "b", "c", "d", "e", "f"]
    I1 = IndependentSet(vertices)
    I1.findIdependentSets()
    # I1.printAllIndependentSets()
    print(I1.findAllMaximalSets())