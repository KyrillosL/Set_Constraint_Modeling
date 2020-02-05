from pprint import pprint

from termcolor import colored

from SCM.contraintes import *
from SCM.ensemble import Ensemble
from SCM.outils import *
from SCM.solveur import propagation, FinRechercheException


def solution_to_matrice(sol, n, s, p):
    m = r_to_m([None for i in range(0, n) for j in range(i, n) if i != j], s, p)
    for nom in sol.items():
        split = nom[0].split('_')
        if len(split) == 2:
            ligne = int(split[0])
            colonne = int(split[1])
            m[ligne][colonne] = tuple(nom[1].borneInf)
    return m


def main0():
    variables = {
            'A'    : Ensemble('A', domaine={1, 2}, const=False),
            'B'    : Ensemble('B', domaine={1, 2}, const=False),
            'card1': Ensemble('card1', domaine=1, const=True),
            # 'c': Ensemble('c', domaine={4}, const=True)
    }

    contraintes = [
            Cardinalite('A', 'card1'),
            Cardinalite('B', 'card1'),
            Different('A', 'B')
    ]

    solutions = []

    propagation(variables, contraintes, solutions, 0)

    print('Variables :')
    pprint(variables)
    print('Contraintes')
    pprint(contraintes)
    nb_solution = len(solutions)
    print(f'{nb_solution} solutions :')
    for i, sol in enumerate(solutions):
        print(colored(f'solution {i}/{nb_solution}', 'green'))
        pprint(sol)


def main6equipes():
    n, s, p, r = conditions(6)
    affiche_conditions(n, s, p, r)
    variables = {}
    contraintes = []

    liste_noms_variables = [str(ss) + "_" + str(pp) for pp in range(p) for ss in range(s)]

    for nom in liste_noms_variables:
        variables[nom] = Ensemble(nom, domaine=set(list(range(n))), const=False)

    variables['card2'] = Ensemble('card2', domaine=2, const=True)
    variables['vide'] = Ensemble('vide', domaine=set(), const=True)

    # Contraintes d'unicite
    for i, nom in enumerate(liste_noms_variables):
        contraintes.append(Cardinalite(nom, 'card2', 1))
        for nom1 in liste_noms_variables[i + 1:]:
            if nom != nom1:
                contraintes.append(Different(nom, nom1, 2))

    # Contrainte semaines
    for i, nom in enumerate(liste_noms_variables):
        for nom1 in liste_noms_variables[i + 1:]:
            if nom[0] == nom1[0]:
                if nom[-1] != nom1[-1]:
                    contraintes.append(Intersection('vide', nom, nom1, 2))

    # Contrainte periode
    for nom in liste_noms_variables:
        for nom1 in liste_noms_variables:
            for nom2 in liste_noms_variables:
                if nom != nom1 and nom != nom2 and nom1 != nom2 and nom < nom1 < nom2:
                    if nom[-1] == nom1[-1] == nom2[-1]:
                        contraintes.append(Intersection3('vide', nom, nom1, nom2, 2))
                        # print(nom, nom1, nom2)

    # Cassage de sysmetrie
    for i, j in enumerate(range(0, n, 2)):
        variables['s1=' + str((j, j + 1))] = Ensemble('s1=' + str((j, j + 1)), domaine={j, j + 1}, const=True)
        contraintes.append(Egal('0_' + str(i), 's1=' + str((j, j + 1)), 0))

    # [[(2, 4), (1, 5), (0, 3)],
    #  [(3, 4), (0, 5), (1, 2)],
    #  [(2, 5), (0, 4), (1, 3)],
    #  [(3, 5), (1, 4), (0, 2)],
    #  [(0, 1), (2, 3), (4, 5)]]

    variables['s2=(3, 5)'] = Ensemble('s2=(3, 5)', domaine={3, 5}, const=True)
    contraintes.append(Egal('1_0', 's2=(3, 5)', 0))
    variables['s2=(1, 4)'] = Ensemble('s2=(1, 4)', domaine={1, 4}, const=True)
    contraintes.append(Egal('1_1', 's2=(1, 4)', 0))
    variables['s2=(0, 2)'] = Ensemble('s2=(0, 2)', domaine={0, 2}, const=True)
    contraintes.append(Egal('1_2', 's2=(0, 2)', 0))

    variables['s2=(2, 5)'] = Ensemble('s2=(2, 5)', domaine={2, 5}, const=True)
    contraintes.append(Egal('2_0', 's2=(2, 5)', 0))
    variables['s2=(0, 4)'] = Ensemble('s2=(0, 4)', domaine={0, 4}, const=True)
    contraintes.append(Egal('2_1', 's2=(0, 4)', 0))
    variables['s2=(1, 3)'] = Ensemble('s2=(1, 3)', domaine={1, 3}, const=True)
    contraintes.append(Egal('2_2', 's2=(1, 3)', 0))

    variables['s2=(3, 4)'] = Ensemble('s2=(3, 4)', domaine={3, 4}, const=True)
    contraintes.append(Egal('3_0', 's2=(3, 4)', 0))
    variables['s2=(0, 5)'] = Ensemble('s2=(0, 5)', domaine={0, 5}, const=True)
    contraintes.append(Egal('3_1', 's2=(0, 5)', 0))
    # variables['s2=(1, 2)'] = Ensemble('s2=(1, 2)', domaine={1, 2}, const=True)
    # contraintes.append(Egal('3_2', 's2=(1, 2)', 0))
    solutions = []

    contraintes.sort(key=lambda x: x.priorite, reverse=False)

    print('Contraintes')
    pprint(contraintes)
    try:
        propagation(variables, contraintes, solutions, 0, une_seule_solution=False)
    except FinRechercheException:
        pass

    print('Variables :')
    pprint(variables)
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
