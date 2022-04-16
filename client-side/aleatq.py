import random
import sqlite3

connect=sqlite3.connect("ttmcQ.db")

c=connect.cursor()

#Fonction de selection aléatoire du thème de question.
def selectionQ():
    nb= str(random.randint(1,50))
    req= "SELECT * FROM Questions where Id =" +nb
    res=c.execute(req)
    for resultat in res:
        print(resultat)
    return nb

print(selectionQ())

#Fonction de selection de la question par le joueur
def SelectionJ(nb,question):
    req=str("SELECT Q"+question+" FROM Questions where Id ="+nb)
    res=c.execute(req)
    for resultat in res:
        print(resultat)

print(SelectionJ(selectionQ(),"7"))


#Fonction qui retourne la réponse a la question selectionner par le joueur
def ReponseJ(rep,nb,question):
    req = str("SELECT R"+question+" FROM Reponses where Id="+nb)
    res=c.execute(req)
    for resultat in res:
        resu=resultat[0]
        #print(resu)
        TabRes=resu.split(",")
        return TabRes

print(ReponseJ("oui","1","4"))



