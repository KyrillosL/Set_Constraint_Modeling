# from abc import ABC, abstractmethod
#
#
# # class ContrainteUnaire(Contrainte):
# #
#
#
# class Variable:
#
#     def __init__(self, domaine):
#         self.domaine = domaine
#
#     def vide(self):
#         return self.domaine == set()
#
#     def impossible_a_couper(self):
#         return len(self.domaine) <= 1
#
#     def __repr__(self):
#         return self.__str__()
#
#     def __str__(self):
#         return str(self.domaine)
#
#
# class Contrainte(ABC):
#
#     def __init__(self, contrainte):
#         self.contrainte = contrainte
#
#     def __repr__(self):
#         return self.__str__()
#
#     def __str__(self):
#         return self.contrainte
#
#     @abstractmethod
#     def __call__(self, variables):
#         pass
#
#
# class ContrainteBinaire(Contrainte):
#
#     def __init__(self, contrainte, var1, var2):
#         super().__init__(contrainte)
#         self.var1 = var1
#         self.var2 = var2
#
#     def __str__(self):
#         return str(self.var1) + self.contrainte + str(self.var2)
#
#
# class ContrainteTernaire(Contrainte):
#
#     def __init__(self, contrainte, var1, var2, var3):
#         super().__init__(contrainte)
#         self.var1 = var1
#         self.var2 = var2
#         self.var3 = var3
#
#     def __str__(self):
#         return str(self.var1) + " = " + str(self.var2) + self.contrainte + str(self.var3)
#
#
# class Union(ContrainteTernaire):
#
#     def __init__(self, var1, var2, var3):
#         super().__init__(" Union ", var1, var2, var3)
#
#     def __call__(self, variables):
#         print(self)
#         var1 = variables[self.var1]
#         var2 = variables[self.var2]
#         var3 = variables[self.var3]
#
#         return var1.domaine == var2.domaine.union(var3.domaine)
#
#
# class Intersection(ContrainteTernaire):
#
#     def __init__(self, var1, var2, var3):
#         super().__init__(" Intersection ", var1, var2, var3)
#
#     def __call__(self, variables):
#         print(self)
#         var1 = variables[self.var1]
#         var2 = variables[self.var2]
#         var3 = variables[self.var3]
#
#         return var1.domaine == var2.domaine.intersection(var3.domaine)
#
#
# class Inclusion(ContrainteBinaire):
#
#     def __init__(self, var1, var2):
#         super().__init__(" Inclusion ", var1, var2)
#
#     def __call__(self, variables):
#         print(self)
#         var1 = variables[self.var1]
#         var2 = variables[self.var2]
#
#         return all([e not in var2.domaine for e in var1.domaine])
#
#
# class Filtre(ABC):
#
#     def __init__(self, filtre):
#         self.filtre = filtre
#
#     def __repr__(self):
#         return self.__str__()
#
#     def __str__(self):
#         return str(self.filtre)
#
#     @abstractmethod
#     def __call__(self, variables):
#         pass
#
#
# class FUnion(Filtre):
#
#     def __call__(self, variables):
#
#         tmpC = C.copy()
#         C.borneInf |= (A.borneInf | B.borneInf)
#         C.borneSup &= (A.borneSup | B.borneSup)
#         if not C.verification():
#             raise Exception("Contrainte insatisfiable")
#         return tmpC != C
#
#     @staticmethod
#     def union(A, B, C):
#         tmpC = C.copy()
#         C.borneInf |= (A.borneInf | B.borneInf)
#         C.borneSup &= (A.borneSup | B.borneSup)
#         if not C.verification():
#             raise Exception("Contrainte insatisfiable")
#         return tmpC != C
#
#     @staticmethod
#     def intersection(A, B, C):
#         tmpA = A.copy()
#         tmpB = B.copy()
#         tmpC = C.copy()
#         C.borneInf |= (A.borneInf & B.borneInf)
#         A.borneInf |= C.borneInf
#         B.borneInf |= C.borneInf
#         C.borneSup &= (A.borneSup | B.borneSup)
#         if not (A.verification() and B.verification() and C.verification()):
#             raise Exception("Contrainte insatisfiable")
#         return tmpA != A or tmpB != B or tmpC != C
#
#     @staticmethod
#     def inclusion(A, B):
#         tmpA = A.copy()
#         tmpB = B.copy()
#         A.borneSup &= B.borneSup
#         B.borneInf |= A.borneInf
#         if not (A.verification() and B.verification()):
#             raise Exception("Contrainte insatisfiable")
#         return tmpA != A or tmpB != B
#
#     @staticmethod
#     def exclusion(A, B):
#         tmpA = A.copy()
#         tmpB = B.copy()
#         A.borneSup -= B.borneInf
#         B.borneSup -= A.borneInf
#         if not A.verification():
#             raise Exception("Contrainte insatisfiable 'A'")
#         if not B.verification():
#             raise Exception("Contrainte insatisfiable 'B'")
#         return tmpA != A or tmpB != B
#
#
# class Ensemble:
#     def __init__(self, domaine={}, const=False):
#         self.borneSup = domaine
#         if const:
#             self.borneInf = domaine
#         else:
#             self.borneInf = set()
#
#     def verification(self):
#         for element in self.borneInf:
#             if element not in self.borneSup:
#                 return False
#         return True
#
#     def split(self):
#         S = []
#         E = self.borneSup - self.borneInf
#         for i in range(0, 2 ** len(E)):
#             v = 1
#             s = set()
#             for n in E:
#                 if v & i:
#                     s.add(n)
#                 v += 1
#             s.update(self.borneInf)
#             S.append(s)
#         return S
#
#     def __str__(self):
#         return "Borne Inferieur = " + str(self.borneInf) + " / Borne Supperieur = " + str(self.borneSup)
#
#     def __eq__(self, value):
#         return self.borneInf == value.borneInf and self.borneSup == value.borneSup
#
#     def __ne__(self, value):
#         return not self == value
#
#     def copy(self):
#         ensemble = Ensemble()
#         ensemble.borneInf = self.borneInf.copy()
#         ensemble.borneSup = self.borneSup.copy()
#         return ensemble




