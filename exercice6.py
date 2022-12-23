#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sqlite3
import csv

bdd = sqlite3.connect("BARS.db")
curseur = bdd.cursor()

#connexion du manager
identifiant = input("\nEntrez votre identifiant : ")
mot_de_passe = input("Entrez votre matricule : ")

connexion = f"SELECT identifiant \
                FROM Managers \
                WHERE identifiant = '{identifiant}' \
                AND matricule = '{mot_de_passe}';"
curseur.execute(connexion)
if not curseur.fetchone() :  
    print("\nIdentifiants incorrects.")
    exit() 
else :
    print("\nVous souhaitez connaître le nombre de boissons vendues dans votre établissement.\n")

curseur.execute(f"SELECT nom_bar \
                    FROM Etablissements \
                    WHERE matricule_manager = '{mot_de_passe}'")
nom_bar = curseur.fetchone()

print(f"Vous êtes le manager du bar \"{nom_bar[0]}\".\n")

'''
dates = []
curseur.execute("SELECT strftime('%m',date) FROM Ventes;")
for ligne in curseur.fetchall():
    dates.append(ligne[0])
print(dates)
'''

#problèmes : 
# faire entrer que le mois à l'utilisateur
#ne sait pas comment faire pour aussi afficher le bénéfice généré pour chaque employé dans la même requête

curseur.execute(f"SELECT COUNT(V.idBoisson), ROUND(SUM(C.prix_EU),2)\
    FROM Ventes AS V, Carte AS C , Employes AS E, Etablissements AS Et\
        WHERE C.idBoisson = V.idBoisson\
            AND E.nom_bar = \"{nom_bar[0]}\"\
                AND Et.nom_bar = \"{nom_bar[0]}\"\
                AND V.matricule = E.matricule\
                    AND V.date BETWEEN '01-11-2022' AND '31-11-2022'\
                        GROUP BY  Et.nom_bar")
results = curseur.fetchall()
for r in results :
    print(f"Vos employés ont vendu {r[0]} boissons pour un total de {r[1]} euros.")

#Bien préciser pour E.nom_bar et Et.nom_bar qu'il s'agit du bar du manager
#Sinon problème de résultat
#Exemple avec Daniel.Faviet / T80612 / Le Saphir
#Si on ne met que E.nom_bar =\"{nom_bar[0]}\" ou que Et.nom_bar = \"{nom_bar[0]}\"\
#On aura comme boisson vendu 50170 au lieu de 5017 et comme total 266985,0 au lieu de 26698.5

bdd.close()
