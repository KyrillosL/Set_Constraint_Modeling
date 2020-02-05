from copy import deepcopy
# import pickle
#
#
# def deepcopy(a):
#     return pickle.loads(pickle.dumps(a, -1))


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


def semaines_ok(m, n):
    for semaine in m:
        present = [False] * n
        for a, b in semaine:
            if present[a] or present[b]:
                return False
            present[a] = True
            present[b] = True
    return True


def periodes_ok(m_t, n):
    for periode in m_t:
        present = [0] * n
        for a, b in periode:
            present[a] += 1
            present[b] += 1
            if present[a] > 2 or present[b] > 2:
                return False
    return True


def nombre_incoherences_semaine(m, n):
    nb = 0
    for semaine in m:
        present = [-1] * n
        for a, b in semaine:
            present[a] += 1
            present[b] += 1
        nb += sum(list(map(abs, present)))  # [abs(ab) for ab in present])
    return nb


def nombre_incoherences_periodes(m_t, n):
    nb = 0
    for periode in m_t:
        present = [0] * n
        for a, b in periode:
            present[a] += 1
            present[b] += 1
        nb += sum([0 if i <= 2 else i - 2 for i in present])
    return nb


def nombre_incoherences_totales(m, n):
    return nombre_incoherences_semaine(m, n) + nombre_incoherences_periodes(transpose(m), n)


def matrice_incoherences_semaine(m, n):
    matrice_incoherences = [[0] * (n // 2) for _ in range(n - 1)]
    for num_s, semaine in enumerate(m):
        present = [-1] * n
        for a, b in semaine:
            present[a] += 1
            present[b] += 1
        inco = list(map(abs, present))
        for num_p, ab in enumerate(semaine):
            a, b = ab
            matrice_incoherences[num_s][num_p] += (inco[a] > 0) + (inco[b] > 0)
    return matrice_incoherences


def matrice_incoherences_periode(m_t, n, matrice_incoherences=None):
    if not matrice_incoherences:
        matrice_incoherences = [[0] * (n - 1) for _ in range(n // 2)]
    for num_p, periode in enumerate(m_t):
        present = [0] * n
        for a, b in periode:
            present[a] += 1
            present[b] += 1
        inco = [0 if v <= 2 else v - 2 for v in present]
        for num_s, ab in enumerate(periode):
            a, b = ab
            matrice_incoherences[num_p][num_s] += (inco[a] > 0) + (inco[b] > 0)
    return matrice_incoherences


def matrice_incoherences_totales(m, n):
    return transpose(matrice_incoherences_periode(transpose(m), n, transpose(matrice_incoherences_semaine(m, n))))


def voisins_colonne(matrice, pivot):
    voi = []
    for i in range(len(matrice)):
        if i != pivot[0]:
            v = deepcopy(matrice)
            permutation_m(v, pivot, (i, pivot[1]))
            voi.append(v)
    return voi


def voisins_totaux(matrice, pivot):
    voi = []
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            if (i, j) != pivot:
                v = deepcopy(matrice)
                permutation_m(v, pivot, (i, j))
                voi.append(v)
    return voi


def r_to_m(r, s, p):
    return [r[i * p:i * p + p] for i in range(s)]


def m_to_r(m):
    return [ab for s in m for ab in s]


def transpose(m):
    return list(map(list, zip(*m)))


def permutation(r, i1, i2):
    r[i1], r[i2] = r[i2], r[i1]


def permutation_m(m, i1, i2):
    m[i1[0]][i1[1]], m[i2[0]][i2[1]] = m[i2[0]][i2[1]], m[i1[0]][i1[1]]


import matplotlib.pyplot as plt


def show_stats(stats, title=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    if title:
        plt.title(title)
    plt.xlabel("tours")
    plt.ylabel('fitness')
    # plt.xlim(0, len(stats['max_fitness']))
    # plt.ylim(-70, 0)  # (-70,0)#(0, 100)  # stats['parameters']['chromosome size'])  # stats['max_fitness'][-1]*1.1

    ax.plot(stats['max_fitness'], color='red', label='max')
    ax.plot(stats['min_fitness'], color='green', label='min')
    ax.plot(stats['mean_fitness'], color='blue', label='mean')
    # ax.plot(stats['fitness_diversity'], color='black', label='fitness_diversity')

    windows_size = 49
    polynomial_order = 3

    # ax.plot(savgol_filter(stats['max_fitness'], windows_size, polynomial_order), color='red', linestyle='dashed',
    #         label='max_fitness soft')
    # ax.plot(savgol_filter(stats['min_fitness'], windows_size, polynomial_order), color='green', linestyle='dashed',
    #         label='min_fitness soft')
    # ax.plot(savgol_filter(stats['mean_fitness'], windows_size, polynomial_order), color='blue', linestyle='dashed',
    #         label='mean_fitness soft')

    plt.legend(title='fitness', loc='lower right')

    # plt.title("\n".join(textwrap.wrap(str(stats['parameters']['mutation'][1]), 120)))
    plt.show()

    # fig, ax = plt.subplots(figsize=(10, 10))
    #
    # ax.plot(stats['diversity'], color='yellow', label='diversity')
    # ax.plot(stats['max_age'], color='c', label='max_age')
    # ax.plot(stats['mean_age'], color='m', label='mean_age')
    #
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    #
    # plt.show()
    #
    # fig, ax = plt.subplots(figsize=(10, 10))
    #
    # ax.plot(stats['total_fitness'], color='black', label='total_fitness')
    #
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    #
    # plt.show()
