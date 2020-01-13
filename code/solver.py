from copy import deepcopy
from math import pow

from termcolor import colored
from contraintes import *


def trellis(ens):
    size_ens = len(ens)
    lst_bool = set()
    for i in range(int(pow(2, size_ens))):
        s = str(size_ens)
        ss = '{0:0' + s + 'b}'
        print(f'{i} : {ss.format(i)}')
        lst_bool.add(ss.format(i))
    print(lst_bool)
    ens = list(ens)
    tre = []
    for e in lst_bool:
        print(e)
        el = []
        for i, j in enumerate(e):
            print(f'{i} : {j}')
            if j == "1":
                el.append(ens[i])
        tre.append(set(el))
    return tre


def propagation(variables, contraintes, solutions, profondeur):
    # filtrage()
    print(f'p{profondeur} variables : {variables}')
    # split si le split est possible sinon il y a une solution
    a_tester, la_suite = coupe(variables)
    if a_tester:
        propagation(a_tester, contraintes, solutions, profondeur + 1)
    if la_suite:
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


def test():
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
        print(colored(s, "green", attrs=['blink']))


test()
