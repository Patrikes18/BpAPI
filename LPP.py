import sys
class LinearProgram:
    def __init__(self):
        self.independentsets = [frozenset({1, 4}), frozenset({0, 2, 4}), frozenset({0, 2, 3}), frozenset({2, 3, 5}), frozenset({1, 5})]
        self.max = -1
        self.table = [[]]
        pass
    
    def createTablePhase1(self):
        for set in self.independentsets:
            for elem in set:
                if elem > self.max:
                    self.max = elem

        self.table = [[0] * len(self.independentsets) for _ in range(0, self.max + 1)]
        li = [list(x) for x in self.independentsets]
        li.sort()
        tmp = 0
        for set in li:
            for elem in set:
                self.table[elem][tmp] = 1
            tmp += 1

        self.tableau1 = [[0] * (len(self.independentsets) + 2 * (self.max + 1)) for _ in range(0, self.max + 1)]
        self.Cj = [0] * len(self.tableau1[0])
        for row in range(len(self.tableau1)):
            for col in range(len(self.tableau1[row])):
                if col < len(self.table[row]):
                    self.tableau1[row][col] = self.table[row][col]
                elif col < (len(self.table[row]) + (self.max + 1)):
                    if col == row + self.max:
                        self.tableau1[row][col] = -1
                else:
                    if col == row + self.max * 2 + 1:
                        self.tableau1[row][col] = 1
                        self.Cj[col] = 1
        
        self.Cb = [1] * (self.max + 1)
        self.R = [1] * (self.max + 1)
        self.Z = [0] * (len(self.tableau1[0]) + 1)
        self.Base = [1] * (self.max + 1)
        rowb = 0
        for col in range(len(self.Cj)):
            if self.Cj[col]:
                self.Base[rowb] = col
                rowb += 1

        self.changedBase = [False] * (self.max + 1)
        self.computeZ(1)

    def createTablePhase2(self):
        self.tableau2 = [[0] * (len(self.independentsets) + self.max + 1) for _ in range(0, self.max + 1)]
        
        for row in range(len(self.tableau2)):
            for col in range(len(self.tableau2[row])):
                self.tableau2[row][col] = self.tableau1[row][col]
        
        self.Cj = [0] * len(self.tableau2[0])
        for i in range(len(self.Cj)):
            if i < len(self.independentsets):
                self.Cj[i] = 1

        self.Cb = [1] * (self.max + 1)
        for i in range(len(self.Cb)):
            self.Cb[i] = self.Cj[self.Base[i]]

        self.changedBase = [False] * (self.max + 1)
        self.computeZ(2)

    def iterate(self, num):
        if num == 1:
            max = -1
            maxindexcol = -1
            for i in range(len(self.Z) - 1):
                if self.Z[i] > max:
                    maxindexcol = i
                    max = self.Z[i]
                    
            rescol = [sys.maxsize] * (self.max + 1)
            for i in range(len(self.R)):
                if self.tableau1[i][maxindexcol] > 0:
                    rescol[i] = self.R[i] / self.tableau1[i][maxindexcol]

            min = rescol[0]
            minindexrow = 0
            for i in range(len(rescol)):
                if rescol[i] < min and self.changedBase[i] == False:
                    minindexrow = i
                    min = rescol[i]
                    self.changedBase[i] = True

            pivot = self.tableau1[minindexrow][maxindexcol]
            for i in range(len(self.tableau1[minindexrow])):
                self.tableau1[minindexrow][i] = self.tableau1[minindexrow][i] / pivot

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

        elif num == 2:
            max = -1
            maxindexcol = -1

            for i in range(len(self.Z) - 1):
                if self.Z[i] > max:
                    maxindexcol = i
                    max = self.Z[i]

            rescol = [-1] * (self.max + 1)

            for i in range(len(self.R)):
                if self.tableau2[i][maxindexcol] > 0:
                    rescol[i] = self.R[i] / self.tableau2[i][maxindexcol]

            max = -1
            maxindexrow = -1

            for i in range(len(rescol)):
                if rescol[i] > max and self.changedBase[i] == False:
                    maxindexrow = i
                    max = rescol[i]
                    self.changedBase[i] = True
            pivot = self.tableau2[maxindexrow][maxindexcol]

            for i in range(len(self.tableau2[maxindexrow])):
                self.tableau2[maxindexrow][i] = self.tableau2[maxindexrow][i] / pivot
            self.R[maxindexrow] = self.R[maxindexrow] / pivot

            for i in range(len(self.tableau2)):
                pivotrowval = self.tableau2[i][maxindexcol]
                if i != maxindexrow:
                    for j in range(len(self.tableau2[i])):
                        self.tableau2[i][j] = self.tableau2[i][j] - (pivotrowval * self.tableau2[maxindexrow][j])

                    self.R[i] = self.R[i] - (pivotrowval * self.R[maxindexrow])

            self.Base[maxindexrow] = maxindexcol
            self.Cb[maxindexrow] = self.Cj[maxindexcol]
            self.computeZ(2)

    def computeZ(self, num):
        if num == 1:
            for col in range(len(self.tableau1[0])):
                sum = 0
                for row in range(len(self.tableau1)):
                    sum += self.Cb[row] * self.tableau1[row][col]
                
                sum -= self.Cj[col]
                self.Z[col] = sum
            
            sum = 0
            for rescol in range(len(self.R)):
                sum += self.Cb[rescol] * self.R[rescol]

            self.Z[-1] = sum
            self.williterate = False
            for i in range(len(self.Z) - 1):
                if self.Z[i] > 0:
                    self.williterate = True
                    break
        elif num == 2:
            for col in range(len(self.tableau2[0])):
                sum = 0
                for row in range(len(self.tableau2)):
                    sum += self.Cb[row] * self.tableau2[row][col]
                
                sum -= self.Cj[col]
                self.Z[col] = sum
            
            sum = 0
            for rescol in range(len(self.R)):
                sum += self.Cb[rescol] * self.R[rescol]

            self.Z[-1] = sum
            self.williterate = False
            for i in range(len(self.Z) - 1):
                if self.Z[i] > 0:
                    self.williterate = True
                    break

if __name__ == '__main__':
    lp = LinearProgram()
    lp.createTablePhase1()
    # for i in lp.tableau1:
    #     print(i)
    while lp.williterate:
        lp.iterate(1)
    lp.createTablePhase2()
    while lp.williterate:
        lp.iterate(2)
    # for i in lp.tableau2:
    #     print(i)
    print()
    print(lp.Cb)
    print()
    print(lp.Base)
    print()
    print(lp.R)
    print()