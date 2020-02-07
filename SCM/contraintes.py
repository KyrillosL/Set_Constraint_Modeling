from abc import ABC, abstractmethod


def get_var(variable, nom):
    return variable[nom]


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

    @abstractmethod
    def duplicate(self):
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
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        return var1.borneInf != var2.borneInf

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        if var1.const and var2.const:
            if var1.borneInf == var2.borneInf:
                raise ContraiteException(f'{var1.borneInf} est egal a {var2.borneInf}')
        return False

    def duplicate(self):
        return Different(self.var1, self.var2, self.priorite)


class Egal(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" = ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        return var1.borneInf == var2.borneInf

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        if var1.const and var2.const:
            if var1.borneInf != var2.borneInf:
                raise ContraiteException("var1 != var2")
        if var2.const and not var1.const:
            var1.borneInf = var2.borneInf
            var1.borneSup = var1.borneInf
            var1.const = True
            return True
        if var1.const and not var2.const:
            var2.borneInf = var1.borneInf
            var2.borneSup = var2.borneInf
            var2.const = True
            return True
        return False

    def duplicate(self):
        return Egal(self.var1, self.var2, self.priorite)


class Cardinalite(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" cardinalite =  ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        return (len(var1.borneInf) <= var2.value) and (len(var1.borneSup) >= var2.value)

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        if var1.const:
            if len(var1.borneInf) != var2.value:
                raise ContraiteException(f'Cardinalite de {var1.nom} non respectee')
        return False

    def duplicate(self):
        return Cardinalite(self.var1, self.var2, self.priorite)


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
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var3 = get_var(variables, self.var3)
        return var1.borneInf == var2.borneInf.union(var3.borneInf)

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var3 = get_var(variables, self.var3)
        var1tmp = var1.duplicate()
        var1.borneInf |= (var2.borneInf | var3.borneInf)
        var1.borneSup &= (var2.borneSup | var3.borneSup)
        if not var1.valide():
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp

    def duplicate(self):
        return Union(self.var1, self.var2, self.var3, self.priorite)


class Intersection(ContrainteTernaire):

    def __init__(self, var1, var2, var3, priorite):
        super().__init__(" Intersection ", var1, var2, var3, priorite)

    def validation_contrainte(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var3 = get_var(variables, self.var3)
        return var1.borneInf == var2.borneInf.intersection(var3.borneInf)

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var3 = get_var(variables, self.var3)
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

    def duplicate(self):
        return Intersection(self.var1, self.var2, self.var3, self.priorite)


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
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var3 = get_var(variables, self.var3)
        var4 = get_var(variables, self.var4)
        return var1.borneInf == var2.borneInf.intersection(var3.borneInf).intersection(var4.borneInf)

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var3 = get_var(variables, self.var3)
        var4 = get_var(variables, self.var4)
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

    def duplicate(self):
        return Intersection3(self.var1, self.var2, self.var3, self.var4, self.priorite)


class Inclusion(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" Inclusion ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        return all([e in var2.borneInf for e in var1.borneInf])

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var1tmp = var1.duplicate()
        var2tmp = var2.duplicate()

        var1.borneSup &= var2.borneSup
        var2.borneInf |= var1.borneInf

        if not (var1.valide() and var2.valide()):
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp

    def duplicate(self):
        return Inclusion(self.var1, self.var2, self.priorite)


class Exclusion(ContrainteBinaire):

    def __init__(self, var1, var2, priorite):
        super().__init__(" Exclusion ", var1, var2, priorite)

    def validation_contrainte(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        return all([e not in var2.borneInf for e in var1.borneInf])

    def filtre(self, variables):
        var1 = get_var(variables, self.var1)
        var2 = get_var(variables, self.var2)
        var1tmp = var1.duplicate()
        var2tmp = var2.duplicate()

        var1.borneSup &= var2.borneSup
        var2.borneInf |= var1.borneInf

        var1.borneSup -= var2.borneInf
        var2.borneSup -= var1.borneInf

        if not (var1.valide() and var2.valide()):
            raise ContraiteException(f'Contrainte "{self}" insatisfiable')
        return var1 != var1tmp or var2 != var2tmp

    def duplicate(self):
        return Exclusion(self.var1, self.var2, self.priorite)
