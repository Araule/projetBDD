#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

# on crée 4 tableaux, un par entité
# on a Employes, Etablissements, Carte, Ventes
curseur.execute("CREATE TABLE Employes (matricule TEXT PRIMARY KEY, nom TEXT NOT NULL, prenom TEXT NOT NULL, profession TEXT, \
    nom_bar TEXT, FOREIGN KEY (nom_bar) REFERENCES Etablissements(nom_bar));") #departement?
curseur.execute("CREATE TABLE Etablissements (nom_bar TEXT PRIMARY KEY, adresse TEXT NOT NULL, numTelephone INTEGER, \
    matricule_manager TEXT, FOREIGN KEY (matricule_manager) REFERENCES Employes(matricule));") #identifiant?
curseur.execute("CREATE TABLE Carte (idBoisson INTEGER PRIMARY KEY AUTOINCREMENT, boisson TEXT NOT NULL, type TEXT,\
    prix_EU REAL, degre_BIERES REAL, quantite_CL REAL);")
curseur.execute("CREATE TABLE Ventes (idVente INTEGER PRIMARY KEY AUTOINCREMENT, matricule TEXT, idBoisson INTEGER, date TEXT, \
    FOREIGN KEY (matricule) REFERENCES Employes(matricule), FOREIGN KEY (idBoisson) REFERENCES Etablissements(idBoisson));") # quand 2 identifiants?


PATH = "/home/laura/Documents/projetBDD/"

# L'entité Employes a pour attributs : matricule (clé primaire car identifiant unique), nom, prenom, profession, nom_bar
fichierEmployes = open(PATH+'employes.csv', 'rt')
CSVEmployes = csv.DictReader(fichierEmployes, delimiter="\t")
for ligne in CSVEmployes:
    curseur.execute("INSERT INTO Employes (matricule, nom, prenom, profession, nom_bar) \
        VALUES(:Matricule, :Nom, :Prenom, :Profession, :Nom_Bar)", ligne)
fichierEmployes.close()

# L'entité Etablissements a pour attributs : nom_bar (clé primaire car chaque bar a un nom différent), adresse, numTelephone, matricule_manager
fichierEtablissements = open(PATH+'etablissements.csv', 'rt')
CSVEtablissements = csv.DictReader(fichierEtablissements, delimiter="\t")
for ligne in CSVEtablissements:
    curseur.execute("INSERT INTO Etablissements (nom_bar, adresse, numTelephone, matricule_manager) \
        VALUES(:Name, :Adresse, :NumTel, :Manager_Id)", ligne)
fichierEtablissements.close()

# L'entité Carte a pour attributs : idBoisson (clé primaire car identifiant unique), boisson, type, prix_EU, degre_BIERES, quantite_CL
fichierCarte = open(PATH+'carte.csv', 'rt')
CSVCarte = csv.DictReader(fichierCarte, delimiter="\t")
for ligne in CSVCarte:
    curseur.execute("INSERT INTO Carte (idBoisson, boisson, type, prix_EU, degre_BIERES, quantite_CL) \
        VALUES(:Id_Boisson, :Nom, :Type, :Prix, :Degre, :Quantite)", ligne)
fichierCarte.close()

# L'entité Ventes a pour attributs : idVente (clé primaire crée par nous-même car il n'y avait pas d'identifiant unique dans le fichier csv), matricule, idBoisson, date
fichierVentes = open(PATH+'ventes.csv', 'rt')
CSVVentes = csv.DictReader(fichierVentes, delimiter="\t")
for ligne in CSVVentes:
    curseur.execute("INSERT INTO Ventes (matricule, idBoisson, date) \
        VALUES(:Employe_Id, :Boisson_Id, :Date)", ligne)
fichierVentes.close()

bdd.commit()
bdd.close()