from abc import ABC, abstractmethod
from copy import deepcopy
from inspect import currentframe, getframeinfo


class Contrainte(ABC):

    def __init__(self, contrainte):
        self.contrainte = contrainte

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.contrainte

    @abstractmethod
    def validation_contrainte(self, variables):
        pass

    @abstractmethod
    def filtre(self, variables):
        pass


class ContrainteBinaire(Contrainte, ABC):

    def __init__(self, contrainte, var1, var2):
        super().__init__(contrainte)
        self.var1 = var1
        self.var2 = var2

    def __str__(self):
        return str(self.var1) + self.contrainte + str(self.var2)


class ContrainteTernaire(Contrainte, ABC):

    def __init__(self, contrainte, var1, var2, var3):
        super().__init__(contrainte)
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3

    def __str__(self):
        return str(self.var1) + " = " + str(self.var2) + self.contrainte + str(self.var3)


class Union(ContrainteTernaire):

    def __init__(self, var1, var2, var3):
        super().__init__(" Union ", var1, var2, var3)

    def validation_contrainte(self, variables):
        print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        print(f'Const? var1 {var1.const} var2 {var2.const} var3 {var3.const}')
        return var1.borneInf == var2.borneInf.union(var3.borneInf)

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        var1tmp = deepcopy(var1)
        var1.borneInf |= (var2.borneInf | var3.borneInf)
        var1.borneSup &= (var2.borneSup | var3.borneSup)
        if not var1.valide():
            raise Exception(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp


class Intersection(ContrainteTernaire):

    def __init__(self, var1, var2, var3):
        super().__init__(" Intersection ", var1, var2, var3)

    def validation_contrainte(self, variables):
        print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        print(f'Const? var1 {var1.const} var2 {var2.const} var3 {var3.const}')
        return var1.borneInf == var2.borneInf.intersection(var3.borneInf)

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        var1tmp = deepcopy(var1)
        var2tmp = deepcopy(var2)
        var3tmp = deepcopy(var3)
        var1.borneInf |= (var2.borneInf & var3.borneInf)
        var2.borneInf |= var1.borneInf
        var3.borneInf |= var1.borneInf
        var1.borneSup &= (var2.borneSup | var3.borneSup)
        if not (var1.valide() and var2.valide() and var3.valide()):
            raise Exception(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp or var3 != var3tmp


class Inclusion(ContrainteBinaire):

    def __init__(self, var1, var2):
        super().__init__(" Inclusion ", var1, var2)

    def validation_contrainte(self, variables):
        print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        return all([e in var2.borneInf for e in var1.borneInf])

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var1tmp = deepcopy(var1)
        var2tmp = deepcopy(var2)

        var1.borneSup &= var2.borneSup
        var2.borneInf |= var1.borneInf

        if not (var1.valide() and var2.valide()):
            raise Exception(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp


class Exclusion(ContrainteBinaire):

    def __init__(self, var1, var2):
        super().__init__(" Exclusion ", var1, var2)

    def validation_contrainte(self, variables):
        print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        return all([e not in var2.borneInf for e in var1.borneInf])

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var1tmp = deepcopy(var1)
        var2tmp = deepcopy(var2)

        var1.borneSup &= var2.borneSup
        var2.borneInf |= var1.borneInf

        var1.borneSup -= var2.borneInf
        var2.borneSup -= var1.borneInf

        if not (var1.valide() and var2.valide()):
            raise Exception(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp
