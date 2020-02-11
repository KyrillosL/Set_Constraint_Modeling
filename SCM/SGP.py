# from pprint import pprint
#
# from SCM.contraintes import Cardinalite, Intersection, Intersection4
# from SCM.ensemble import Ensemble
# from SCM.solveur import propagation, FinRechercheException
#
#
# def get_num_var(variable, nom):
#     for i, v in enumerate(variable):
#         if v.nom == nom:
#             return i
#     raise Exception(f'Variable "{nom}" not found')
#
#
# def launch_SGP(n_groupe=3, n_semaine=3, n_golfeur_groupe=3, n_golfeur=9, une_solution=True):
#     ensembles = []
#     contraintes = []
#
#     liste_noms_ensembles = [str(s) + "_" + str(g) for g in range(n_groupe) for s in range(n_semaine)]
#
#     ensembles.append(Ensemble('n_golfeur_groupe', domaine=n_golfeur_groupe, const=True))
#     ensembles.append(Ensemble('vide', domaine=set(), const=True))
#
#     for nom in liste_noms_ensembles:
#         ensembles.append(Ensemble(nom, domaine=set(list(range(n_golfeur))), const=False))
#
#     pprint(liste_noms_ensembles)
#
#     for i, nom in enumerate(liste_noms_ensembles):
#         contraintes.append(Cardinalite(get_num_var(ensembles, nom), get_num_var(ensembles, 'n_golfeur_groupe'), 1))
#
#     for s in range(n_semaine):
#         for g1 in range(n_groupe - 1):
#             for g2 in range(g1 + 1, n_groupe):
#                 nom = f'{s}_{g1}'
#                 nom1 = f'{s}_{g2}'
#                 contraintes.append(Intersection(get_num_var(ensembles, 'vide'), get_num_var(ensembles, nom),
#                                                 get_num_var(ensembles, nom1), 2))
#
#     for s1 in range(n_semaine - 1):
#         for s2 in range(s1 + 1, n_semaine):
#             for g1 in range(n_groupe - 1):
#                 for g2 in range(g1 + 1, n_groupe):
#                     nom1 = f'{s1}_{g1}'
#                     nom2 = f'{s1}_{g2}'
#                     nom3 = f'{s2}_{g1}'
#                     nom4 = f'{s2}_{g2}'
#                     contraintes.append(Intersection4(
#                             get_num_var(ensembles, 'vide'),
#                             get_num_var(ensembles, nom1),
#                             get_num_var(ensembles, nom2),
#                             get_num_var(ensembles, nom3),
#                             get_num_var(ensembles, nom4),
#                             2))
#
#     solutions = []
#
#     pprint(contraintes)
#     contraintes.sort(key=lambda x: x.priorite, reverse=False)
#
#     try:
#         propagation(ensembles, contraintes, solutions, 0, une_solution=une_solution)
#     except FinRechercheException as e:
#         print(e)
#
#     nb_solution = len(solutions)
#     print(f'{nb_solution} solutions :')
#     for i, sol in enumerate(solutions):
#         print(f'solution {i + 1}/{nb_solution}')
#         pprint(sol)
#
#
# if __name__ == "__main__":
#     import time
#
#     start_time = time.time()
#     launch_SGP(n_groupe=3, n_semaine=3, n_golfeur_groupe=3, n_golfeur=9, une_solution=True)
#     print("--- %s seconds ---" % (time.time() - start_time))
