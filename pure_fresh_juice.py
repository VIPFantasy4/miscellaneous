from gurobipy import *


class Q4(Model):
    def __init__(self, name=''):
        super().__init__(name)
        self._QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', ]
        self._SUPPLIES_OF_ORANGE = [1400, 1850, 2950, 2100, 1750, 2300, 3150, 2900, ]
        self._TYPES_OF_JUICE = [
            'Orange Juice',
            'Orange and Mango Juice',
            'Breakfast Juice',
            'Tropical Juice',
            'Guava Delight',
            'Orchard Medley',
            'Strawberry Surprise',
        ]
        self._TYPES_OF_FRUIT = [
            'Orange',
            'Mango',
            'Apple',
            'Pineapple',
            'Passionfruit',
            'Guava',
            'Strawberry',
        ]
        self._DATA_OF_INGREDIENT = [
            [1, 0, 0, 0, 0, 0, 0, ],
            [0.9, 0.1, 0, 0, 0, 0, 0, ],
            [0.15, 0.02, 0.55, 0.28, 0, 0, 0, ],
            [0.04, 0, 0.65, 0.3, 0.01, 0, 0, ],
            [0, 0, 0.8, 0.1, 0, 0.1, 0, ],
            [0.45, 0.05, 0.5, 0, 0, 0, 0, ],
            [0, 0, 0.9, 0, 0, 0.02, 0.08, ],
        ]
        self._COSTS_OF_FRUITS = [901, 1300, 620, 800, 1500, 710, 1370, ]
        self._DATA_OF_ANTICIPATION = [
            [669, 859, 1340, 955, 787, 933, 1689, 1404, ],
            [286, 387, 593, 400, 377, 401, 611, 601, ],
            [466, 746, 1266, 900, 571, 757, 1121, 1054, ],
            [455, 531, 802, 671, 499, 620, 946, 946, ],
            [316, 462, 508, 375, 306, 464, 509, 417, ],
            [1197, 808, 603, 995, 1111, 760, 632, 800, ],
            [677, 714, 548, 323, 622, 786, 489, 407, ],
        ]
        self._PRICE = 1500

    def optimize_and_print(self):
        vars_of_quarter_to_juice = {
            (q, j): self.addVar()
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        }
        self.setObjective(quicksum(
            (self._PRICE - self.get_cost_by_type_of_juice(j)) * vars_of_quarter_to_juice[q, j]
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        ), GRB.MAXIMIZE)
        for q in range(len(self._QUARTERS)):
            for j in range(len(self._TYPES_OF_JUICE)):
                self.addConstr(vars_of_quarter_to_juice[q, j] <= self._DATA_OF_ANTICIPATION[j][q])
            self.addConstr(quicksum(
                self._DATA_OF_INGREDIENT[j][0] * vars_of_quarter_to_juice[q, j]
                for j in range(len(self._TYPES_OF_JUICE))
            ) <= self._SUPPLIES_OF_ORANGE[q])
        self.optimize()
        print('Q4', 'objVal', self.objVal)

    def get_cost_by_type_of_juice(self, j):
        return quicksum(self._COSTS_OF_FRUITS[i] * v for i, v in enumerate(self._DATA_OF_INGREDIENT[j]))


class Q5(Q4):
    def __init__(self, name=''):
        super().__init__(name)

    def optimize_and_print(self):
        vars_of_quarter_to_juice = {
            (q, j): self.addVar()
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        }
        vars_of_quarter_to_fruit = {
            (q, f): self.addVar(vtype=GRB.INTEGER)
            for q in range(len(self._QUARTERS)) for f in range(len(self._TYPES_OF_FRUIT))
        }
        self.setObjective(quicksum(
            (self._PRICE - self._COSTS_OF_FRUITS[0] * self._DATA_OF_INGREDIENT[j][0]) * vars_of_quarter_to_juice[q, j]
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        ) - quicksum(
            self._COSTS_OF_FRUITS[f] * vars_of_quarter_to_fruit[q, f] * 10
            for q in range(len(self._QUARTERS)) for f in range(len(self._TYPES_OF_FRUIT))
        ), GRB.MAXIMIZE)
        for q in range(len(self._QUARTERS)):
            for j in range(len(self._TYPES_OF_JUICE)):
                self.addConstr(vars_of_quarter_to_juice[q, j] <= self._DATA_OF_ANTICIPATION[j][q])
            for f in range(1, len(self._TYPES_OF_FRUIT)):
                self.addConstr(quicksum(
                    self._DATA_OF_INGREDIENT[j][f] * vars_of_quarter_to_juice[q, j]
                    for j in range(len(self._TYPES_OF_JUICE))
                ) <= 10 * vars_of_quarter_to_fruit[q, f])
            self.addConstr(quicksum(
                self._DATA_OF_INGREDIENT[j][0] * vars_of_quarter_to_juice[q, j]
                for j in range(len(self._TYPES_OF_JUICE))
            ) <= self._SUPPLIES_OF_ORANGE[q])
        self.optimize()
        print('Q5', 'objVal', self.objVal)


