from pprint import pprint

from termcolor import colored

from SCM.contraintes import *
from SCM.ensemble import Ensemble
from SCM.solveur import propagation

if __name__ == "__main__":
    variables = {
            'A': Ensemble('A', domaine={1, 2, 3, 4}, const=False),
            'B': Ensemble('B', domaine={3, 4, 5, 6}, const=False),
            'c': Ensemble('c', domaine={4}, const=True)
    }

    contraintes = [
            Intersection('A', 'B', 'c')
    ]

    solutions = []

    propagation(variables, contraintes, solutions, 0)

    print('Variables :')
    pprint(variables)
    print('Contraintes')
    pprint(contraintes)
    nb_solution = len(solutions)
    print(f'{nb_solution} solutions :')
    for i, s in enumerate(solutions):
        print(colored(f'solution {i}/{nb_solution}', 'green'))
        pprint(s)
