import distinctipy
import sys
    
class Coloring:
    def __init__(self):
        self.Cb = [1, 1, 1, 0, 1, 1]
        self.Base = [0, 2, 4, 7, 1, 3]
        self.R = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        self.independentsets = [frozenset({1, 4}), frozenset({0, 2, 4}), frozenset({0, 2, 3}), frozenset({2, 3, 5}), frozenset({1, 5})]
        self.colors = []
        self.inputedges = [{'vertices': ['a', 'b'], 'value': 0.3}, {'vertices': ['a', 'f'], 'value': 0.3}, {'vertices': ['a', 'g'], 'value': 0.15}, {'vertices': ['b', 'g'], 'value': 0.2}, {'vertices': ['b', 'c'], 'value': 0.3}, {'vertices': ['b', 'd'], 'value': 0.3}, {'vertices': ['d', 'e'], 'value': 0.25}, {'vertices': ['d', 'g'], 'value': 0.1}, {'vertices': ['e', 'g'], 'value': 0.3}, {'vertices': ['e', 'f'], 'value': 0.3}]
        self.strongedges = [{'vertices': ['a', 'b'], 'value': 0.3}, {'vertices': ['a', 'f'], 'value': 0.3}, {'vertices': ['b', 'c'], 'value': 0.3}, {'vertices': ['b', 'd'], 'value': 0.3}, {'vertices': ['d', 'e'], 'value': 0.25}, {'vertices': ['e', 'f'], 'value': 0.3}]
        # print(self.inputedges.difference(self.strongedges))
        self.allvertices = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g'}
        self.strongvertices = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'}
        self.invertices = {'a': 0.4, 'b': 0.5, 'c': 0.8, 'd': 0.3, 'e': 0.7, 'f': 0.5, 'g': 0.8}
        self.findWeakEdges()
        self.computeWeakVertexColor()
        self.colors = []
        self.makeColors()
        print(self.colors)
        self.colorVertices()

    def makeColors(self):
        for color in distinctipy.get_colors(len(self.independentsets)):
            self.colors.append(self.RGBtoHEX(color))

    def RGBtoHEX(self, rgb: tuple[float, float, float]) -> str:
        rgb = tuple([int(255*a) for a in rgb])
        return '#%02x%02x%02x' % rgb
    
    def findWeakEdges(self):
        self.weakedges = []
        self.weakvertices = set()
        for edge in self.inputedges:
            if edge not in self.strongedges:
                self.weakedges.append(edge)
        # print(self.weakedges)
        for weakedge in self.weakedges:
            # print(self.strongvertices.keys())
            if self.getIndexOf(weakedge["vertices"][0]) not in self.strongvertices.keys():
                self.weakvertices.add(weakedge["vertices"][0])
            if self.getIndexOf(weakedge["vertices"][1]) not in self.strongvertices.keys():
                self.weakvertices.add(weakedge["vertices"][1])
        self.weakvertices = sorted(self.weakvertices)

    def getIndexOf(self, ver):
        for v in self.allvertices.items():
            if v[1] == ver:
                return v[0]
    
    def computeWeakVertexColor(self):
        #TODO prerobit pre viacere nespojene vrcholy
        self.Istrength = []
        for edge in self.weakedges:
            strength = edge["value"] / min(self.invertices[edge["vertices"][0]], self.invertices[edge["vertices"][1]])
            val = []
            if self.getIndexOf(edge["vertices"][0]) not in self.strongvertices.keys() and self.getIndexOf(edge["vertices"][1]) not in self.strongvertices.keys():
                val = [strength, -1]
            elif self.getIndexOf(edge["vertices"][0]) not in self.strongvertices.keys():
                val = [strength, self.getIndexOf(edge["vertices"][1])]
            elif self.getIndexOf(edge["vertices"][1]) not in self.strongvertices.keys():
                val = [strength, self.getIndexOf(edge["vertices"][0])]
            self.Istrength.append(val)
        print(self.Istrength)
        minval = sys.maxsize
        samecolor = -1
        for s in self.Istrength:
            if minval > s[0]:
                minval = s[0]
                samecolor = s[1]
        print(samecolor)
        return
    
    def colorVertices(self):
        remove = []
        for i in range(len(self.Base)):
            if self.Base[i] >= len(self.independentsets):
                remove.append(i)
        
        for i in remove:
            self.Base.pop(i)
            self.R.pop(i)
            self.Cb.pop(i)

        # vertices = dict.fromkeys(self.allvertices,[])
        vertices = dict()
        for i in self.allvertices:
            vertices[i] = []
        # print(vertices)
        li = [list(x) for x in self.independentsets]
        li.sort()
        print(li)
        for i in range(len(li)):
            for j in range(len(li[i])):
                vertices[li[i][j]].append(self.colors[i])
        
        vertexcolorarray = []
        for vertexindex in range(len(vertices)):
            vertexcolorarray.append(self.colorString(vertices[vertexindex]))
        print(vertexcolorarray)
        return

    def colorString(self, vertexcolors) -> str:
        # print(vertexcolors)
        sum = 0
        for i in vertexcolors:
            # print(i)
            index = self.colors.index(i)
            Rindex = self.Base.index(index)
            sum += self.R[Rindex]
        print("R sum", sum)
        val = []
        for i in vertexcolors:
            index = self.colors.index(i)
            Rindex = self.Base.index(index)
            tmp = (1 / sum) * self.R[Rindex]
            val.append(round(tmp,3))
        print(val)
        colorsforvertex = []
        for i in range(len(val)):
            colorsforvertex.append(f"{vertexcolors[i]};{val[i]}")
        return ":".join(colorsforvertex)










if __name__ == '__main__':
    c = Coloring()