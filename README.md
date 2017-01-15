# DM Maison numéro 1
Lien : [http://www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect]

## 0. Prerequisites

For the tests :
nose==1.3.7
nose-parameterized==0.5.0

## 1. Comment ça marche ?

Le code est organisé de façon à pouvoir tester facilement deux méthodes différentes de résolution du problème.

### Méthode 1

Méthode 1 : en introduisant des variables qui codent les orientation des tuiles

Cette méthode correspond aux fichiers suivants :
- connect_with_tiles_orientation.py
- test_connect_with_tiles_orientation.py (un fichier avec quelques tests sur 
les méthodes implémentées)

Dans cette méthode, chaque tuile est représentée par un numéro de la liste [0, 1, 3, 5, 7, 15] et par une rotation appartenant à la liste : [0, 1, 2, 3], correspondant au facteur multiplicatif d'une rotation de 90 degrès.

Chaque tuile possède ici une variable représentant la rotation.


### Méthode 2

Méthode 2 : en introduisant des variables qui codent la présence de 
connecteurs sur le contact entre deux tuiles adjacentes

Cette méthode correspond aux fichiers suivants :
- connect_with_tiles_connection.py
- test_connect_with_tiles_connection.py (un fichier avec quelques tests sur 
les méthodes implémentées)

Dans cette méthode, chaque tuile est représentée par 4 variables de connection, comme nous pouvons le voir sur le schéma ci-dessous:

```
                j = 0     j = 1     j = 2


                 x0        x1        x2
                ----      ----      ----  
               |    |    |    |    |    | 
i = 0       x3 |    | x4 |    | x5 |    | x6
                ----      ----      ----  
                 x7        x8        x9
                ----      ----      ----  
               |    |    |    |    |    | 
i = 1       x10|    | x11|    | x12|    | x13
                ----      ----      ----  
                 x14       x15       x16
                ----      ----      ----  
               |    |    |    |    |    | 
i = 2       x17|    | x18|    | x19|    | x20 
                ----      ----      ----  
                 x21       x22       x23

```

Pour une tuile de taille n * n, il y a donc ici 2n(n+1) variables.

### Code commun aux deux méthodes

Dans le fichier connect_with_common.py, vous pourrez retrouver quelques 
fonctions communes aux deux méthodes (notamment la fonction qui permet de
faire rotater une tuile sur elle-même).


## 2. Résultats et performances

Voici les temps comparatifs de résolution des 9 tuiles présentes dans le 
fichier grid_samples.py

Pour chaque grille, voici le temps en ms que met chacune des deux méthodes à
calculer la solution.

| Grid |  Method 1 (Orientation) |  Method 2 (Connection) | Best Method |
|------|-------------------------|------------------------|-------------|
|   2  |           0.236         |           0.517        |      1      |
|   3  |           0.364         |           0.964        |      1      |
|   4  |           0.679         |           1.947        |      1      |
|   5  |           1.132         |           3.234        |      1      |
|   6  |           1.613         |           5.211        |      1      |
|   7  |           2.469         |           8.331        |      1      |
|   8  |          14.393         |          17.367        |      1      |
|   9  |          17.612         |          24.624        |      1      |
|  10  |           7.779         |          32.921        |      1      |

Dans tous les cas, la méthode 1 est plus rapide, ce qui semble être logique 
puisqu'il y a beaucoup moins de variables dans la méthode 1 que dans la 
deuxième.