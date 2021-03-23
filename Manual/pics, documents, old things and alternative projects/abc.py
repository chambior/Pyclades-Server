# -*-coding:Latin-1 -* #permet d'afficher les accents (latin-1)
 
import os # on importe le module os qui dispose de variables et de fonctions
          # utiles pour dialoguer avec votre système d'exploitation
 
# programme testant si une année, entrée par l'utilisateur,
# est bissextile ou non
 
print("Entrez une année :")
annee = input() # on attend que l'utilisateur entre l'année qu'il désire tester
annee = int(annee) # risque d'erreur si l'utilisateur n'a pas rentré un nombre
                   # si l'année est bissextile ou non
if annee%400==0 or (annee%4==0 and annee%100!=0):
    print("L'année entrée est bissextile.")
else:
    print("L'année entrée n'est pas bissextile.")
 
# on met le programme en pause pour éviter qu'il ne se referme (Windows)
os.system("pause")
