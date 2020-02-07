from abc import ABC, abstractmethod
# from copy import copy as deepcopy


class ContraiteException(Exception):
    pass


class Contrainte(ABC):

    def __init__(self, contrainte, priorite):
        self.contrainte = contrainte
        self.priorite = priorite

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

    def __init__(self, contrainte, var1, var2, priorite):
        super().__init__(contrainte, priorite)
        self.var1 = var1
        self.var2 = var2

    def __str__(self):
        return str(self.var1) + self.contrainte + str(self.var2)


class Different(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" != ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename.split('/')[-1], frameinfo.lineno)
        # print(f'Const? var1 {var1.const} var2 {var2.const}')
        return var1.borneInf != var2.borneInf

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        if var1.const and var2.const:
            if var1.borneInf == var2.borneInf:
                raise ContraiteException(f'{var1.borneInf} est pas egal a {var2.borneInf}')
        return False


class Egal(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" = ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename.split('/')[-1], frameinfo.lineno)
        # print(f'Const? var1 {var1.const} var2 {var2.const}')
        return var1.borneInf == var2.borneInf

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        if var1.const and var2.const:
            if var1.borneInf != var2.borneInf:
                raise ContraiteException("var1 != var2")
        if var2.const and not var1.const:
            var1.borneInf = var2.borneInf
            var1.const = True
            return True
        if var1.const and not var2.const:
            var2.borneInf = var1.borneInf
            var2.const = True
            return True
        return False


class Cardinalite(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" cardinalite =  ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename.split('/')[-1], frameinfo.lineno)
        # print(f'Const? var1 {var1.const} var2 {var2.const}')
        return (len(var1.borneInf) <= var2.borneInf) and (len(var1.borneSup) >= var2.borneSup)

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        if var1.const:
            if len(var1.borneInf) > var2.borneInf:
                raise ContraiteException(f'Cardinalite de {var1.nom} non respectee')
        return False


class ContrainteTernaire(Contrainte, ABC):

    def __init__(self, contrainte, var1, var2, var3, priorite):
        super().__init__(contrainte, priorite)
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3

    def __str__(self):
        return str(self.var1) + " = " + str(self.var2) + self.contrainte + str(self.var3)


class Union(ContrainteTernaire):

    def __init__(self, var1, var2, var3, priorite):
        super().__init__(" Union ", var1, var2, var3, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename.split('/')[-1], frameinfo.lineno)
        # print(f'Const? var1 {var1.const} var2 {var2.const} var3 {var3.const}')
        return var1.borneInf == var2.borneInf.union(var3.borneInf)

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        var1tmp = var1.duplicate()
        var1.borneInf |= (var2.borneInf | var3.borneInf)
        var1.borneSup &= (var2.borneSup | var3.borneSup)
        if not var1.valide():
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp


class Intersection(ContrainteTernaire):

    def __init__(self, var1, var2, var3, priorite):
        super().__init__(" Intersection ", var1, var2, var3, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename.split('/')[-1], frameinfo.lineno)
        # print(f'Const? var1 {var1.const} var2 {var2.const} var3 {var3.const}')
        # print(f'Borne? \nvar1 {var1.borneInf == var1.borneSup}\nvar2 {var2.borneInf == var2.borneSup}\nvar3 {var3.borneInf == var3.borneSup}')
        return var1.borneInf == var2.borneInf.intersection(var3.borneInf)

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        var1tmp = var1.duplicate()
        var2tmp = var2.duplicate()
        var3tmp = var3.duplicate()
        var1.borneInf |= (var2.borneInf & var3.borneInf)
        var2.borneInf |= var1.borneInf
        var3.borneInf |= var1.borneInf
        var1.borneSup &= (var2.borneSup & var3.borneSup)
        if not (var1.valide() and var2.valide() and var3.valide()):
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp or var3 != var3tmp


class ContrainteQuaternaire(Contrainte, ABC):

    def __init__(self, contrainte, var1, var2, var3, var4, priorite):
        super().__init__(contrainte, priorite)
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
        self.var4 = var4

    def __str__(self):
        return str(self.var1) + " = " + str(self.var2) + self.contrainte + \
               str(self.var3) + self.contrainte + str(self.var4)


class Intersection3(ContrainteQuaternaire):

    def __init__(self, var1, var2, var3, var4, priorite):
        super().__init__(" Intersection ", var1, var2, var3, var4, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        var4 = variables[self.var4]
        # frameinfo = getframeinfo(currentframe())
        # print(frameinfo.filename.split('/')[-1], frameinfo.lineno)
        # print(f'Const? var1 {var1.const} var2 {var2.const} var3 {var3.const}')
        # print(f'Borne? \nvar1 {var1.borneInf == var1.borneSup}\nvar2 {var2.borneInf == var2.borneSup}\nvar3 {var3.borneInf == var3.borneSup}')
        return var1.borneInf == var2.borneInf.intersection(var3.borneInf).intersection(var4.borneInf)

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var3 = variables[self.var3]
        var4 = variables[self.var4]
        var1tmp = var1.duplicate()
        var2tmp = var2.duplicate()
        var3tmp = var3.duplicate()
        var4tmp = var4.duplicate()
        var1.borneInf |= (var2.borneInf & var3.borneInf & var4.borneInf)
        var2.borneInf |= var1.borneInf
        var3.borneInf |= var1.borneInf
        var4.borneInf |= var1.borneInf
        var1.borneSup &= (var2.borneSup & var3.borneSup & var4.borneSup)
        if not (var1.valide() and var2.valide() and var3.valide()):
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp or var3 != var3tmp or var4 != var4tmp


class Inclusion(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" Inclusion ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        return all([e in var2.borneInf for e in var1.borneInf])

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var1tmp = var1.duplicate()
        var2tmp = var2.duplicate()

        var1.borneSup &= var2.borneSup
        var2.borneInf |= var1.borneInf

        if not (var1.valide() and var2.valide()):
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp


class Exclusion(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" Exclusion ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        # print(self)
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        return all([e not in var2.borneInf for e in var1.borneInf])

    def filtre(self, variables):
        var1 = variables[self.var1]
        var2 = variables[self.var2]
        var1tmp = var1.duplicate()
        var2tmp = var2.duplicate()

        var1.borneSup &= var2.borneSup
        var2.borneInf |= var1.borneInf

        var1.borneSup -= var2.borneInf
        var2.borneSup -= var1.borneInf

        if not (var1.valide() and var2.valide()):
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp
