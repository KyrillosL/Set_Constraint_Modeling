from abc import ABC, abstractmethod
from copy import deepcopy

from termcolor import colored


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


def propagation(variables, contraintes, solutions, profondeur):
    # filtrage()
    print(f'p{profondeur} variables : {variables}')
    # split si le split est possible sinon il y a une solution
    a_tester, la_suite = coupe(variables)
    if a_tester != None:
        propagation(a_tester, contraintes, solutions, profondeur + 1)
    if la_suite != None:
        propagation(la_suite, contraintes, solutions, profondeur + 1)
    # on teste les contraintes
    if all([v[1].impossible_a_couper() for v in variables.items()]):
        if all([not v[1].vide() for v in variables.items()]):
            for c in contraintes:
                print("CONTRAINTES")
                print(variables)
                rc = c(variables)
                print(rc)
                if not rc:
                    print(colored(f'\tno', 'red'))
                    return
            print(colored(f'\tappend : {variables}', 'green'))
            solutions.append(variables)


def coupe(variables):
    print(f'\tcoupe : {variables}')
    for i, v in enumerate(variables):
        print(f'\tv : {variables[v]}')
        if not variables[v].impossible_a_couper():
            print("\t\ton coupe")
            part1 = deepcopy(variables)
            part2 = deepcopy(variables)
            element_a_garder = part2[v].domaine.pop()
            part1[v].domaine = {element_a_garder}
            print(f'\t\tpart1 : {part1}\n\t\tpart2 : {part2}')
            return part1, part2
    return None, None


a = Variable(set(range(3, 8)))
b = Variable(set(range(2, 4)))
x = Variable(set(range(5)))
y = Variable(set(range(2, 7)))
z = Variable(set(range(1, 7)))
w = Variable(set(range(1, 7)))

variables = {'x': x, 'y': y, 'z': z, 'w': w, 'a': a, 'b': b}

contraintes = [Egal("z", Union("x", "y")), Egal("w", Intersection("a", "b"))]

solutions = list()

propagation(variables, contraintes, solutions, 0)

print("Solutions : ")
for s in solutions:
    print(colored(s,"green", attrs=['blink']))
