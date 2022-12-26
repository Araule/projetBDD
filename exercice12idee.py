#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv
from datetime import datetime

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# on affiche les identifiants de connexion des managers
curseur.execute("SELECT * FROM Managers")
results = curseur.fetchall()
for r in results :
    print(r)


# Le manager se connecte
identifiant = input("\nEntrez votre identifiant : ")
mot_de_passe = input("Entrez votre mot de passe : ")
connexion = f"SELECT identifiant \
                FROM Managers \
                WHERE identifiant = '{identifiant}' \
                AND matricule = '{mot_de_passe}';"
curseur.execute(connexion)
if not curseur.fetchone() :  
    print("\nIdentifiants incorrects. Vous n'avez peut-être pas accès aux informations suivantes.")
    exit() 
else :
    print("\nBienvenue.")


# On sélectionne le bar du manager pour filtrer les requêtes qui suivent
curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()
print(f"\nVous êtes le manager du bar \"{nom_bar[0]}\".")

# On demande au manager combien de boissons souhaite-il enlever de la carte 
# On veut que la variable soit de type int
input_chiffre = int(input("\nCombien de boissons maximum souhaitez-vous enlever de la carte ? "))


# On rattache les résultats des deux requêtes à une variable pour les réutiliser plus tard
curseur.execute(f"SELECT ROUND(SUM(C.prix_EU), 2) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\"") # total des bénéfices du mois de novembre dans le bar du manager
results = curseur.fetchall()
for r in results :
    total_bénéfice = r[0]

curseur.execute(f"SELECT COUNT(V.idBoisson) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\"") # nombre total de boissons vendues au mois de novembre dans le bar du manager
results = curseur.fetchall()
for r in results :
    total_vendue = r[0]


# On crée une liste vide qui contiendra le nom des boissons que le manager peut supprimer de la carte
liste_boisson = []


i = 0 # on initialise un compteur

# Dans la requête, les boissons sont triés de celle qui apporte le moins de bénéfice à celle qui en rapporte le plus
# La boucle a plusieurs compteurs :
# 1 : input_chiffre et i - si le compteur i atteint le nombre de boisson que le manager souhaite enlever de la carte, la boucle s'arrête
# 2 : if statement : si les bénéfices de la boisson suivante représentent plus de 2% des bénéfices, la boucle s'arrête aussi
# Il est peu probable que la boucle s'arrête à cause du deuxième compteur car une boisson qui représente plus de 2% des recettes totals sur un mois, c'est une boisson qui se vend très bien

# Pour qu'une boisson soit supprimer, il faut que son bénéfice représente moins de 2% du bénéfice total du bar au mois de Novembre
# Mais il faut aussi que le nombre de boissons vendues représente moins de 1% du nombre total de boissons vendues dans le mois
# Cela permet d'écarter des boissons populaires auprès de la clientèle mais qui se vendent à un prix plus bas
# L'idée est d'enlever certaines boissons peu populaire et qui rapporte peu, pas de ne garder que les boissons qui rapportent le plus
# en s'alienant une partie de la clientèle

curseur.execute(f"SELECT C.boisson, ROUND(SUM(C.prix_EU), 2) \
                    FROM Employes AS E \
                    INNER JOIN Ventes AS V \
                    ON E.matricule = V.matricule \
                    INNER JOIN Carte AS C \
                    ON C.idBoisson = V.idBoisson \
                    WHERE E.nom_bar = \"{nom_bar[0]}\" \
                    GROUP BY C.boisson \
                    ORDER BY ROUND(SUM(C.prix_EU), 2)")
results = curseur.fetchall()
for r in results :
    
    if r[1] < (total_bénéfice * 0.02) :
        curseur.execute(f"SELECT COUNT(V.idboisson) \
                            FROM Employes AS E \
                            INNER JOIN Ventes AS V \
                            ON E.matricule = V.matricule \
                            INNER JOIN Carte AS C \
                            ON C.idBoisson = V.idBoisson \
                            WHERE E.nom_bar = \"{nom_bar[0]}\" \
                            AND C.boisson = \"{r[0]}\"")
        results2 = curseur.fetchall()
        
        for r2 in results2 :
            
            if r2[0] < (total_vendue * 0.01) :
                liste_boisson.append(f"{r[0]} : {r[1]} euros de bénéfice, vendue {r2[0]} fois")
                i += 1
    
    if i != input_chiffre :
        continue
    
    break

print(f"\nVous pouvez supprimer de la carte ces {i} boissons. Chaque boisson représente moins de 2% des recettes totales du mois de Novembre et moins de 1% du nombre total de boissons vendues.")
for ligne in liste_boisson :
    print(ligne)

bdd.close()