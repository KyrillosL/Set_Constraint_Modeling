from copy import deepcopy


class Contrainte:

    def __init__(self, contrainte):
        self.contrainte = contrainte

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.contrainte


class ContrainteBinaire(Contrainte):

    def __init__(self, contrainte, var1, var2):
        super().__init__(contrainte)
        self.var1 = var1
        self.var2 = var2


class Union(ContrainteBinaire):

    def __init__(self, var1, var2):
        super().__init__(" Union ", var1, var2)
        self.var1 = var1
        self.var2 = var2


class Egal(ContrainteBinaire):

    def __init__(self, var1, var2):
        super().__init__(" = ", var1, var2)
        self.var1 = var1
        self.var2 = var2


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
    while not all([v.impossible_a_couper() for v in variables]):
        # split si le split est possible sinon il y a une solution
        a_tester, la_suite = coupe(variables)
        # propage
        # if a_tester == set() and la_suite == set():
        #     break
        # if not a_tester in solutions:
        propagation(a_tester, contraintes, solutions, profondeur + 1)
        # if not la_suite in solutions:
        propagation(la_suite, contraintes, solutions, profondeur + 1)
    # on teste les contraintes
    print(f'append : {variables}')
    solutions.append(variables)


def coupe(variables):
    print(f'\tcoupe : {variables}')
    for i, v in enumerate(variables):
        print(f'\tv : {v}')
        if not v.impossible_a_couper():
            print("\t\ton coupe")
            part1 = deepcopy(variables)
            part2 = deepcopy(variables)
            element_a_garder = part2[i].domaine.pop()
            part1[i].domaine = {element_a_garder}
            print(f'\t\tpart1 : {part1}\n\t\tpart2 : {part2}')
            return part1, part2
    return set(), set()


# x = Variable(set(range(5)))
# y = Variable(set(range(2, 7)))
# z = Variable(set(range(1, 7)))

x = Variable(set(range(3)))
y = Variable(set(range(3)))
z = Variable(set(range(3)))
variables = [x, y, z]

contraintes = [Egal(z, Union(x, y))]

solutions = list()

propagation(variables, contraintes, solutions, 0)

print(solutions)
