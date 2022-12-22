#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# On veut une table dans le database avec les identifiants des managers (prenom.nom) et  leur mot de passe (matricule)
# la clé primaire sera l'identifiant du manager (dans notre datatbase, il n'y a pas de personne avec le même prénom et le même nom)
# curseur.execute("CREATE TABLE Login (identifiant TEXT PRIMARY KEY, mot_de_passe TEXT NOT NULL);")

# On crée une liste de dictionnaires avec { id : prenom.nom, mdp : matricule)
curseur.execute("SELECT Em.prenom, Em.nom, Em.matricule \
                    FROM Employes AS Em, Etablissements AS Et \
                    WHERE Et.matricule_manager = Em.matricule \
                    AND Em.nom_bar = Et.nom_bar")
id_managers = []
results = curseur.fetchall()
for r in results :
    id_managers.append({ "id" : f"{r[0]}.{r[1]}", "mdp" : r[2] })

# maintenant, on ajoute nos données dans la table Login
#for id in id_managers :
# curseur.execute("INSERT INTO Login (identifiant, mot_de_passe) \
# VALUES(:id, :mdp)", id)
# bdd.commit()

# on vérifie que tout est en ordre
curseur.execute("SELECT * FROM Login")
results = curseur.fetchall()
for r in results :
    print(r)


# L'utilisateur rentre ses identifiants
identifiant = input("Entrez votre identifiant : ")
mot_de_passe = input("Entrez votre mot de passe : ")
# Si l'identification se passe bien, c'est un manager donc il a les droits d'utilisateur
# Sinon un message d'erreur s'affiche
connexion = f"SELECT identifiant from Login WHERE identifiant='{identifiant}' AND mot_de_passe ='{mot_de_passe}';"
curseur.execute(connexion)
if not curseur.fetchone() :  # s'il n'y a pas de résultat, c'est que le login n'est pas bon, cet utilisateur n'est pas un manager
    print("Identifiants incorrects.")
else:
    print("Bienvenue")


bdd.close()