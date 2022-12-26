#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

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
input_chiffre = input("\nCombien de boissons souhaitez-vous enlever de la carte ? ")
print(f"Vous souhaitez enlever {input_chiffre} de la carte.")


# On crée deux listes, une pour les boissons qui se sont le moins vendues, et une liste pour les boissons qui ont rapporté le moins d'argent
moins_vendue = []
moins_benefice = []

# affiche les boissons les moins vendues dans l’établissement ce mois-ci
# filtre : le nom du bar du manager connecté
# regroupement : grâce au jointure entre Carte et Ventes, les ventes sont regroupées par le nom de boisson de la table Carte
# trie : par le nombre de boisson vendu (selon leur nom), du nombre le plus petit au plus grand
print(f"\nVoici la liste des \"{input_chiffre}\" boissons qui se sont le moins bien vendues au mois de Novembre.")
curseur.execute(f"SELECT C.boisson, COUNT(V.idBoisson) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY C.boisson \
            ORDER BY COUNT(V.idBoisson) \
            LIMIT  \"{input_chiffre}\"")
boissons_peu_vendues = curseur.fetchall()
for r in boissons_peu_vendues :
    print(f"{r[0]} n'a été vendues que {r[1]} fois.")
    moins_vendue.append(r[0])


# afficher les boissons les moins vendues dans l’établissement ce mois-ci
# filtre : le nom du bar du manager connecté
# regroupement : grâce au jointure entre Carte et Ventes, les ventes sont regroupées par le nom de boisson de la table Carte
# trie : par les bénéfices des ventes des boissons (selon leur nom), du nombre le plus petit au plus grand
print(f"\nVoici la liste des \"{input_chiffre}\" boissons qui ont rapporté le moins d'argent au mois de Novembre.")
curseur.execute(f"SELECT C.boisson, ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY C.boisson \
            ORDER BY ROUND(SUM(C.prix_EU), 2)\
            LIMIT  \"{input_chiffre}\"")
boissons_peu_bénéfice = curseur.fetchall()
for r in boissons_peu_bénéfice :
    print(f"{r[0]} n'a permis un bénéfice que de {r[1]} euros.")
    moins_benefice.append(r[0])


# On demande au manager quel solution il préfère utiliser et on l'applique à la base de donnée
print(f"\nsolution 1 : supprimer les {input_chiffre} boissons qui se sont le moins bien vendues.")
print(f"solution 2 : supprimer les {input_chiffre} boissons qui ont rapporté le moins d'argent.")
input_solution = input("\nQuel solution préférez-vous utiliser ? (tapez 1 ou 2) : ")


if input_solution == "1" : # alors on supprime les boissons qui se sont le moins bien vendues
    print("\nLes boissons supprimées seront : ")
    for boisson in moins_vendue : 
        print (boisson)
        curseur.execute(f"DELETE FROM Carte \
                            WHERE boisson = \"{boisson}\"")
else : # sinon on supprimer les boissons qui ont rapporté le moins d'argent
    print("\nLes boissons supprimées seront : ")
    for boisson in moins_benefice : 
        print (boisson)
        curseur.execute(f"DELETE FROM Carte \
                            WHERE boisson = \"{boisson}\"")


# On vérifie que la suppression s'est bien passé
print("\n")
curseur.execute("SELECT * FROM Carte")
results = curseur.fetchall()
for r in results :
    print(r)


bdd.close()