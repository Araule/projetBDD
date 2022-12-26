#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()


# On veut une table dans la base de données avec les identifiants des managers (prenom.nom) et  leur mot de passe (matricule)
# la clé primaire sera l'identifiant du manager (dans notre datatbase, il n'y a pas de personne avec le même prénom et le même nom)
curseur.execute("CREATE TABLE Managers (identifiant TEXT PRIMARY KEY, matricule TEXT NOT NULL);")


# On crée une liste de dictionnaires avec { id : prenom.nom, mdp : matricule)
curseur.execute("SELECT Em.prenom, Em.nom, Em.matricule \
                    FROM Employes AS Em, Etablissements AS Et \
                    WHERE Et.matricule_manager = Em.matricule \
                    AND Em.nom_bar = Et.nom_bar")
id_managers = []
results = curseur.fetchall()
for r in results :
    id_managers.append({ "id" : f"{r[0]}.{r[1]}", "mdp" : r[2] })


# maintenant, on ajoute nos données dans la table Managers
for ligne in id_managers :
    curseur.execute("INSERT INTO Managers (identifiant, matricule) \
                        VALUES(:id, :mdp)", ligne)
bdd.commit()


# on vérifie que tout est en ordre
curseur.execute("SELECT * FROM Managers")
results = curseur.fetchall()
for r in results :
    print(r)


# L'utilisateur rentre ses identifiants, vous pouvez choisir n'importe quel identifiant des résultats précédents
identifiant = input("\nEntrez votre identifiant : ")
mot_de_passe = input("Entrez votre mot de passe : ")


# Si l'identification se passe bien, c'est un manager donc il a les droits d'utilisateur
# Sinon un message d'erreur s'affiche
connexion = f"SELECT identifiant \
                FROM Managers \
                WHERE identifiant = '{identifiant}' \
                AND matricule = '{mot_de_passe}';"
curseur.execute(connexion)
if not curseur.fetchone() :  # s'il n'y a pas de résultat à la recherche "connexion", c'est que le login n'est pas bon, cet utilisateur n'est pas un manager
    print("\nIdentifiants incorrects. Vous n'avez peut-être pas accès à ces informations.")
    exit() # le script s'arrête.
else :
    print("\nVous souhaitez accéder aux ventes effectuées dans votre bar.\n")


# on va chercher le nom du bar où il travaille. 
# filtre : mot_de_passe est aussi le matricule du manager qui s'est connecté, cela rend la chose plus simple
curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()

print(f"Vous êtes le manager du bar \"{nom_bar[0]}\".\n")


# on reprend la requête de base de l'exercice 3
# filtre : le nom du bar, qui change selon quel manager s'est connecté
curseur.execute(f"SELECT E.nom, E.prenom, COUNT(V.idBoisson), ROUND(SUM(C.prix_EU),2) \
            FROM Employes AS E \
            INNER JOIN Ventes AS V \
            ON E.matricule = V.matricule \
            INNER JOIN Carte AS C \
            ON C.idBoisson = V.idBoisson \
            WHERE E.nom_bar = \"{nom_bar[0]}\" \
            GROUP BY V.matricule")
print("\nnombre de boissons vendues par chaque employé : ")
results = curseur.fetchall()
for r in results:
    print(f"{r[1]} {r[0]} a vendu {r[2]} boissons pour un total de {r[3]} euros.")



bdd.close()