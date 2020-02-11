int: nbr_groupe = 5;
int: nbr_semaine = 3;
int: nbr_golfeur_par_groupe = 4;
int: nbr_golfeur = nbr_groupe*nbr_golfeur_par_groupe;

set of int: groupe = 1..nbr_groupe;
set of int: semaine = 1..nbr_semaine;
set of int: golfeur = 1..nbr_golfeur;

array[semaine, golfeur] of var groupe: groupe_par_semaine;

constraint forall(gr in 0..nbr_groupe-1)(
  forall(go in 1..nbr_golfeur_par_groupe)(
    groupe_par_semaine[1,go+(gr*nbr_golfeur_par_groupe)]=(gr+1)
));

constraint forall(s in semaine)(
    forall(g in groupe)(
      how_many_in_a_group(s,g)==nbr_golfeur_par_groupe
    )
);

constraint forall(g1 in 1..nbr_golfeur-1)(
  forall(g2 in g1+1..nbr_golfeur)(
    forall(s1 in 1..nbr_semaine-1)(
      if groupe_par_semaine[s1,g1]==groupe_par_semaine[s1,g2]
        then forall(s2 in s1+1..nbr_semaine)(
          groupe_par_semaine[s2,g1]!=groupe_par_semaine[s2,g2]
        )
      endif
    )
  )
);

function var int: how_many_in_a_group(int: semaine, int: groupe) =
  how_many(semaine, groupe, 1);

function var int: how_many(int: semaine, int: groupe, int: golfeur) =
  if golfeur > nbr_golfeur then 0
  else
    if groupe_par_semaine[semaine,golfeur]==groupe
      then 1+how_many(semaine, groupe, golfeur+1)
    else
      how_many(semaine, groupe, golfeur+1)
    endif
  endif;

solve satisfy;