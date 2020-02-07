from termcolor import colored

from SCM.contraintes import ContraiteException
from SCM.ensemble import Ensemble


class FinRechercheException(Exception):
    pass


def filtrage(variables, contraintes):
    filtrage_ok = True
    try:
        modif = True
        while modif:
            modif = False
            for contrainte in contraintes:
                # print(contrainte)
                modif = modif or contrainte.filtre(variables)
                # print(modif)
    except ContraiteException as e:
        # print(e)
        filtrage_ok = False
    return filtrage_ok


def joblib_launch(d, to_split, var, old, contr, solutions, profondeur, une_seule_solution):
    e = Ensemble(to_split.nom, domaine=d, const=True)
    var[old] = e
    new_var = []
    for v in var:
        new_var.append(v.duplicate())
    propagation(new_var, contr, solutions, profondeur + 1,
                une_seule_solution=une_seule_solution)


def coupe(variables, contraintes, solutions, profondeur, une_seule_solution=False):
    # Si certaines variables ne sont pas des constantes :
    if any([not v.const for v in variables]):
        # On cherche quelle variable peut etre coupee
        liste_rank = [len(x.borneSup) - len(x.borneInf) for x in variables]
        liste_noms = [x.nom for x in variables]
        _, nouvelle_liste_nom, var = zip(*sorted(zip(liste_rank, liste_noms, variables)))
        var = list(var)
        contr = []
        for c in contraintes:
            contr.append(c.duplicate())
        for c in contr:
            if hasattr(c, 'var1'):
                c.var1 = nouvelle_liste_nom.index(liste_noms[c.var1])
                if hasattr(c, 'var2'):
                    c.var2 = nouvelle_liste_nom.index(liste_noms[c.var2])
                    if hasattr(c, 'var3'):
                        c.var3 = nouvelle_liste_nom.index(liste_noms[c.var3])
                        if hasattr(c, 'var4'):
                            c.var4 = nouvelle_liste_nom.index(liste_noms[c.var4])
        to_split = next(v for v in var if not v.const)
        diff_domaines = to_split.split()
        old = var.index(to_split)
        if profondeur == -1:
            from joblib import Parallel, delayed
            backend = 'loky'  # 'loky' 'threading' 'multiprocessing'
            Parallel(n_jobs=len(diff_domaines), backend=backend)(
                    delayed(joblib_launch)(d, to_split, var, old, contr, solutions, profondeur, une_seule_solution) for d
                    in diff_domaines)
        else:
            for d in diff_domaines:
                e = Ensemble(to_split.nom, domaine=d, const=True)
                var[old] = e
                new_var = []
                for v in var:
                    new_var.append(v.duplicate())
                propagation(new_var, contr, solutions, profondeur + 1,
                            une_seule_solution=une_seule_solution)
        var[old] = to_split


def verification_contraintes(variables, contraintes, solutions):
    # on teste les contraintes si toutes les variables sont des constantes
    if all([v.const for v in variables]):
        for c in contraintes:
            if not c.validation_contrainte(variables):
                return False
        return True
    return False


def propagation(variables, contraintes, solutions, profondeur, une_seule_solution=False):
    # filtrage des variables
    filtrage_ok = filtrage(variables, contraintes)

    if filtrage_ok:
        coupe(variables, contraintes, solutions, profondeur, une_seule_solution=une_seule_solution)

        contraintes_ok = verification_contraintes(variables, contraintes, solutions)

        if contraintes_ok:
            from copy import deepcopy
            solutions.append(deepcopy(variables))
            print(colored(f'\tsolution {len(solutions)} : {variables}', 'green'))
            if une_seule_solution:
                raise FinRechercheException()
