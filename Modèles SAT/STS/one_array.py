from satispy import Variable, Cnf
from satispy.solver import Minisat
import random
import math
n=8
team= n
week =n-1
period=int(n/2)

exp = Cnf()


sol={}
#Creation des variables :
for w in range(week):
    sol[w]={}
    for p in range(period):
        sol[w][p]=[]

        for length_team in range(team):
            v0 = Variable(str(w)+str(p)+str(length_team))
            sol[w][p].append(v0)




#C1 Une équipe joue contre une autre
for w in range(week):
    for p in range(period):
        c = Cnf()
        for t in range(team):

            for t2 in range(t+1, team):
                c |= (sol[w][p][t]&sol[w][p][t2]) #C1-3 Au moins deux équipe
                for t3 in range(t2+1, team):
                    exp &= ( (sol[w][p][t] & sol[w][p][t2] )>> -sol[w][p][t3]) #Pas plus de deux équipes
        exp &=c

#C3  Une équipe joue 1 fois par semaine
for w in range(week):
    for p in range(period):
        for p2 in range(p+1,period):
            for t in range(team):
                exp &= (sol[w][p][t] >> -sol[w][p2][t] )  #C3


#C4 Pas deux fois la même équipe par période
for w in range(week):
    for w2 in range(w+1, week):
        for w3 in range(w2+1, week):
            for p in range(period):
                for t in range(team):
                    exp &= (- sol[w][p][t] | -sol[w2][p][t] | -sol[w3][p][t] )  #C4


#C2 Pas deux fois le même match dans une  Periode
for w in range(week):
    for w2 in range(w+1, week):
        for p in range(period):
            for t in range(team):
                for t2 in range(t+1, team):
                    #exp &= ( (sol[w][p][t] & sol[w][p][t2]) >> -(sol[w][p2][t] & sol[w][p2][t2]))  #C2
                    exp &= ( (sol[w][p][t] & sol[w][p][t2]) >> -(sol[w2][p][t] & sol[w2][p][t2]))
                    #exp &= ( (sol[w][p][t] & sol[w][p][t2]) >> -(sol[w2][p2][t] & sol[w2][p2][t2]))

#C2 Pas deux fois le même match dans une  Periode
for w in range(week):
    for w2 in range(w+1, week):
        for p in range(period):
            for p2 in range( period):
                for t in range(team):
                    for t2 in range(t+1, team):
                        if p != p2:
                            #exp &= ( (sol[w][p][t] & sol[w][p][t2]) >> -(sol[w][p2][t] & sol[w][p2][t2]))  #C2
                            exp &= ( (sol[w][p][t] & sol[w][p][t2]) >> -(sol[w2][p2][t] & sol[w2][p2][t2]))




solver = Minisat()

solution = solver.solve(exp)

if solution.success:
    print ("Found a solution:\n")#, solution)

    #for key in solution.varmap:
    #    print(key)


    for w in range(week):
        for p in range(period):
            for length_team in range(team):
                #print(w,p,number_team, length_team)
                #print(solution["w0p0nt0lt0"])
                #print("key: ",sol[w][p][number_team][length_team])
                #print(sol[w][p][number_team][length_team]," ", solution[sol[w][p][number_team][length_team]], end=' ')
                #print(w,p,number_team,length_team,solution[sol[w][p][number_team][length_team]], end=' ')
                print(solution[sol[w][p][length_team]], end=' ')
            print(end="|")
        print()

    copy_sol= solution.varmap
    for w in range(week):
        for p in range(period):
            numero_team1=-1
            numero_team2=-1
            already_done=[  ]
            num_team=[]
            for length_team in range(team):
                if copy_sol[sol[w][p][length_team]]==True:
                    if sol[w][p][length_team] in already_done:
                        print("already in ", length_team)
                    else :
                        num_team.append(length_team+1)
                        #print("else ", length_team)
                        already_done.append(sol[w][p][length_team])

            print(" ".join(map(str, num_team)), end=' | ')
        print()


else:
    print("The expression cannot be satisfied")

