"""
    Trieda predstavujúca lineárne programovanie.

    Atribúty:
    ---------
    independentsets : list()
        zoznam najväčších nezávislých množín
    verticesnum : int
        počet vrcholov, ktoré boli použité v nezávislých množinách
    strongvertices : set()
        množina vrcholov, ktoré boli použité v nezávislých množinách
    self.tableau1 : [[]]
        tabuľka pre prvú fázu simplexovej metódy
    self.tableau2 : [[]]
        tabuľka pre druhú fázu simplexovej metódy
    Cj : []
        vektor ceny
    Cb : []
        koeficienty vektoru riešenia
    R : []
        výsledné váhy nezávislých množín
    Z : []
        redukovaný vektor ceny
    Base : []
        premenné, ktoré tvoria vektor riešenia
    changedBase : []
        pomocný zoznam, ktorý hovorí, kde sa menila hodnota vo vektore Base
    williterate : bool
        príznak, ktorý určuje iteráciu 

    Metódy:
    -------
    createTablePhase1()
        vytvorí tabuľku pre prvú fázu
    createTablePhase2()
        vytvorí tabuľku pre druhú fázu
    iterate(phase)
        iterovanie lineárneho programovania
    computeZ(phase)
        výpočet redukovaného vektoru Z
"""

import sys

