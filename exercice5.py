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

# On a ici la liste des matricules de l'ensemble des managers
curseur.execute("SELECT matricule_manager \
                    FROM Etablissements")
results = curseur.fetchall()
matricules_managers = []
for r in results :
    matricules_managers.append(r[0])

# L'utilisateur rentre son matricule
identifiant = input("Entrez votre matricule : ")
# Si son matricule se trouve dans la liste matricules_managers, alors il a les droits d'utilisateurs
# Sinon un message d'erreur s'affiche

# Pour cela il faut rajouter cette liste d'utilisateurs autorisés dans la bdd



bdd.close()