def propagation_0(variables, contraintes, solutions, profondeur):
    filtrage(variables, contraintes)
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


def run():
    a = Variable(trellis(set(range(3, 8))))
    b = Variable(trellis(set(range(2, 4))))
    x = Variable(trellis(set(range(3))))
    y = Variable(trellis(set(range(3))))
    z = Variable(trellis(set(range(3))))
    w = Variable(trellis(set(range(1, 7))))

    variables = {'x': x, 'y': y, 'z': z}  # , 'w': w, 'a': a, 'b': b}

    contraintes = [Intersection('z', 'x', 'y')]

    solutions = list()

    propagation(variables, contraintes, solutions, 0)

    print("Solutions : ")
    for s in solutions:
        print(colored(s, "green", attrs=['blink']))

# def STS(nb_equipes=6):
#     nb_semaines = nb_equipes - 1
#     nb_periodes = nb_equipes // 2
#     rencontres = [(i, j) for i in range(0, nb_equipes) for j in range(i, nb_equipes) if i != j]
#
#     variables = {}
#
#     for s in range(nb_semaines):
#         for p in range(nb_periodes):
#             v = Variable()
#             variables.add(f'planning_{s}_{j}', v)


# if __name__ == "__main__":
#     A = Ensemble(set(range(1, 4)))
#     B = Ensemble(set(range(2, 5)))
#     Const = Ensemble(set({2}), const=True)
#     Const3 = Ensemble(set({3}), const=True)
#     Vide = Ensemble()
#
#     flags = True
#     n = 1
#     while flags:
#         flags = False
#         print(f"passe {n}")
#         n += 1
#         flags = flags or Contrainte.intersection(A, B, Const)
#         flags = flags or Contrainte.exclusion(A, Const3)
#
#     print(A)
#     print(B)
#     print(Const)
#     print(Const3)
#     L = A.split()
#     print(L)
