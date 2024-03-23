import distinctipy
import sys
class Coloring:
    def __init__(self, vertices, edges, independentsets, linprog):
        self.Cb = linprog.Cb.copy()
        self.Base = linprog.Base.copy()
        self.R = linprog.R.copy()
        li = [list(x) for x in independentsets]
        li.sort()
        self.independentsets = li
        self.vertices = vertices
        self.edges = edges
        self.colors = []
        self.colorstring = [""] * len(self.vertices.vertices)
        self.makeColors()
        self.computeWeight()

    def makeColors(self):
        for color in distinctipy.get_colors(len(self.independentsets)):
            self.colors.append(self.RGBtoHEX(color))

    def RGBtoHEX(self, rgb: tuple[float, float, float]) -> str:
        rgb = tuple([int(255*a) for a in rgb])
        return '#%02x%02x%02x' % rgb

    def computeWeight(self):
        remove = []
        for i in range(len(self.Base)):
            if self.Base[i] >= len(self.independentsets):
                remove.append(i)
        
        for i in remove:
            self.Base.pop(i)
            self.R.pop(i)
            self.Cb.pop(i)
        
        sums = [0] * len(self.vertices.vertices)
        for vertexindex in range(len(self.vertices.vertices)):
            sum = 0
            for setindex in range(len(self.independentsets)):
                if vertexindex in self.independentsets[setindex]:
                    Rindex = self.Base.index(setindex)
                    sum += self.R[Rindex]
            sums[vertexindex] = sum

        self.weights = [0] * len(self.vertices.vertices)
        for weighindex in range(len(sums)):
            if sums[weighindex] > 0:
                Rindex = self.Base.index(setindex)
                tmp = (1 / sums[weighindex]) *self.R[Rindex]
                self.weights[weighindex] = round(tmp, 3)
            else:
                self.weights[weighindex] = 0.0

    def createColorString(self):
        self.matchColorsToVertices()
        arr = [[""] for _ in range(len(self.vertices.vertices))]
        # print(arr)
        for vertexindex in range(len(self.vertices.vertices)):
            for colorindex in range(len(self.colors)):
                if vertexindex in self.independentsets[colorindex]:
                    arr[vertexindex].append(f"{self.colors[colorindex]};{self.weights[vertexindex]}")
            self.colorstring[vertexindex] = ":".join(arr[vertexindex])
        # print(self.colorstring)
        Istrength = dict()
        for i in self.vertices.vertices:
            if not self.vertices.getStrengthOf(i):
                Istrength[i] = []

        # print(Istrength)
        for vertex1 in Istrength.items():
            for vertex2 in self.vertices.vertices.items():
                for edgeindex in range(len(self.edges)):
                    if self.edges[edgeindex].isEdge(self.vertices.getNameOf(vertex1[0]), vertex2[1]):
                        strength = self.edges[edgeindex].value / min(self.vertices.values[vertex1[0]], self.vertices.values[vertex2[0]])
                        Istrength[vertex1[0]].append([strength, vertex2[0]])
            if len(Istrength[vertex1[0]]) == 0:
                Istrength[vertex1[0]].append([0, -1])
        # print(Istrength)
                        
        missingcolors = [""] * len(self.vertices.vertices)
        for i in self.vertices.vertices:
            if self.vertices.getStrengthOf(i):
                missingcolors[i] = self.colorstring[i]
            elif Istrength[i][0][1] == -1:
                missingcolors[i] = self.colors[0]
            else:
                missingcolors[i] = ""

        chosencolor = dict()

        for i in Istrength.items():
            minval = sys.maxsize
            samecolor = -1
            for j in i[1]:
                # print("j", j)
                if minval > j[0]:
                    minval = j[0]
                    samecolor = j[1]
            if samecolor != -1:
                chosencolor[i[0]] = samecolor
        
        for v1 in chosencolor.items():
            for v2 in chosencolor.items():
                if v1[1] == v2[0] and v2[1] == v1[0]:
                    missingcolors[v1[1]] = self.colors[0]
                    missingcolors[v2[1]] = self.colors[0]
                    chosencolor[v1[0]] = -1
                    chosencolor[v2[0]] = -1
        while "" in missingcolors:
            for i in range(len(missingcolors)):
                if missingcolors[i] == "":
                    missingcolors[i] = missingcolors[chosencolor[i]]
        return missingcolors


    def matchColorsToVertices(self):
        self.palette = dict()
        for i in self.vertices.vertices:
            self.palette[i] = []
        for vertexindex in self.vertices.vertices:
            for setindex in range(len(self.independentsets)):
                if vertexindex in self.independentsets[setindex]:
                    self.palette[vertexindex].append(self.colors[setindex])
        # print(self.palette)




