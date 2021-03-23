# -*-coding:Latin-1 -* #permet d'afficher les accents (latin-1)
 
import os # on importe le module os qui dispose de variables et de fonctions
          # utiles pour dialoguer avec votre syst�me d'exploitation
 
# programme testant si une ann�e, entr�e par l'utilisateur,
# est bissextile ou non
 
print("Entrez une ann�e :")
annee = input() # on attend que l'utilisateur entre l'ann�e qu'il d�sire tester
annee = int(annee) # risque d'erreur si l'utilisateur n'a pas rentr� un nombre
                   # si l'ann�e est bissextile ou non
if annee%400==0 or (annee%4==0 and annee%100!=0):
    print("L'ann�e entr�e est bissextile.")
else:
    print("L'ann�e entr�e n'est pas bissextile.")
 
# on met le programme en pause pour �viter qu'il ne se referme (Windows)
os.system("pause")