class Q6(Q5):
    def __init__(self, name=''):
        super().__init__(name)

    def optimize_and_print(self):
        gdi = self._TYPES_OF_JUICE.index('Guava Delight')
        omi = self._TYPES_OF_JUICE.index('Orchard Medley')
        ssi = self._TYPES_OF_JUICE.index('Strawberry Surprise')
        gourmet_juices = [gdi, omi, ssi, ]
        vars_of_quarter_to_juice = {
            (q, j): self.addVar()
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        }
        vars_of_quarter_to_fruit = {
            (q, f): self.addVar(vtype=GRB.INTEGER)
            for q in range(len(self._QUARTERS)) for f in range(len(self._TYPES_OF_FRUIT))
        }
        vars_of_quarter_to_gourmet_juice = {
            (q, gj): self.addVar(vtype=GRB.BINARY)
            for q in range(len(self._QUARTERS)) for gj in gourmet_juices
        }
        self.setObjective(quicksum(
            (self._PRICE - self._COSTS_OF_FRUITS[0] * self._DATA_OF_INGREDIENT[j][0]) * vars_of_quarter_to_juice[q, j]
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        ) - quicksum(
            self._COSTS_OF_FRUITS[f] * vars_of_quarter_to_fruit[q, f] * 10
            for q in range(len(self._QUARTERS)) for f in range(len(self._TYPES_OF_FRUIT))
        ), GRB.MAXIMIZE)
        for q in range(len(self._QUARTERS)):
            for j in range(len(self._TYPES_OF_JUICE)):
                self.addConstr(vars_of_quarter_to_juice[q, j] <= self._DATA_OF_ANTICIPATION[j][q])
                self.addConstr(
                    vars_of_quarter_to_juice[q, j] == vars_of_quarter_to_juice[q, j]
                    * (j in gourmet_juices and vars_of_quarter_to_gourmet_juice[q, j] or 1)
                )
            for f in range(1, len(self._TYPES_OF_FRUIT)):
                self.addConstr(quicksum(
                    self._DATA_OF_INGREDIENT[j][f] * vars_of_quarter_to_juice[q, j]
                    for j in range(len(self._TYPES_OF_JUICE))
                ) <= 10 * vars_of_quarter_to_fruit[q, f])
            self.addConstr(quicksum(
                self._DATA_OF_INGREDIENT[j][0] * vars_of_quarter_to_juice[q, j]
                for j in range(len(self._TYPES_OF_JUICE))
            ) <= self._SUPPLIES_OF_ORANGE[q])
            self.addConstr(quicksum(vars_of_quarter_to_gourmet_juice[q, gj] for gj in gourmet_juices) <= 2)
        self.optimize()
        print('Q6', 'objVal', self.objVal)


class Q7(Q6):
    def __init__(self, name=''):
        super().__init__(name)

    def optimize_and_print(self):
        gdi = self._TYPES_OF_JUICE.index('Guava Delight')
        omi = self._TYPES_OF_JUICE.index('Orchard Medley')
        ssi = self._TYPES_OF_JUICE.index('Strawberry Surprise')
        gourmet_juices = [gdi, omi, ssi, ]
        vars_of_quarter_to_juice = {
            (q, j): self.addVar()
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        }
        vars_of_quarter_to_fruit = {
            (q, f): self.addVar(vtype=GRB.INTEGER)
            for q in range(len(self._QUARTERS)) for f in range(len(self._TYPES_OF_FRUIT))
        }
        vars_of_quarter_to_gourmet_juice = {
            (q, gj): self.addVar(vtype=GRB.BINARY)
            for q in range(len(self._QUARTERS)) for gj in gourmet_juices
        }
        self.setObjective(quicksum(
            (self._PRICE - self._COSTS_OF_FRUITS[0] * self._DATA_OF_INGREDIENT[j][0]) * vars_of_quarter_to_juice[q, j]
            for q in range(len(self._QUARTERS)) for j in range(len(self._TYPES_OF_JUICE))
        ) - quicksum(
            self._COSTS_OF_FRUITS[f] * vars_of_quarter_to_fruit[q, f] * 10
            for q in range(len(self._QUARTERS)) for f in range(len(self._TYPES_OF_FRUIT))
        ), GRB.MAXIMIZE)
        for q in range(len(self._QUARTERS)):
            for j in range(len(self._TYPES_OF_JUICE)):
                self.addConstr(vars_of_quarter_to_juice[q, j] <= self._DATA_OF_ANTICIPATION[j][q])
                self.addConstr(
                    vars_of_quarter_to_juice[q, j] == vars_of_quarter_to_juice[q, j]
                    * (j in gourmet_juices and vars_of_quarter_to_gourmet_juice[q, j] or 1)
                )
            for f in range(1, len(self._TYPES_OF_FRUIT)):
                self.addConstr(quicksum(
                    self._DATA_OF_INGREDIENT[j][f] * vars_of_quarter_to_juice[q, j]
                    for j in range(len(self._TYPES_OF_JUICE))
                ) <= 10 * vars_of_quarter_to_fruit[q, f])
            self.addConstr(quicksum(
                self._DATA_OF_INGREDIENT[j][0] * vars_of_quarter_to_juice[q, j]
                for j in range(len(self._TYPES_OF_JUICE))
            ) <= self._SUPPLIES_OF_ORANGE[q])
            self.addConstr(quicksum(vars_of_quarter_to_gourmet_juice[q, gj] for gj in gourmet_juices) <= 2)
            if q > 0:
                for gj in gourmet_juices:
                    self.addConstr(
                        vars_of_quarter_to_gourmet_juice[q, gj] + vars_of_quarter_to_gourmet_juice[q - 1, gj] >= 1
                    )
        self.optimize()
        print('Q7', 'objVal', self.objVal)
        print('-' * 44)
        for j in range(len(self._TYPES_OF_JUICE)):
            print([vars_of_quarter_to_juice[q, j].x for q in range(len(self._QUARTERS))])


Q7().optimize_and_print()
