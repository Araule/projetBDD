#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ici, on veut refaire la même chose que dans l’exercice 3 en jouant sur les droits utilisateurs.
# Pour cela, l’identifiant du manager accédant à ces informations devra être spécifié. Si l’employé
# a accès aux ventes de son établissement (i.e., s’il s’agit du manager de l’établissement), alors il
# pourra accéder aux ventes effectuées dans son bar. Sinon, un message d’erreur apparaîtra à
# l’écran lui indiquant qu’il n’a pas accès à ces informations.
# Dans les exercices suivants, on conservera les droits d’utilisateurs des managers.

import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# On veut une liste avec les identifiants des managers (prenom.nom) et une liste avec les mots de passe des managers (matricule)
curseur.execute("SELECT Em.prenom, Em.nom, Em.matricule \
                    FROM Employes AS Em, Etablissements AS Et \
                    WHERE Et.matricule_manager = Em.matricule \
                    AND Em.nom_bar = Et.nom_bar")
results = curseur.fetchall()
id_managers = []
mdp_managers = []
for r in results :
    id_managers.append((f"{r[0]}.{r[1]}", r[2]))
print(id_managers, mdp_managers)

# L'utilisateur rentre son matricule
#identifiant = input("Entrez votre identifiant : ")
#mot_de_passe = input("Entrez votre mot de passe : ")
# Si l'identification se passe bien, c'est un manager donc il a les droits d'utilisateur
# Sinon un message d'erreur s'affiche

# Pour cela il faut rajouter cette liste d'utilisateurs autorisés dans la bdd



bdd.close()