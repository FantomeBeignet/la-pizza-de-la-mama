######################################
# Optimisation L3 - 2021/2022        #
# One Pizza is all you need          #
# evaluation.py - Guillaume Coiffier #
######################################

import sys

try:
    instance_file = sys.argv[1]
    solution_file = sys.argv[2]
except:
    raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
        python3 evaluation.py <chemin_vers_fichier_d_entree> <chemin_vers_fichier_de_solution>")

## Lecture du fichier de l'instance
data = []
try:
    with open(instance_file, "r") as f:
        data = f.readlines()
    data = [l.strip().split() for l in data]
except:
    raise Exception("Erreur lors de la lecture de l'instance. Vérifiez que le premier argument est bien un fichier d'instance (comme B_basic.txt)")

## Construction des structures de données

Nclients = int(data[0][0]) # Nombre total de clients
data.pop(0)

ingredients = dict() # nom d'un ingrédient (str) -> identifiant (entier allant de 0 à N-1)
noms_ingredients = [] # identifiant (entier allant de 0 à N-1, indice dans la liste) -> nom de l'ingrédient (str) qui a cet identifiant

Ningredients = 0

L = [set() for _ in range(Nclients)] # L[i] est la liste des ingrédients que le client i aime (Like)
D = [set() for _ in range(Nclients)] # D[i] est la liste des ingrédients que le client i n'aime pas (Dislike)

for client in range(Nclients):
    Lc,Dc = data[2*client][1:], data[2*client+1][1:] # préférences du client
    for nom_ingr in Lc + Dc:
        if nom_ingr not in ingredients: # nom_ingr n'est pas dans les clés du dictionnaire -> c'est un ingrédient que l'on a pas encore rencontré
            ingredients[nom_ingr] = Ningredients # on lui attribue un numéro unique dans [0;N-1]
            noms_ingredients.append(nom_ingr)
            Ningredients += 1 # incrémenter le compteur d'ingrédients
    L[client] = {ingredients[i] for i in Lc}
    D[client] = {ingredients[i] for i in Dc}

# À partir d'ici, les ingrédients sont identifiés par des nombres allant de 0 à N-1

print("Nombre de clients :", Nclients)
print("Nombre total d'ingredients :", Ningredients)
print()

## Lecture du fichier de solution
data_soluce = []
try:
    with open(solution_file, "r") as f:
        data_soluce = f.readlines()
except:
    print("Erreur lors de la lecture de la solution. Vérifiez que le premier argument est bien un fichier d'instance (comme B_basic.txt)")
    exit()

## Vérification de la validité de la solution

# Vérification du nombre de lignes dans le fichier
if len(data_soluce)!=1:
    print("Erreur dans la solution : la solution ne tient pas sur une seule ligne")
    exit()

data_soluce = data_soluce[0].strip().split()
n_ingredients_soluce, data_soluce = int(data_soluce[0]), data_soluce[1:] # on sépare le nombre d'ingrédient de leurs noms

# Vérification du nombre d'ingrédients
if n_ingredients_soluce != len(data_soluce):
    print("Erreur dans la solution : le nombre d'ingrédients ne correspond pas aux noms")
    exit()

# Vérification des doublons
sans_doublons = set(data_soluce) # dans un set, chaque élément distinct ne peut être présent qu'au plus une fois
if len(sans_doublons) != len(data_soluce):
    print("Erreur dans la solution : des doublons sont présents parmis les ingrédients")
    exit()

# Vérification de l'existence des ingrédients
for ing in data_soluce:
    if ing not in ingredients: # ingredient est la liste (clés de dictionnaire) des noms d'ingrédients
        print("Erreur dans la solution : l'ingrédient {} trouvé dans la solution ne figure pas parmi les ingrédients possibles".format(ing))
        exit()

## Fonction de calcul du score d'une solution
def compute_score(solution_set):
    s = 0
    for c in range(Nclients):
        if L[c].issubset(solution_set) and len(D[c].intersection(solution_set))==0:
            # Tous les ingrédients aimés (L) sont présents dans la solution -> L est un sous ensemble de solution_set
            # Aucun ingrédient détesté (D) n'est présent dans la solution -> l'intersection de D et de solution_set est vide
            s += 1
    return s

solution_set = {ingredients[nom_ingr] for nom_ingr in data_soluce} # transformer en indices entiers
score = compute_score(solution_set)
print("La solution proposée contient {} ingrédients".format(n_ingredients_soluce))
print("Score de cette solution : {}".format(score))