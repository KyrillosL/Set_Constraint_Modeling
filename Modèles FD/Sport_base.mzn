int: nbr_equipe = 12;
int: nbr_semaine = nbr_equipe-1;
int: nbr_periode = nbr_equipe div 2;

set of int: equipes = 1..nbr_equipe;
set of int: semaines = 1..nbr_semaine;
set of int: periodes = 1..nbr_periode;

array[semaines,periodes,0..1] of var equipes: planning;

%Une équipe ne peut pas jouer contre elle-même
constraint forall(s in semaines)(
  forall(p in periodes)(
    planning[s,p,0]!=planning[s,p,1]
));

%Un match n'a lieu qu'une fois
constraint forall(s1 in 1..nbr_semaine-1)(
  forall(s2 in s1+1..nbr_semaine)(
    forall(p1 in 1..nbr_periode-1)(
      forall(p2 in p1+1..nbr_periode)(
        (planning[s1,p1,0]=planning[s2,p1,0] -> planning[s1,p2,1]!=planning[s2,p2,1]) /\
        (planning[s1,p1,0]=planning[s2,p1,1] -> planning[s1,p2,1]!=planning[s2,p2,0]) /\
        (planning[s1,p1,1]=planning[s2,p1,0] -> planning[s1,p2,0]!=planning[s2,p2,1]) /\
        (planning[s1,p1,1]=planning[s2,p1,1] -> planning[s1,p2,0]!=planning[s2,p2,0])        
))));
constraint forall(s1 in 1..nbr_semaine-1)(
  forall(s2 in s1+1..nbr_semaine)(
    forall(p in 1..nbr_periode)(
      (planning[s1,p,0]=planning[s2,p,0] -> planning[s1,p,1]!=planning[s2,p,1]) /\
      (planning[s1,p,0]=planning[s2,p,1] -> planning[s1,p,1]!=planning[s2,p,0]) /\
      (planning[s1,p,1]=planning[s2,p,0] -> planning[s1,p,0]!=planning[s2,p,1]) /\
      (planning[s1,p,1]=planning[s2,p,1] -> planning[s1,p,0]!=planning[s2,p,0])        
)));

%Une équipe ne joue qu'une fois par semaine
constraint forall(s in semaines)(
  forall(p1 in 1..nbr_periode-1)(
    forall(p2 in p1+1..nbr_periode)(
      planning[s,p1,0]!=planning[s,p2,0] /\ planning[s,p1,1]!=planning[s,p2,0] /\ planning[s,p1,0]!=planning[s,p2,1] /\ planning[s,p1,1]!=planning[s,p2,1]
)));

%Une équipe ne joue que deux fois par période maximum
constraint forall(s1 in 1..nbr_semaine-2)(
  forall(s2 in s1+1..nbr_semaine-1)(
    forall(s3 in s2+1..nbr_semaine)(
      forall(p in periodes)(
        (planning[s1,p,0]=planning[s2,p,0])->((planning[s1,p,0]!=planning[s3,p,0])/\(planning[s1,p,0]!=planning[s3,p,1])) /\
        (planning[s1,p,0]=planning[s2,p,1])->((planning[s1,p,0]!=planning[s3,p,0])/\(planning[s1,p,0]!=planning[s3,p,1])) /\
        (planning[s1,p,1]=planning[s2,p,0])->((planning[s1,p,1]!=planning[s3,p,0])/\(planning[s1,p,1]!=planning[s3,p,1])) /\
        (planning[s1,p,1]=planning[s2,p,1])->((planning[s1,p,1]!=planning[s3,p,0])/\(planning[s1,p,1]!=planning[s3,p,1]))
))));