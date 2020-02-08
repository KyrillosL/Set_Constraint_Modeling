from SCM.STS import launch_STS

if __name__ == "__main__":
    import time

    start_time = time.time()
    nombre_equipes = 8
    trouver_toutes_les_solutions = False
    launch_STS(nombre_equipes, trouver_toutes_les_solutions)
    print("--- %s seconds ---" % (time.time() - start_time))
