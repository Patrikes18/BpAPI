"""
    Trieda predstavujúca zoznam vrcholov fuzzy grafu.

    Atribúty:
    ---------
    vertices : dict()
        slovník typu {index : 'názov'}
    values : dict()
        slovník typu {index : váha}
    strong : dict()
        slovník typu {index : sila}

    Metódy:
    -------
    getAllVertices()
        vracia slovník všetkých vrcholov
    getIndexOf(ver)
        vracia index na základe názvu vrcholu
    getNameOf(index)
        vracia názov vrcholu na základe indexu
    getValueWithIndex(ver)
        vracia váhu na základe indexu vrcholu
    getValueWithName(name)
        vracia váhu na základe názvu vrcholu
    setStrong(name)
        nastaví vrchol ako silný
    getAllStrength()
        vracia silu všetkých vrcholov
    getStrengthOf(index)
        vracia silu jedného vrcholu
"""
class VertexModel:
    def __init__(self, vertices : dict):
        """
            Konštruktor.

            Parametre:
            ----------
            vertices : dict()
                slovník typu {'názov' : váha}
        """
        self.vertices = dict(enumerate(vertices))
        self.values = dict()
        self.strong = dict()
        for ver in vertices.items():
            self.values[self.getIndexOf(ver[0])] = ver[1]
            self.strong[self.getIndexOf(ver[0])] = False

    def getAllVertices(self) -> dict:
        """
            Metóda, ktorá vracia slovník všetkých vrcholov.

            Návratové hodnoty:
            ------------------
            Slovník typu {index : 'názov'}.
        """
        return self.vertices
    
    def getIndexOf(self, ver : str) -> int | None:
        """
            Metóda, ktorá vracia index na základe názvu vrcholu.

            Parametre:
            ----------
            ver : str
                Hľadaný vrchol.
            
            Návratové hodnoty:
            ------------------
            Index vrcholu alebo None, ak sa vrchol nenachádza v zozname.
        """
        for v in self.vertices.items():
            if v[1] == ver:
                return v[0]
        return None
    
    def getNameOf(self, index : int) -> str:
        """
            Metóda, ktorá vracia názov vrcholu na základe jeho indexu.

            Parametre:
            ----------
            index : int
                Index hľadaného vrcholu.
            
            Návratové hodnoty:
            ------------------
            Názov vrcholu.
        """
        return self.vertices[index]
            
    def getValueWithIndex(self, ver : int) -> float:
        """
            Metóda, ktorá vracia váhu na základe indexu vrcholu.

            Parametre:
            ----------
            ver : int
                Index hľadaného vrcholu.
            
            Návratové hodnoty:
            ------------------
            Váha vrcholu.
        """
        return self.values[ver]
    
    def getValueWithName(self, name : str) -> float:
        """
            Metóda, ktorá vracia váhu na základe názvu vrcholu.

            Parametre:
            ----------
            name : str
                Hľadaný vrchol.
            
            Návratové hodnoty:
            ------------------
            Váha vrcholu.
        """
        ver = self.getIndexOf(name)
        return self.values[ver]
    
    def setStrong(self, name : str):
        """
            Metóda, ktorá nastaví vrchol ako silný.

            Parametre:
            ----------
            name : str
                Hľadaný vrchol.
        """
        ver = self.getIndexOf(name)
        self.strong[ver] = True

    def getAllStrength(self) -> dict:
        """
            Metóda, ktorá vracia silu všetkých vrcholov.

            Návratové hodnoty:
            ------------------
            Slovník typu {index : sila} 
        """
        return self.strong
    
    def getStrengthOf(self, index : int) -> bool:
        """
            Metóda, ktorá vracia váhu na základe názvu vrcholu.

            Parametre:
            ----------
            index : int
                Index hľadaného vrcholu.
            
            Návratové hodnoty:
            ------------------
            Sila vrcholu.
        """
        return self.strong[index]