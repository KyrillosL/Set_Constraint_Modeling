from SCM.STS import launch_STS

if __name__ == "__main__":
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="Nombre d'equipes")
    parser.add_argument("-s", type=int, help="0 toutes les solutions, 1 une seule solution")
    args = parser.parse_args()

    nombre_equipes = args.n if args.n else 8

    trouver_toutes_les_solutions = True if args.s else False

    start_time = time.time()
    launch_STS(nombre_equipes, trouver_toutes_les_solutions)
    print("--- %s seconds ---" % (time.time() - start_time))
