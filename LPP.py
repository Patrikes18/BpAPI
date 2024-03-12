class LinearProgram:
    def __init__(self):
        self.independentsets = [frozenset({1, 4}), frozenset({0, 2, 4}), frozenset({0, 2, 3}), frozenset({2, 3, 5}), frozenset({1, 5})]
        self.max = -1
        self.table = [[]]
        pass
    
    def createTable(self):
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


if __name__ == '__main__':
    lp = LinearProgram()
    lp.createTable()