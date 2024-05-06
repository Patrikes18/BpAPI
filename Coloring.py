"""
    Trieda implementujúca farbenie fuzzy grafu.

    Atribúty:
    ---------
    vertices : VertexModel
        trieda vrcholov
    edges : list(EdgeModel, ...)
        zoznam hrán
    independentsets : set()
        množina nezávislých množín
    Cb : []
        koeficienty vektoru riešenia
    R : []
        výsledné váhy nezávislých množín
    Base : []
        premenné, ktoré tvoria vektor riešenia
    colors : []
        zoznam farieb
    colorstring : []
        zoznam farebných reťazcov
    weights : []
        zoznam nových váh jednotlivých farieb pre nezávislé množiny

    Metódy:
    -------
    makeColors()
        vytvorí farby pre každú nezávislú množinu
    RGBtoHEX(rgb)
        pomocná funkcia pre vytvorenie farby
    computeWeight()
        prepočítava váhy farieb
    computeWeightFor(vertex)
        pomocná funkcia pre prepočítanie váh farieb pre daný vrchol
    createColorString()
        vytvára farebný reťazec
"""

import distinctipy
import sys
import LPP
import VertexModel


class Coloring:
    def __init__(self, vertices : VertexModel, edges : list, independentsets : list, linprog : LPP):
        """
            Konštruktor.

            Parametre:
            ----------
            vertices : VertexModel
                Trieda s vrcholmi fuzzy grafu.
            edges : list(EdgeModel, ...)
                Zoznam hrán.
            independentsets : list(frozenset())
                Zoznam nezávislých množín.
            linprog : LPP
                Trieda lineárneho programovania.
        """
        self.Cb = linprog.Cb.copy()
        self.Base = linprog.Base.copy()
        self.R = linprog.R.copy()
        li = [list(x) for x in independentsets]
        li.sort()
        self.independentsets = li
        self.vertices = vertices
        self.edges = edges
        self.colors = []
        self.colorstring = [""] * len(self.vertices.getAllVertices())
        self.makeColors()

    def makeColors(self):
        """
            Metóda, ktorá vytvorí farby pre nezávislé množiny.
        """
        for color in distinctipy.get_colors(len(self.independentsets)):
            self.colors.append(self.RGBtoHEX(color))

    def RGBtoHEX(self, rgb: tuple[float, float, float]) -> str:
        """
            Metóda, ktorá premení farby vytvorené knižnicou distinctipy na ich hexadecimálne hodnoty.

            Parametre:
            ----------
            rgb : tuple[float, float, float]
                Farba od distinctipy.
            
            Návratové hodnoty:
            ------------------
                reťazec reprezentujúci farbu
        """
        rgb = tuple([int(255*a) for a in rgb])
        return '#%02x%02x%02x' % rgb

    def computeWeight(self):
        """
            Metóda, ktorá prepočítava váhy farieb.
        """
        # Odstránenie nedbytočných premenných zo stĺpca Base a úprava stĺpcov R a Cb.
        remove = []
        for i in range(len(self.Base)):
            if self.Base[i] >= len(self.independentsets):
                remove.append(i)
        
        remove.sort(reverse=True)

        for i in remove:
            self.Base.pop(i)
            self.R.pop(i)
            self.Cb.pop(i)
        
        vertices = dict()
        for i in self.vertices.getAllVertices():
            vertices[i] = []

        for i in range(len(self.independentsets)): # Priradenie farieb silne susediacim vrcholom podľa nezávislých množín.
            for j in range(len(self.independentsets[i])):
                vertices[self.independentsets[i][j]].append(self.colors[i])
        
        self.weights = []
        for vertexindex in range(len(vertices)): # Prepočítanie váh farieb.
            self.weights.append(self.computeWeightFor(vertices[vertexindex]))

    def computeWeightFor(self, vertex : list) -> list:
        """
            Metóda, ktorá prepočíta váhy fariev danému vrcholu.

            Parametre:
            ----------
            vertex : list()
                Zoznam farieb pre vrchol.

            Návratová hodnoty:
            ------------------
            Zoznam farieb a váh daného vrchola.
        """
        sum = 0
        for i in vertex:
            index = self.colors.index(i)
            Rindex = self.Base.index(index)
            sum += self.R[Rindex]

        val = []
        for i in vertex:
            index = self.colors.index(i)
            Rindex = self.Base.index(index)
            tmp = (1 / sum) * self.R[Rindex]
            if tmp > 0.0:
                val.append([round(tmp,3), i])
        return val

    def createColorString(self) -> list:
        """
            Metóda, ktorá vytvára farebný reťazec na vyfarbenie.

            Návratové hodnoty:
            ------------------
            Zoznam farebných reťazcov pre všetky vrcholy.
        """
        arr = [[] for _ in range(len(self.vertices.getAllVertices()))]
        for vertexindex in range(len(self.vertices.getAllVertices())): # Vytváranie farebného reťazca pre silne susediace vrcholy.
            for weightcolor in range(len(self.weights[vertexindex])):
                arr[vertexindex].append(f"{self.weights[vertexindex][weightcolor][1]};{self.weights[vertexindex][weightcolor][0]}")
            self.colorstring[vertexindex] = ":".join(arr[vertexindex])

        Istrength = dict()
        for i in self.vertices.getAllVertices(): # Pomocný slovník pre slabo susediace vrcholy.
            if not self.vertices.getStrengthOf(i):
                Istrength[i] = []

        for vertex1 in Istrength.items(): # Určenie farebnej palety pre slabo susediace vrcholy.
            for vertex2 in self.vertices.getAllVertices().items():
                for edgeindex in range(len(self.edges)):
                    if self.edges[edgeindex].isEdge(self.vertices.getNameOf(vertex1[0]), vertex2[1]):
                        strength = self.edges[edgeindex].value / min(self.vertices.values[vertex1[0]], self.vertices.values[vertex2[0]]) # Určenie množstva sily medzi vrcholmi.
                        Istrength[vertex1[0]].append([strength, vertex2[0]])
            if len(Istrength[vertex1[0]]) == 0:
                Istrength[vertex1[0]].append([0, -1])

        missingcolors = [""] * len(self.vertices.getAllVertices())
        for i in self.vertices.getAllVertices():
            if self.vertices.getStrengthOf(i): # Priradenie farebného reťazca silne susediacim vrcholom.
                missingcolors[i] = self.colorstring[i]
            elif Istrength[i][0][1] == -1: # Vrchol nemá žiadnu hranu s ostatnými vrcholmi.
                missingcolors[i] = self.colors[0]
            else: # Slabo susediace vrcholy.
                missingcolors[i] = ""

        chosencolor = dict()
        for i in Istrength.items(): # Určenie najmenšieho množstva sily.
            minval = sys.maxsize
            samecolor = -1
            for j in i[1]:
                if minval > j[0]:
                    minval = j[0]
                    samecolor = j[1]

            if samecolor != -1:
                chosencolor[i[0]] = samecolor
        
        for v1 in chosencolor.items(): # Slabo susediace vrcholy majú medzi sebou najmenšie množstvo sily.
            for v2 in chosencolor.items():
                if v1[1] == v2[0] and v2[1] == v1[0]:
                    missingcolors[v1[1]] = self.colors[0]
                    missingcolors[v2[1]] = self.colors[0]
                    chosencolor[v1[0]] = -1
                    chosencolor[v2[0]] = -1

        while "" in missingcolors: # Postupné priraďovanie farieb na základe už známych priradení.
            for i in range(len(missingcolors)):
                if missingcolors[i] == "":
                    missingcolors[i] = missingcolors[chosencolor[i]]

        return missingcolors
