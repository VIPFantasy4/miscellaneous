from gurobipy import *
import pandas as pd


class Q2(Model):
    def __init__(self, name=''):
        super().__init__(name)
        self._STORES = ['S' + str(i) for i in range(10)]
        self._DCS = ['DC' + str(i) for i in range(3)]
        self._DATA_OF_TRANSPORTING = [
            [3149, 3761, 1498, 3592, 3950, 2385, 2522, 2976, 3691, 616, ],
            [2895, 2548, 1685, 3055, 2782, 993, 755, 2323, 2412, 2454, ],
            [1406, 1653, 1767, 1566, 1780, 1493, 1664, 878, 1497, 2608, ],
        ]
        self._DEMANDS = [12, 14, 6, 20, 14, 15, 7, 16, 8, 7, ]
        self._CAPACITIES = [50, 50, 73, ]

    def optimize_and_print(self):
        vars_of_dc_to_store = {
            (dc, s): self.addVar()
            for dc in range(len(self._DCS)) for s in range(len(self._STORES))
        }
        self.setObjective(quicksum(
            vars_of_dc_to_store[dc, s] * self._DATA_OF_TRANSPORTING[dc][s]
            for dc in range(len(self._DCS)) for s in range(len(self._STORES))
        ), GRB.MINIMIZE)
        for dc in range(len(self._DCS)):
            self.addConstr(quicksum(
                vars_of_dc_to_store[dc, s] for s in range(len(self._STORES))
            ) <= self._CAPACITIES[dc])
        for s in range(len(self._STORES)):
            self.addConstr(quicksum(
                vars_of_dc_to_store[dc, s] for dc in range(len(self._DCS))
            ) == self._DEMANDS[s])
        self.optimize()
        print('Q2', 'objVal', self.objVal)
        print('-' * 44)
        print(pd.DataFrame(
            [[vars_of_dc_to_store[dc, s].x for s in range(len(self._STORES))] for dc in range(len(self._DCS))],
            index=self._DCS, columns=self._STORES))


Q2().optimize_and_print()
