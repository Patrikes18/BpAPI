"""
    Trieda predstavujúca hranu fuzzy grafu.

    Atribúty:
    ---------
    v1 : str
        názov prvého vrcholu hrany
    v2 : str
        názov druhého vrcholu hrany
    value : float
        váha hrany
    strong : bool
        sila hrany

    Metódy:
    -------
    isEdge(v1, v2)
        vracia True, ak vrcholy v1 a v2 tvoria túto hranu, inak vracia False
    getValue()
        vracia váhu hrany
    getFirstVertex()
        vracia názov prvého vrcholu hrany
    getSecondVertex
        vracia názov druhého vrcholu hrany
    setStrong()
        nastaví hranu ako silnú
    getStrenght()
        vráti silu hrany
"""
class EdgeModel:
    def __init__(self, edge : dict):
        """
            Konštruktor.

            Parametre:
            ----------
            edge : dict()
                slovník typu {'vertices' : ['vrchol1', 'vrchol2'], 'value' : váha}
        """
        s = sorted(edge["vertices"])
        self.v1 = s[0]
        self.v2 = s[1]
        self.value = edge["value"]
        self.strong = False

    def isEdge(self, v1 : str, v2 : str) -> bool:
        """
            Metóda, ktorá zisťuje, či vrcholy tvoria hranu.
            
            Parametre:
            ----------
            v1 : str
                názov prvého vrcholu hrany
            v2 : str
                názov druhého vrcholu hrany
            
            Návratové hodnoty:
            ------------------
            True, ak vrcholy v1 a v2 tvoria túto hranu, inak False.
        """
        return (self.v1 == v1 and self.v2 == v2) or (self.v1 == v2 and self.v2 == v1)
    
    def getValue(self) -> float:
        """
            Metóda vracia váhu hrany.

            Návratové hodnoty:
            ------------------
            Váha hrany.
        """
        return self.value
    
    def getFirstVertex(self) -> str:
        """
            Metóda vracia názov prvého vrcholu hrany.

            Návratové hodnoty:
            ------------------
            Názov vrchola.
        """
        return self.v1
    
    def getSecondVertex(self) -> str:
        """
            Metóda vracia názov druhého vrcholu hrany.

            Návratové hodnoty:
            ------------------
            Názov vrchola.
        """
        return self.v2
    
    def setStrong(self):
        """
            Metóda, ktorá nastaví hranu ako silnú.
        """
        self.strong = True

    def getStrength(self) -> bool:
        """
            Metóda, ktorá vráti silu hrany.

            Návratové hodnoty:
            ------------------
            True, ak je hrana silná, inak vracia False.
        """
        return self.strong