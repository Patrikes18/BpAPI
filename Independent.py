"""
    Trieda predstavujúca nezávislé množiny.

    Atribúty:
    ---------
    vertices : VertexModel
        trieda vrcholov
    edges : list(EdgeModel, ...)
        zoznam hrán
    independent : set()
        množina nezávislých množín
    maxindependent : []
        zoznam najväčších nezávislých množín

    Metódy:
    -------
    findStrongEdges()
        hľadá silne susediace vrcholy
    isSafeForIndependentSet(vertex, tempSolutionSet)
        pomocná metóda pri hľadaní nezávislých množín
    findIdependentSets(vertexnumber = 1)
        rekurzívne hľadá nezávislé množiny
    findAllMaximalSets()
        zo zoznamu nezávilých množín vracia tie najväčšie nezávislé množiny
"""

import VertexModel

class IndependentSet:
    def __init__(self, vertices : VertexModel, edges : list):
        """
            Konštruktor.

            Parametre:
            ----------
            vertices : VertexModel
                Trieda, ktorá má v sebe uložené vrcholy.
            edges : list(EdgeModel, ...)
                Zoznam hrán
        """
        self.vertices = vertices
        self.edges = edges
        self.tmpindependent = set()
        self.independent = set()
        self.maxindependent = []

    def findStrongEdges(self):
        """
            Metóda, ktorá hľadá silne susediace vrcholy.
        """
        for edge in self.edges:
            # Kontrola váhy hrany na základe vzťahu: min(váha prvého vrcholu, váha druhého vrcholu)/2 <= váha hrany
            if min(self.vertices.getValueWithName(edge.getFirstVertex()), self.vertices.getValueWithName(edge.getSecondVertex())) / 2 <= edge.getValue(): # Ide o silne susediace vrcholy
                edge.setStrong()
                self.vertices.setStrong(edge.getFirstVertex())
                self.vertices.setStrong(edge.getSecondVertex())
    
    def isSafeForIndependentSet(self, vertex : int, tempSolutionSet : set) -> bool:
        """
            Metóda, ktorá určuje, či se vrchol bezpečný pre nezávislú množinu. Prevziate a upravené z https://www.geeksforgeeks.org/maximal-independent-set-from-a-given-graph-using-backtracking/

            Parametre:
            ----------
            vertex : int
                Index testovaného vrcholu.
            tempSolutionSet : set()
                Nezávislá množina, na ktorej vrchol testujeme.

            Návratové hodnoty:
            ------------------
            True, ak je vrchol bezpečný pre vloženie do nezávislej množiny, inak False.
        """
        if self.vertices.getStrengthOf(vertex): # Vrchol je silný.
            for itr in tempSolutionSet: # Prechádzame nezávislú množinu a skúšame všetky jej vrcholy.
                for edge in self.edges: # Prechádzame všetky hrany grafu.
                    if edge.getStrength() and edge.isEdge(self.vertices.getNameOf(itr), self.vertices.getNameOf(vertex)):
                        # Hrana je medzi silne susediacimi vrcholmi a druhý vrchol je už v nezávislej množine.
                        return False
            return True
        else:
            return False
    
    def findIdependentSets(self, vertexnumber = 1):
        """
            Metóda, ktorá rekurzívne hľadá nezávislé množiny. Prevziate a upravené z https://www.geeksforgeeks.org/maximal-independent-set-from-a-given-graph-using-backtracking/

            Parametre:
            ----------
            vertexnumber : int
                Index skúmaného vrcholu. V základe je skúmaný vrchol na indexe 1.
        """
        for i in range(vertexnumber, len(self.vertices.getAllStrength()) + 1): # Prechádzame všetky vrcholy grafu.
            if (self.isSafeForIndependentSet(i - 1, self.tmpindependent)) : # Kontrola bezpečnosti daného vrcholu.
                # Backtracking
                self.tmpindependent.add(i - 1)
                self.findIdependentSets(i + 1) # Rekurzia.
                self.tmpindependent.remove(i - 1)
            
        self.independent.add(frozenset(self.tmpindependent)) # Pridanie nezávislej množiny do množiny.
    
    def findAllMaximalSets(self) -> list:
        """
            Metóda, ktorá zo zoznamu nezávilých množín vracia tie najväčšie nezávislé množiny.

            Návratové hodnoty:
            ------------------
            Zoznam najväčších nezávislých množín.
        """
        enumeratedset = dict(enumerate(self.independent)) # Pomocný slovník typu {index : nezávislá množina}
        val = dict() # Pomocný slovník, ktorý určuje podmnožiny, ktoré môžeme odstrániť.
        for i in range(0, len(self.independent)): # Prechádzanie zoznamu nezávislých množín z ľava do prava.
            for j in range(i+1, len(self.independent)):
                set1 = enumeratedset[i]
                set2 = enumeratedset[j]
                if set1.issubset(set2): # Množina je podmnožinou.
                    val[i] = set1
                elif set1 == frozenset(): # Prazdna množina je podmnožinou všetkých množín
                    val[i] = frozenset()

        for i in range(len(self.independent)-1, 0, -1): # Prechádzanie zoznamu nezávislých množín z prava do ľava.
            for j in range(i-1, -1, -1):
                set1 = enumeratedset[i]
                set2 = enumeratedset[j]
                if set1.issubset(set2): # Množina je podmnožinou.
                    val[i] = set1
                elif set1 == frozenset(): # Prazdna množina je podmnožinou všetkých množín
                    val[i] = frozenset()

        for i in val: # Odstránenie podmnožín
            enumeratedset.pop(i)
        
        for a in enumeratedset: # Vytvorenie zoznamu najväčších nezávislých množín
            self.maxindependent.append(enumeratedset[a])
        return self.maxindependent