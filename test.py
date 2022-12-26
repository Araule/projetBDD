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
mot_de_passe = input("Entrez votre matricule : ")
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

# On sélectionne le bar du manager
curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()
print(f"\nVous êtes le manager du bar \"{nom_bar[0]}\".")

#les boissons qui seront supprimées
boissons_supprimees = input("Entrez le nombre de boissons que vous voulez supprimées : ")

print(f"\nLe manager veut supprimer de la carte {boissons_supprimees} boissons.")

#boissons les moins consommées est égal aux boissons les moins vendues
#le résultat de l'input boissons_supprimees devient la valeur de LIMIT
print(f"\nVoici la liste des \"{boissons_supprimees}\" boissons qui se sont le moins bien vendues dans votre établissement au mois de Novembre.")
curseur.execute(f"SELECT C.boisson, COUNT(V.idBoisson) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY C.boisson \
            ORDER BY COUNT(V.idBoisson) \
            LIMIT \"{boissons_supprimees}\"")
boissons_moins_consommées = curseur.fetchall()
for r in boissons_moins_consommées :
    print(f"{r[0]} n'a été vendu que {r[1]} fois.")
print(boissons_moins_consommées)

#les boissons qui rapportent le moins
print(f"\nVoici la liste des \"{boissons_supprimees}\" boissons qui ont rapporté le moins d'argent au mois de Novembre.")
curseur.execute(f"SELECT C.boisson, ROUND(SUM(C.prix_EU), 2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY C.boisson \
            ORDER BY ROUND(SUM(C.prix_EU), 2)\
            LIMIT  \"{boissons_supprimees}\"")
boissons_peu_bénéfice = curseur.fetchall()
for r in boissons_peu_bénéfice :
    print(f"{r[0]} n'a permis un bénéfice que de {r[1]} euros.")


#une liste des boissons
#les boissons sont égales aux résultats de la réquête boissons_moins_consommées
boisson_supp = (tuple(zip(*boissons_moins_consommées))[0])
print(boisson_supp)


# supprimer les boissons les moins consommées
#on supprime dans l'attribut de la table C.boisson de la table Carte le contenu de la liste boisson_supp
print(f"Les boissons supprimées seront \"{boisson_supp}\".\n")
curseur.execute(f"DELETE FROM Carte\
        WHERE  \"{boisson_supp}\" IN (SELECT C.boisson FROM Carte AS C)")
#

# WHERE EXISTS (SELECT C.boisson, COUNT(V.idBoisson) FROM Employes AS E, Ventes AS V WHERE  E.matricule = V.matricule AND C.idBoisson = V.idBoisson\
# AND E.nom_bar = \"{nom_bar[0]}\" GROUP BY C.boisson \ORDER BY ROUND(SUM(C.prix_EU), 2)\LIMIT 10") ")




