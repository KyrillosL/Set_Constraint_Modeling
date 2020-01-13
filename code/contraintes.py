from abc import ABC, abstractmethod
from copy import deepcopy


# class ContrainteUnaire(Contrainte):
#


class Variable:

    def __init__(self, domaine):
        self.domaine = domaine

    def vide(self):
        return self.domaine == set()

    def impossible_a_couper(self):
        return len(self.domaine) <= 1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.domaine)


class Contrainte(ABC):

    def __init__(self, contrainte):
        self.contrainte = contrainte

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.contrainte

    @abstractmethod
    def __call__(self, variables):
        pass


class ContrainteBinaire(Contrainte):

    def __init__(self, contrainte, var1, var2):
        super().__init__(contrainte)
        self.var1 = var1
        self.var2 = var2

    def __str__(self):
        return str(self.var1) + self.contrainte + str(self.var2)


class Union(ContrainteBinaire):

    def __init__(self, var1, var2):
        super().__init__(" Union ", var1, var2)
        self.var1 = var1
        self.var2 = var2

    def __call__(self, variables):
        print(self)
        if isinstance(self.var1, Contrainte):
            var1 = self.var1(variables)
        else:
            var1 = variables[self.var1]
        if isinstance(self.var2, Contrainte):
            var2 = self.var2(variables)
        else:
            var2 = variables[self.var2]

        union = var1.domaine.union(var2.domaine)
        print(f'Union = {union}')
        var1.domaine = var1.domaine.intersection(union)
        var2.domaine = var2.domaine.intersection(union)
        return union


class Intersection(ContrainteBinaire):

    def __init__(self, var1, var2):
        super().__init__(" Intersection ", var1, var2)
        self.var1 = var1
        self.var2 = var2

    def __call__(self, variables):
        print(self)
        if isinstance(self.var1, Contrainte):
            var1 = self.var1(variables)
        else:
            var1 = variables[self.var1]
        if isinstance(self.var2, Contrainte):
            var2 = self.var2(variables)
        else:
            var2 = variables[self.var2]

        intersection = var1.domaine.intersection(var2.domaine)
        print(f'Inter = {intersection}')
        var1.domaine = deepcopy(intersection)
        var2.domaine = deepcopy(intersection)
        return intersection


class Egal(ContrainteBinaire):

    def __init__(self, var1, var2):
        super().__init__(" = ", var1, var2)
        self.var1 = var1
        self.var2 = var2

    def __call__(self, variables):
        print(self)
        if isinstance(self.var1, Contrainte):
            var1 = self.var1(variables)
        else:
            var1 = variables[self.var1]
        if isinstance(self.var2, Contrainte):
            var2 = self.var2(variables)
        else:
            var2 = variables[self.var2]
        if isinstance(var1, Variable):
            var1 = var1.domaine
        if isinstance(var2, Variable):
            var2 = var2.domaine

        egal = var1 == var2
        print(f'egal = {egal}')
        return egal
