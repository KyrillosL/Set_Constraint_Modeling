from copy import deepcopy

from termcolor import colored

from SCM.contraintes import ContraiteException
from SCM.ensemble import Ensemble


# import pickle
#
#
# def deepcopy(a):
#     return pickle.loads(pickle.dumps(a, -1))


class FinRechercheException(Exception):
    pass


def filtrage(variables, contraintes):
    filtrage_ok = True
    try:
        modif = True
        while modif:
            modif = False
            for contrainte in contraintes:
                modif = modif or contrainte.filtre(variables)
    except ContraiteException:
        filtrage_ok = False
    except Exception as e:
        print('coucou')
        print(e)
    return filtrage_ok


def lance_propa(old, d, variables, contraintes, solutions, profondeur, une_seule_solution, to_split):
    e = Ensemble(old.nom, domaine=d, const=True)
    variables[to_split] = e
    # print(colored(variables, 'blue'))
    propagation(deepcopy(variables), contraintes, solutions, profondeur + 1,
                une_seule_solution=une_seule_solution)


def coupe(variables, contraintes, solutions, profondeur, une_seule_solution=False):
    # Si certaines variables ne sont pas des constantes :
    if any([not variables[v].const for v in variables]):
        # print('on peut couper une variable')
        to_split = None
        # On cherche quelle variable peut etre coupee
        # print(variables)
        for i, v in enumerate(variables.items()):
            if not variables[v[0]].const:
                to_split = v[0]
        # print(f'to split : {to_split} : {variables[to_split]}')
        diff_domaines = variables[to_split].split()
        # print(colored(diff_domaines, 'red'))
        old = variables.pop(to_split)

        # if profondeur <= 0:
        #     from joblib import Parallel, delayed
        #     backend = 'loky'  # 'loky' 'threading' 'multiprocessing'
        #     Parallel(n_jobs=len(diff_domaines), backend=backend)(
        #             delayed(lance_propa)(old, d, variables, contraintes, solutions, profondeur, une_seule_solution,
        #                                  to_split) for d in diff_domaines)
        # else:
        for d in diff_domaines:
            e = Ensemble(old.nom, domaine=d, const=True)
            variables[to_split] = e
            # print(colored(variables, 'blue'))
            propagation(deepcopy(variables), contraintes, solutions, profondeur + 1,
                        une_seule_solution=une_seule_solution)
        variables[to_split] = old


def verification_contraintes(variables, contraintes, solutions):
    # on teste les contraintes si toutes les variables sont des constantes
    if all([variables[v[0]].const for v in variables.items()]):
        for c in contraintes:
            # print("CONTRAINTES")
            # print(variables)
            # print(c)
            rc = c.validation_contrainte(variables)
            # print(rc)
            if not rc:
                # print(colored(f'\tno', 'red'))
                return False
        return True
    return False


def propagation(variables, contraintes, solutions, profondeur, une_seule_solution=False):
    # if profondeur < 3:
    #     print(f'p{profondeur} variables : {variables}')

    # filtrage des variables
    filtrage_ok = filtrage(variables, contraintes)

    if filtrage_ok:
        coupe(variables, contraintes, solutions, profondeur, une_seule_solution=une_seule_solution)

        contraintes_ok = verification_contraintes(variables, contraintes, solutions)

        if contraintes_ok:
            solutions.append(deepcopy(variables))
            print(colored(f'\tsolution {len(solutions)} : {variables}', 'green'))
            if une_seule_solution:
                raise FinRechercheException()
