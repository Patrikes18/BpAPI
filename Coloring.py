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
        self.computeWeight() #TODO možno odstrániť?

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
        
        remove.sort(reverse=True)

        for i in remove:
            self.Base.pop(i)
            self.R.pop(i)
            self.Cb.pop(i)
        
        vertices = dict()
        for i in self.vertices.vertices:
            vertices[i] = []

        for i in range(len(self.independentsets)):
            for j in range(len(self.independentsets[i])):
                vertices[self.independentsets[i][j]].append(self.colors[i])
        
        self.weights = []
        for vertexindex in range(len(vertices)):
            self.weights.append(self.computeWeightFor(vertices[vertexindex]))
        # print(self.weights)

    def computeWeightFor(self, vertex):
        sum = 0
        for i in vertex:
            index = self.colors.index(i)
            Rindex = self.Base.index(index)
            sum += self.R[Rindex]
        # print("R sum", sum)
        val = []
        for i in vertex:
            index = self.colors.index(i)
            Rindex = self.Base.index(index)
            tmp = (1 / sum) * self.R[Rindex]
            if tmp > 0.0:
                val.append([round(tmp,3), i])
        # print(val)
        return val

    def createColorString(self):
        self.matchColorsToVertices()
        arr = [[] for _ in range(len(self.vertices.vertices))]
        # print(arr)
        for vertexindex in range(len(self.vertices.vertices)):
            for weightcolor in range(len(self.weights[vertexindex])):
                arr[vertexindex].append(f"{self.weights[vertexindex][weightcolor][1]};{self.weights[vertexindex][weightcolor][0]}")
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
