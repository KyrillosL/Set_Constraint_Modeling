from typing import Dict, Any

from satispy import Variable, Cnf
from satispy.solver import Minisat
import random
import math
n=6
team= n
week =n-1
period=int(n/2)

exp = Cnf()


sol={}  # type: Dict[int, Dict[Any, Any]]

#Creation des variables :
for w in range(week):
    sol[w]={}
    for p in range(period):
        sol[w][p]={}
        for number_team in range(2):
            sol[w][p][number_team]=[]
            for length_team in range(team):
                v0 = Variable(str(w)+str(p)+str(number_team)+str(length_team))
                sol[w][p][number_team].append(v0)


#C1 Codage d'une équipe : au moins une équipe. OK
for w in range(week):
    for p in range(period):
        for number_team in range(2):
            c = Cnf()
            for length_team in range(team):
                c |= sol[w][p][number_team][length_team] #C1-3 Au moins une équipe
            exp &=c


#####SYMETRIEEEESSS
#L'équipe 6 ne peut pas jouer en team2
for w in range(week):
    for p in range(period):
        exp &= -sol[w][p][0][team-1]



#Si une équipe joue dans le slot 1, alors les équipes ayant un numéro inférieures ne peuvent pas jouer dans le slot 2
for w in range(week):
    for p in range(period):
        for i in range(team-1):
            c= Cnf()
            for j in range( i+1):
                exp &= sol[w][p][0][i] >> -sol[w][p][1][j]
####END SYMETRIES



#C1 Codage d'une équipe : au plus une équipe. OK
for w in range(week):
    for p in range(period):
        for number_team in range(2):

            for length_team in range(team):
                for length_team2 in range(length_team+1, team):
                    exp &=sol[w][p][number_team][length_team]>> -sol[w][p][number_team][length_team2]



#C1 Une équipe joue contre une autre OK
for w in range(week):
    for p in range(period):
        for number_team in range(2):
            for number_team2 in range(number_team+1, 2):
                for length_team in range(team):
                    exp &=  (sol[w][p][number_team][length_team] >> -sol[w][p][number_team2][length_team])



#C1 Pas deux fois le même match /Periods
for w in range(week):
    for w2 in range(w+1, week):
        for p in range(period):
                #for p2 in range(p+1, period):
                    #for number_team in range(2):
                        #for number_team2 in range(number_team+1, 2):
            for length_team in range(team):
                for length_team2 in range(team):
                    exp &=  ((sol[w][p][0][length_team] & sol[w][p][1][length_team2] )
                             >> ((-sol[w2][p][0][length_team] | -sol[w2][p][1][length_team2]) & (-sol[w2][p][1][length_team] | -sol[w2][p][0][length_team2])) )


z et (x ou y) = z et x ou z et y 


#C1 Pas deux fois le même match /WEEKS
for w in range(week):
    for p in range(period):
        for p2 in range(p+1, period):
            #for number_team in range(2):
            #for number_team2 in range(number_team+1, 2):
            for length_team in range(team):
                for length_team2 in range(team):
                    exp &=  ((sol[w][p][0][length_team] & sol[w][p][1][length_team2] )
                             >> ((-sol[w][p2][0][length_team] | -sol[w][p2][1][length_team2])&(-sol[w][p2][1][length_team] | -sol[w][p2][0][length_team2])))

#C1 Pas deux fois le même match / LES DEUX
for w in range(week):
    for w2 in range(w+1, week):
        for p in range(period):
            for p2 in range(p+1, period):

                for length_team in range(team):
                    for length_team2 in range(team):
                        exp &=  ((sol[w][p][0][length_team] & sol[w][p][1][length_team2] )
                                 >> ((-sol[w2][p2][0][length_team] | -sol[w2][p2][1][length_team2])& (-sol[w2][p2][1][length_team] | -sol[w2][p2][0][length_team2])))
                        exp &=  ((sol[w2][p][0][length_team] & sol[w2][p][1][length_team2] )
                                 >> ((-sol[w][p2][0][length_team] | -sol[w][p2][1][length_team2])&(-sol[w][p2][1][length_team] | -sol[w][p2][0][length_team2])))


#C2 Une équipe joue une fois par semaine
for w in range(week):
    for p in range(period):
        for p2 in range(p+1,period):
            for number_team in range(2):
                for number_team2 in range(number_team+1, 2):
                    for length_team in range(team):

                        exp&= (sol[w][p][number_team][length_team]>>( -sol[w][p][number_team2][length_team] & -sol[w][p2][number_team][length_team] & -sol[w][p2][number_team2][length_team]  ))
                        exp&= (sol[w][p][number_team2][length_team]>>( -sol[w][p2][number_team][length_team] ))#Periode 1 team 2 pas dans periode 2 team 1
                        exp&= (sol[w][p][number_team2][length_team]>>( -sol[w][p2][number_team2][length_team] ))# Periode 1 team 2 pas dans periode 2 team 2



#C2 Une équipe joue au maximum deux fois par periode
for w in range(week):
    for w2 in range(w+1, week):
        for w3 in range(w2+1, week):
            for p in range(period):
                for length_team in range(team):
                    exp &=  (  (  (sol[w][p][0][length_team] | sol[w][p][1][length_team]) & (sol[w2][p][0][length_team] | sol[w2][p][1][length_team]) )>> -( sol[w3][p][0][length_team] | sol[w3][p][1][length_team] ))




print(exp)


solver = Minisat()

solution = solver.solve(exp)


if solution.success:
    print ("Found a solution:\n")#, solution)

    #for key in solution.varmap:
    #    print(key)

    for w in range(week):
        for p in range(period):
            for number_team in range(2):
                for length_team in range(team):
                    #print(w,p,number_team, length_team)
                    #print(solution["w0p0nt0lt0"])
                    #print("key: ",sol[w][p][number_team][length_team])
                    #print(sol[w][p][number_team][length_team]," ", solution[sol[w][p][number_team][length_team]], end=' ')
                    #print(w,p,number_team,length_team,solution[sol[w][p][number_team][length_team]], end=' ')
                    print(solution[sol[w][p][number_team][length_team]], end=' ')
                print(end="|")
        print()

    for w in range(week):
        for p in range(period):
            for number_team in range(2):
                numero_team=-1
                for length_team in range(team):
                    if solution[sol[w][p][number_team][length_team]]==True:
                        numero_team=length_team+1
                print(numero_team, end=' ')
        print()
else:
    print("The expression cannot be satisfied")
