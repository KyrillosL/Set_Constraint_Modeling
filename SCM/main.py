from pprint import pprint

from termcolor import colored

from SCM.contraintes import *
from SCM.ensemble import Ensemble
from SCM.solveur import propagation, FinRechercheException


def creation_rencontres(n=8):
    return [(i, j) for i in range(0, n) for j in range(i, n) if i != j]


def conditions(n=8):
    s = n - 1
    p = n // 2
    r = creation_rencontres(n)
    return n, s, p, r


def affiche_conditions(n, s, p, r):
    print(f'Conditions de la recherche de planification:')
    print(f'Nombre d\'équipes en jeu : {n}')
    print(f'Nombre de semaines : {s}')
    print(f'Nombre de périodes : {p}')
    print(f'Rencontres : {r}')
    print("Semaines :")
    for i in range(s):
        print(f's{i} : {r[i * p:i * p + p]}')
    print("Périodes :")
    for i in range(p):
        print(f'p{i} : {r[i::p]}')


def r_to_m(r, s, p):
    return [r[i * p:i * p + p] for i in range(s)]


def solution_to_matrice(sol, n, s, p):
    m = r_to_m([None for i in range(0, n) for j in range(i, n) if i != j], s, p)
    for v in sol:
        split = v.nom.split('_')
        if len(split) == 2:
            ligne = int(split[0])
            colonne = int(split[1])
            m[ligne][colonne] = tuple(v.borneInf)
    return m


def get_num_var(variable, nom):
    for i, v in enumerate(variable):
        if v.nom == nom:
            return i
    raise Exception(f'Variable "{nom}" not found')


# def main0():
#     variables = {
#             'A'    : Ensemble('A', domaine={1, 2}, const=False),
#             'B'    : Ensemble('B', domaine={1, 2}, const=False),
#             'card1': Ensemble('card1', domaine=1, const=True),
#             # 'c': Ensemble('c', domaine={4}, const=True)
#     }
#
#     contraintes = [
#             Cardinalite('A', 'card1'),
#             Cardinalite('B', 'card1'),
#             Different('A', 'B')
#     ]
#
#     solutions = []
#
#     propagation(variables, contraintes, solutions, 0)
#
#     print('Variables :')
#     pprint(variables)
#     print('Contraintes')
#     pprint(contraintes)
#     nb_solution = len(solutions)
#     print(f'{nb_solution} solutions :')
#     for i, sol in enumerate(solutions):
#         print(colored(f'solution {i}/{nb_solution}', 'green'))
#         pprint(sol)


def main6equipes():
    n, s, p, r = conditions(10)
    affiche_conditions(n, s, p, r)
    variables = []
    contraintes = []

    liste_noms_variables = [str(ss) + "_" + str(pp) for pp in range(p) for ss in range(s)]

    for nom in liste_noms_variables:
        variables.append(Ensemble(nom, domaine=set(list(range(n))), const=False))

    variables.append(Ensemble('card2', domaine=2, const=True))
    variables.append(Ensemble('vide', domaine=set(), const=True))

    # Contraintes d'unicite
    for i, nom in enumerate(liste_noms_variables):
        contraintes.append(Cardinalite(get_num_var(variables, nom), get_num_var(variables, 'card2'), 1))
        for nom1 in liste_noms_variables[i + 1:]:
            if nom != nom1:
                contraintes.append(Different(get_num_var(variables, nom), get_num_var(variables, nom1), 2))

    # Contrainte semaines
    for i, nom in enumerate(liste_noms_variables):
        for nom1 in liste_noms_variables[i + 1:]:
            if nom[0] == nom1[0]:
                if nom[-1] != nom1[-1]:
                    contraintes.append(Intersection(get_num_var(variables, 'vide'), get_num_var(variables, nom),
                                                    get_num_var(variables, nom1), 2))

    # Contrainte periode
    for nom in liste_noms_variables:
        for nom1 in liste_noms_variables:
            for nom2 in liste_noms_variables:
                if nom != nom1 and nom != nom2 and nom1 != nom2 and nom < nom1 < nom2:
                    if nom[-1] == nom1[-1] == nom2[-1]:
                        contraintes.append(Intersection3(get_num_var(variables, 'vide'), get_num_var(variables, nom),
                                                         get_num_var(variables, nom1), get_num_var(variables, nom2), 2))
                        # print(nom, nom1, nom2)

    # Cassage de sysmetrie
    for i, j in enumerate(range(0, n, 2)):
        variables.append(Ensemble('s1=' + str((j, j + 1)), domaine={j, j + 1}, const=True))
        contraintes.append(
                Egal(get_num_var(variables, '0_' + str(i)), get_num_var(variables, 's1=' + str((j, j + 1))), 0))

    # [[(2, 4), (1, 5), (0, 3)],
    #  [(3, 4), (0, 5), (1, 2)],
    #  [(2, 5), (0, 4), (1, 3)],
    #  [(3, 5), (1, 4), (0, 2)],
    #  [(0, 1), (2, 3), (4, 5)]] ok

    # variables.append(Ensemble('s2=(3, 5)', domaine={3, 5}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '1_0'), get_num_var(variables, 's2=(3, 5)'), 0))
    # variables.append(Ensemble('s2=(1, 4)', domaine={1, 4}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '1_1'), get_num_var(variables, 's2=(1, 4)'), 0))
    # variables.append(Ensemble('s2=(0, 2)', domaine={0, 2}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '1_2'), get_num_var(variables, 's2=(0, 2)'), 0))
    #
    # variables.append(Ensemble('s2=(2, 5)', domaine={2, 5}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '2_0'), get_num_var(variables, 's2=(2, 5)'), 0))
    # variables.append(Ensemble('s2=(0, 4)', domaine={0, 4}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '2_1'), get_num_var(variables, 's2=(0, 4)'), 0))
    # variables.append(Ensemble('s2=(1, 3)', domaine={1, 3}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '2_2'), get_num_var(variables, 's2=(1, 3)'), 0))

    # variables.append(Ensemble('s2=(3, 4)', domaine={3, 4}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '3_0'), get_num_var(variables, 's2=(3, 4)'), 0))
    # variables.append(Ensemble('s2=(0, 5)', domaine={0, 5}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '3_1'), get_num_var(variables, 's2=(0, 5)'), 0))
    # variables.append(Ensemble('s2=(1, 2)', domaine={1, 2}, const=True))
    # contraintes.append(Egal(get_num_var(variables, '3_2'), get_num_var(variables, 's2=(1, 2)'), 0))

    solutions = []

    contraintes.sort(key=lambda x: x.priorite, reverse=True)

    try:
        propagation(variables, contraintes, solutions, 0, une_seule_solution=True)
    except FinRechercheException as e:
        print(e)

    # print('Variables :')
    # pprint(variables)
    #
    # print('Contraintes')
    # pprint(contraintes)
    nb_solution = len(solutions)
    print(f'{nb_solution} solutions :')
    solutions_matrice = []
    for i, sol in enumerate(solutions):
        print(colored(f'solution {i + 1}/{nb_solution}', 'green'))
        m = solution_to_matrice(sol, n, s, p)
        solutions_matrice.append(m)
        pprint(m)


if __name__ == "__main__":
    import time

    start_time = time.time()
    main6equipes()
    print("--- %s seconds ---" % (time.time() - start_time))

# --- 200.709454536438 seconds --- pour len(diff_...)
#  pour 8 coeurs
