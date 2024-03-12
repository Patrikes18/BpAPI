# Python3 Program to print the
# independent sets and
# maximal independent sets
# of the given graph
 
# To store all the independent
# sets of the graph
independentSets=set()
 
# To store all maximal independent
# sets in the graph
maximalIndependentSets=set()
 
edges=dict()
vertices=[]
 
# Function to print all independent sets
def printAllIndependentSets():
    for itr in independentSets:
        print("{",end=" ")
        for itr2 in itr:
            print(itr2,end= " ")
         
        print("}",end='')
     
    print()
 
 
# Function to extract all
# maximal independent sets
def printMaximalIndependentSets():
    maxCount = 0;localCount = 0
    for itr in independentSets:
        localCount = 0
        for itr2 in itr:
            localCount+=1
         
        if (localCount > maxCount):
            maxCount = localCount
     
    for itr in independentSets:
 
        localCount = 0
        tempMaximalSet=set()
 
        for itr2 in itr:
            localCount+=1
            tempMaximalSet.add(itr2)
         
        if (localCount == maxCount):
            maximalIndependentSets.add(frozenset(tempMaximalSet))
     
    for itr in maximalIndependentSets :
        print("{",end=" ")
        for itr2 in itr:
            print(itr2,end=" ")
         
        print("}",end="")
     
    print()
 
 
# Function to check if a
# node is safe node.
def isSafeForIndependentSet(vertex, tempSolutionSet):
    for itr in tempSolutionSet:
        if (itr, vertex) in edges:
            return False
 
    return True
 
 
# Recursive function to find
# all independent sets
def findAllIndependentSets(currV, setSize, tempSolutionSet):
    for i in range(currV,setSize+1):
        if (isSafeForIndependentSet(vertices[i - 1], tempSolutionSet)) :
            tempSolutionSet.add(vertices[i - 1])
            findAllIndependentSets(i + 1, setSize, tempSolutionSet)
            tempSolutionSet.remove(vertices[i - 1])
         
    independentSets.add(frozenset(tempSolutionSet))

 
# Driver Program
if __name__ == '__main__':
    V = 6; E = 6
 
    for i in range(V):
        vertices.append(i)
    # print(vertices)

    inputEdges=[(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (5, 0)]
 
    for i in range(E):
        edges[inputEdges[i]]=True
        edges[(inputEdges[i][1],inputEdges[i][0])]=True
    
    # print(edges)
 
    tempSolutionSet=set()
 
    findAllIndependentSets(1, V, tempSolutionSet)
 
    printAllIndependentSets()
 
    # printMaximalIndependentSets()