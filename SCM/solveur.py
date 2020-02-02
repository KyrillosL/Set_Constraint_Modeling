from copy import deepcopy

from termcolor import colored

from SCM.ensemble import Ensemble


def filtrage(variables, contraintes):
    modif = True
    while modif:
        modif = False
        for contrainte in contraintes:
            modif = modif or contrainte.filtre(variables)


def coupe(variables):
    print(f'\tcoupe : {variables}')
    for i, v in enumerate(variables):
        print(f'\tv : {variables[v]}')
        if not variables[v].impossible_a_couper():
            print("\t\ton coupe")
            part1 = deepcopy(variables)
            part2 = deepcopy(variables)
            element_a_garder = part2[v].domaine.pop()
            part1[v].domaine = element_a_garder
            print(f'\t\tpart1 : {part1}\n\t\tpart2 : {part2}')
            return part1, part2
    return None, None


def propagation(variables, contraintes, solutions, profondeur):
    # filtrage des variables
    filtrage(variables, contraintes)

    print(f'p{profondeur} variables : {variables}')

    # Si certaines variables ne sont pas des constantes :
    if any([not variables[v].const for v in variables]):
        print('on peut couper une variable')
        to_split = None
        # On cherche quelle variable peut etre coupee
        print(variables)
        for i, v in enumerate(variables.items()):
            if not variables[v[0]].const:
                to_split = v[0]
        diff_domaines = variables[to_split].split()
        old = variables.pop(to_split)
        for d in diff_domaines:
            e = Ensemble(old.nom, domaine=d, const=True)
            variables[to_split] = e
            propagation(variables, contraintes, solutions, profondeur + 1)

    # on teste les contraintes si toutes les variables sont des constantes
    if all([variables[v[0]].const for v in variables.items()]):
        for c in contraintes:
            print("CONTRAINTES")
            print(variables)
            print(c)
            rc = c.validation_contrainte(variables)
            print(rc)
            if not rc:
                print(colored(f'\tno', 'red'))
                return
        print(colored(f'\tappend : {variables}', 'green'))
        solutions.append(variables)
