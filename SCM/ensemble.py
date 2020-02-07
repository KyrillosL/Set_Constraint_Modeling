from copy import copy as deepcopy
from math import pow


def trellis(ens):
    size_ens = len(ens)
    lst_bool = set()
    for i in range(int(pow(2, size_ens))):
        s = str(size_ens)
        ss = '{0:0' + s + 'b}'
        lst_bool.add(ss.format(i))
    ens = list(ens)
    tre = []
    for e in lst_bool:
        # print(e)
        el = []
        for i, j in enumerate(e):
            if j == "1":
                el.append(ens[i])
        tre.append(set(el))
    return tre


class Ensemble:

    def __init__(self, nom, domaine=None, const=False):
        self.nom = nom
        self.const = const
        if domaine is None:
            domaine = set()
        self.borneSup = domaine
        if const:
            self.borneInf = domaine
        else:
            self.borneInf = set()

    def valide(self):
        for element in self.borneInf:
            if element not in self.borneSup:
                return False
        return True

    def duplicate(self):
        new_ensemble = Ensemble(str(self.nom), {}, const=bool(self.const))
        if type(self.borneInf) == int:
            new_ensemble.borneInf = self.borneInf
            new_ensemble.borneSup = self.borneSup
        else:
            new_borne_inf = set()
            for i in self.borneInf:
                new_borne_inf.add(i)
            new_ensemble.borneInf = new_borne_inf
            new_borne_sup = set()
            for i in self.borneSup:
                new_borne_sup.add(i)
            new_ensemble.borneSup = new_borne_sup
        return new_ensemble

    # def __copy__(self):
    #     new_ensemble = Ensemble(str(self.nom), {}, const=bool(self.const))
    #     if type(self.borneInf) == int:
    #         new_ensemble.borneInf = self.borneInf
    #         new_ensemble.borneSup = self.borneSup
    #     else:
    #         new_borne_inf = set()
    #         for i in self.borneInf:
    #             new_borne_inf.add(i)
    #         new_ensemble.borneInf = new_borne_inf
    #         new_borne_sup = set()
    #         for i in self.borneSup:
    #             new_borne_sup.add(i)
    #         new_ensemble.borneSup = new_borne_sup
    #     return new_ensemble
    #
    # def __deepcopy__(self, memodict={}):
    #     new_ensemble = Ensemble(str(self.nom), {}, const=bool(self.const))
    #     if type(self.borneInf) == int:
    #         new_ensemble.borneInf = self.borneInf
    #         new_ensemble.borneSup = self.borneSup
    #     else:
    #         new_borne_inf = set()
    #         for i in self.borneInf:
    #             new_borne_inf.add(i)
    #         new_ensemble.borneInf = new_borne_inf
    #         new_borne_sup = set()
    #         for i in self.borneSup:
    #             new_borne_sup.add(i)
    #         new_ensemble.borneSup = new_borne_sup
    #     return new_ensemble

    def split(self):
        ens_fils = []
        for t in trellis(self.borneSup - self.borneInf):
            ens_fils.append(deepcopy(self.borneInf.union(t)))
        return ens_fils

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.const:
            return f'{self.nom} = {self.borneInf}'
        else:
            return f'Borne Inf : {self.borneInf} -- Borne Sup : {self.borneSup}'

    def __eq__(self, other):
        return self.borneInf == other.borneInf and self.borneSup == other.borneSup
