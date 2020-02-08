from pprint import pprint

from SCM.contraintes import Cardinalite, Different, Egal, Intersection, Intersection3
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


def launch_STS(n, une_solution):
    n, s, p, r = conditions(n)
    affiche_conditions(n, s, p, r)
    ensembles = []
    contraintes = []

    liste_noms_ensembles = [str(ss) + "_" + str(pp) for pp in range(p) for ss in range(s)]

    for nom in liste_noms_ensembles:
        ensembles.append(Ensemble(nom, domaine=set(list(range(n))), const=False))

    ensembles.append(Ensemble('card2', domaine=2, const=True))
    ensembles.append(Ensemble('vide', domaine=set(), const=True))

    # Contraintes d'unicite
    for i, nom in enumerate(liste_noms_ensembles):
        contraintes.append(Cardinalite(get_num_var(ensembles, nom), get_num_var(ensembles, 'card2'), 1))
        for nom1 in liste_noms_ensembles[i + 1:]:
            if nom != nom1:
                contraintes.append(Different(get_num_var(ensembles, nom), get_num_var(ensembles, nom1), 2))

    # Contrainte semaines
    for i, nom in enumerate(liste_noms_ensembles):
        for nom1 in liste_noms_ensembles[i + 1:]:
            if nom[0] == nom1[0]:
                if nom[-1] != nom1[-1]:
                    contraintes.append(Intersection(get_num_var(ensembles, 'vide'), get_num_var(ensembles, nom),
                                                    get_num_var(ensembles, nom1), 2))

    # Contrainte periode
    for nom in liste_noms_ensembles:
        for nom1 in liste_noms_ensembles:
            for nom2 in liste_noms_ensembles:
                if nom != nom1 and nom != nom2 and nom1 != nom2 and nom < nom1 < nom2:
                    if nom[-1] == nom1[-1] == nom2[-1]:
                        contraintes.append(Intersection3(get_num_var(ensembles, 'vide'), get_num_var(ensembles, nom),
                                                         get_num_var(ensembles, nom1), get_num_var(ensembles, nom2), 2))

    # Cassage de sysmetrie
    for i, j in enumerate(range(0, n, 2)):
        ensembles.append(Ensemble('s1=' + str((j, j + 1)), domaine={j, j + 1}, const=True))
        contraintes.append(
                Egal(get_num_var(ensembles, '0_' + str(i)), get_num_var(ensembles, 's1=' + str((j, j + 1))), 0))

    solutions = []

    contraintes.sort(key=lambda x: x.priorite, reverse=False)

    try:
        propagation(ensembles, contraintes, solutions, 0, une_solution=une_solution)
    except FinRechercheException as e:
        print(e)

    nb_solution = len(solutions)
    print(f'{nb_solution} solutions :')
    for i, sol in enumerate(solutions):
        print(f'solution {i + 1}/{nb_solution}')
        m = solution_to_matrice(sol, n, s, p)
        pprint(m)


if __name__ == "__main__":
    import time

    start_time = time.time()
    launch_STS(8, True)
    print("--- %s seconds ---" % (time.time() - start_time))
