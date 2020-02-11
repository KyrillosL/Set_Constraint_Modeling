# Set Constraint Modeling
projet CSP M2

# Problèmes

## The social Golfer Problem (SGP)

## Sport Tournament Scheduling (STS)

# 1 Modèlisation

## 1.1 Modèle initial

| modèle                   | SGP | STS |
|--------------------------|-----|-----|
| contraintes ensemblistes |  X  |  X  |
| FD entier                |  X  |  X  |
| SAT                      |  X  |  X  |

## 1.2 Modèle amélioré

| améliorations           | SGP | STS |
|-------------------------|-----|-----|
| symétries               |  X  |  X  |
| contraintes redondantes |     |     |
| ordre des contraites    |     |  X  |

## 1.3 Résolution

| résolution             | SGP | STS |
|------------------------|-----|-----|
| implantation du modèle |  X  |  X  |
| comparer les modèles   |  X  |  X  |
| analyser les résultats |  X  |  X  |

# 2 Solveur pour les contraintes ensemblistes

Au choix:

- solveur ensembliste : X
- encodage SAT
- réduction et encodage


# 3 Délivrables

Trois parties :

- travail effectué
- rapport
- présentation orale


# Bibliographie

...

Lancer la recherche sur le STS avec 8 équipes en recherchant une seule solution :
    
    pypy3 main.py -n 8 -s 1
    
    python3 main.py -n 8 -s 1