class LinearProgram:
    def __init__(self, independentsets : list):
        """
            Konštruktor.

            Parametre:
            ----------
            independentsets : list
                zoznam najväčších nezávislých množín
        """
        self.independentsets = independentsets
        self.verticesnum = -1
        self.strongvertices = set()

    def createTablePhase1(self):
        """
            Metóda vytvorí inicializačnú tabuľku pre prvú fázu.
        """
        # Zistenie počtu vrcholov v nezávislých množinách.
        for set in self.independentsets:
            for elem in set:
                self.strongvertices.add(elem)
        self.verticesnum = len(self.strongvertices)

        table = [[0] * len(self.independentsets) for _ in range(0, self.verticesnum)] # Pomocná tabuľka (matica A).
        li = [list(x) for x in self.independentsets]
        li.sort()
        tmp = 0
        tmplist = list(self.strongvertices)
        tmplist.sort()
        for set in li:
            for elem in set:
                table[tmplist.index(elem)][tmp] = 1
            tmp += 1

        self.tableau1 = [[0] * (len(self.independentsets) + 2 * (self.verticesnum)) for _ in range(0, self.verticesnum)]
        self.Cj = [0] * len(self.tableau1[0])
        for row in range(len(self.tableau1)): # Zapĺňanie tabuľky na základe rovníc s nadbytočnými a umelými premennými.
            for col in range(len(self.tableau1[row])):
                if col < len(table[row]): # Hodnoty z matice A
                    self.tableau1[row][col] = table[row][col]
                elif col < (len(table[row]) + (self.verticesnum)): # Nadbytočné premenné.
                    if col == row + len(table[row]):
                        self.tableau1[row][col] = -1
                else:
                    if col == row + len(table[row]) + self.verticesnum: # Umelé premenné.
                        self.tableau1[row][col] = 1
                        self.Cj[col] = 1
        
        self.Cb = [1] * (self.verticesnum)
        self.R = [1] * (self.verticesnum)
        self.Z = [0] * (len(self.tableau1[0]) + 1) # O jedno dlhšie kvôli stĺcu R.
        self.Base = [1] * (self.verticesnum)
        rowb = 0
        for col in range(len(self.Cj)): # Vloženie koeficientov do stĺpca Báza.
            if self.Cj[col]:
                self.Base[rowb] = col
                rowb += 1

        self.changedBase = [False] * (self.verticesnum)
        self.computeZ(1)

    def createTablePhase2(self) -> int:
        """
            Metóda vytvorí inicializačnú tabuľku pre druhú fázu.
             
            Návratové hodnoty:
            ------------------
            0 - Inicializovanie prebehlo bez problémov.
            2 - Lineárne programovanie nemá riešenie.
        """
        for i in range(len(self.Base)): # Kontrola riešenia.
            if self.Base[i] >= (len(self.independentsets) + self.verticesnum): # Problém nemá riešenie, lebo máme umelé premenné v stĺpci Báza.
                return 2
        
        self.tableau2 = [[0] * (len(self.independentsets) + self.verticesnum) for _ in range(0, self.verticesnum)]
        
        for row in range(len(self.tableau2)): # Zapĺňanie tabuľky pre druhú fázu na základe výsledkov prvej fáze.
            for col in range(len(self.tableau2[row])):
                self.tableau2[row][col] = self.tableau1[row][col]
        
        self.Cj = [0] * len(self.tableau2[0])
        for i in range(len(self.Cj)): # Úprava účelovej funkcie.
            if i < len(self.independentsets):
                self.Cj[i] = 1

        self.Cb = [1] * (self.verticesnum)
        for i in range(len(self.Cb)): # Úprava na základe novej účelovej funkcie.
            self.Cb[i] = self.Cj[self.Base[i]]

        self.changedBase = [False] * (self.verticesnum)
        self.computeZ(2)
        return 0

    def iterate(self, phase) -> int:
        """
            Metóda implementujúca iterovanie v simplexovej metóde.

            Parametre:
            ----------
            phase : int
                Fáza, v ktorej iterujeme.
            
            Návratové hodnoty:
            0 - Iterovanie prebehlo bez problémov.
            1 - Iterovanie nemá riešenie.
        """
        if phase == 1: # Prvá fáza.
            # Zisťovanie pivotného stĺpca.
            max = -1
            maxindexcol = -1
            for i in range(len(self.Z) - 1):
                if self.Z[i] > max:
                    maxindexcol = i
                    max = self.Z[i]
            
            # Zisťovanie pivotného riadku.
            rescol = [sys.maxsize] * (self.verticesnum)
            for i in range(len(self.R)):
                if self.tableau1[i][maxindexcol] > 0:
                    rescol[i] = self.R[i] / self.tableau1[i][maxindexcol]

            min = sys.maxsize
            minindexrow = -1
            for i in range(len(rescol)):
                if rescol[i] < min and self.changedBase[i] == False:
                    minindexrow = i
                    min = rescol[i]
            if minindexrow < 0:
                return 1
            self.changedBase[minindexrow] = True

            # Úprava pivotného riadku.
            pivot = self.tableau1[minindexrow][maxindexcol]
            for i in range(len(self.tableau1[minindexrow])):
                self.tableau1[minindexrow][i] = self.tableau1[minindexrow][i] / pivot

            # Úprava nepivotných riadkov.
            self.R[minindexrow] = self.R[minindexrow] / pivot
            for i in range(len(self.tableau1)):
                pivotrowval = self.tableau1[i][maxindexcol]
                if i != minindexrow:
                    for j in range(len(self.tableau1[i])):
                        self.tableau1[i][j] = self.tableau1[i][j] - (pivotrowval * self.tableau1[minindexrow][j])
                    self.R[i] = self.R[i] - (pivotrowval * self.R[minindexrow])

            self.Base[minindexrow] = maxindexcol
            self.Cb[minindexrow] = self.Cj[maxindexcol]
            self.computeZ(1)

        elif phase == 2: # Druhá fáza.
            # Zisťovanie pivotného stĺpca.
            max = -1
            maxindexcol = -1
            for i in range(len(self.Z) - 1):
                if self.Z[i] > max:
                    maxindexcol = i
                    max = self.Z[i]

            # Zisťovanie pivotného riadku.
            rescol = [sys.maxsize] * (self.verticesnum)
            for i in range(len(self.R)):
                if self.tableau2[i][maxindexcol] > 0:
                    rescol[i] = self.R[i] / self.tableau2[i][maxindexcol]

            min = sys.maxsize
            minindexrow = -1
            for i in range(len(rescol)):
                if rescol[i] < min and self.changedBase[i] == False:
                    minindexrow = i
                    min = rescol[i]
            if minindexrow < 0:
                return 1
            self.changedBase[minindexrow] = True

            # Úprava pivotného riadku.
            pivot = self.tableau2[minindexrow][maxindexcol]
            for i in range(len(self.tableau2[minindexrow])):
                self.tableau2[minindexrow][i] = self.tableau2[minindexrow][i] / pivot

            # Úprava nepivotného riadku.
            self.R[minindexrow] = self.R[minindexrow] / pivot
            for i in range(len(self.tableau2)):
                pivotrowval = self.tableau2[i][maxindexcol]
                if i != minindexrow:
                    for j in range(len(self.tableau2[i])):
                        self.tableau2[i][j] = self.tableau2[i][j] - (pivotrowval * self.tableau2[minindexrow][j])
                    self.R[i] = self.R[i] - (pivotrowval * self.R[minindexrow])

            self.Base[minindexrow] = maxindexcol
            self.Cb[minindexrow] = self.Cj[maxindexcol]
            self.computeZ(2)
        return 0

    def computeZ(self, phase):
        """
            Metóda, ktorá implmentuje výpočet redukovaného vektoru Z.

            Parametre:
            ----------
            phase : int
                Fáza, v ktorej iterujeme.
        """
        if phase == 1: # Prvá fáza.
            for col in range(len(self.tableau1[0])):
                sum = 0
                for row in range(len(self.tableau1)):
                    sum += self.Cb[row] * self.tableau1[row][col]
                
                sum -= self.Cj[col]
                self.Z[col] = sum
            
            sum = 0
            for rescol in range(len(self.R)): # Výpočet pre stĺpec R.
                sum += self.Cb[rescol] * self.R[rescol]
            self.Z[-1] = sum

            self.williterate = False
            for i in range(len(self.Z) - 1): # Kontrola vektoru Z.
                if self.Z[i] > 0:
                    self.williterate = True
                    break
        elif phase == 2: # Druhá fáza.
            for col in range(len(self.tableau2[0])):
                sum = 0
                for row in range(len(self.tableau2)):
                    sum += self.Cb[row] * self.tableau2[row][col]
                
                sum -= self.Cj[col]
                self.Z[col] = sum
            
            sum = 0
            for rescol in range(len(self.R)): # Výpočet pre stĺpec R.
                sum += self.Cb[rescol] * self.R[rescol]
            self.Z[-1] = sum

            self.williterate = False
            for i in range(len(self.Z) - 1): # Kontrola vektoru Z.
                if self.Z[i] > 0:
                    self.williterate = True
                    break
