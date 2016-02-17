__author__ = 'User'
import sys
from tkinter import *
from tkinter import messagebox
import json
class page():
#fonction permettant de créer l'interface tk pour pouvoir entrer les valeurs
    def __init__(self):
        self.julien=Tk()
        self.julien.title("Base de donnée")
        Label(self.julien,text='nom de la bière :').grid(row=0,column=0)
        Label(self.julien,text='cote sur 20 :').grid(row=1,column=0)
        Label(self.julien,text='couleur:').grid(row=2,column=0)
        Label(self.julien,text='type/fermentation').grid(row=3,column=0)
        self.__entré=Entry(self.julien)
        self.__entré.grid(row=0,column=1)
        self.__entré1=Entry(self.julien)
        self.__entré1.grid(row=1,column=1)
        self.__entré2=Entry(self.julien)
        self.__entré2.grid(row=2,column=1)
        self.__entré3=Entry(self.julien)
        self.__entré3.grid(row=3,column=1)
        self.__bouton=Button(self.julien,text='Envoyer',command=self.envoie)
        self.__bouton.grid(row=4,column=0)
        self.__bouton2=Button(self.julien,text='Quitter',command=self.julien.destroy)
        self.__bouton2.grid(row=4,column=2)
        self.__bouton3=Button(self.julien,text='Recherche',command=self.recherche)
        self.__bouton3.grid(row=4,column=1)
        self.liste=[]

#fonction permettant d'envoyer les information de l'interface dans les differentes bases de données
    def envoie(self):
        dico1={}
        a=self.__entré.get()
        b=self.__entré1.get()
        c=self.__entré2.get()
        d=self.__entré3.get()
        liste1=["cote","couleur","type/fermentation"]
        liste2=["Blanche","Ambree","Blonde","Brune","Noire","Rouge","Indeterminer"]
        liste3=["Trappiste","D'Abbaye","Pils","Triple","Quadruple","Double","Indeterminer","Fruite","Houblon","Simple"]
        if a==''or b=='' or c==''or d=='':
            return messagebox . showerror ('Erreur', 'Il manque des information ')

        try:
            e=float(b)
            h=0
            for n in liste2:
                if n==c:
                    dico1[liste1[1]]=c
                    h=1
            if h!=1:
                messagebox . showerror ('Erreur', 'couleur mal ortographié:Chaque mot dois commencer par une Majuscule')
            h=0
            for q in liste3:
                if q==d:
                    dico1[liste1[2]]=d
                    h=1
            if h!=1:
                messagebox . showerror ('Erreur', 'type mal ortographié::Chaque mot dois commencer par une Majuscule')
            dico1[liste1[0]]=e
            document=open("base2.txt",'r')
            enreg=json.load(document)
            document.close()
            enreg[a]=dico1
            réintegration=open("base2.txt","w")
            réintegration.write(json.dumps(enreg,sort_keys=True,indent=4,ensure_ascii=False))
            réintegration.close()
        except:
             messagebox . showerror ('Erreur', 'cote est un nombre')

        li1=["Blanche","Ambree","Blonde","Brune","Noire","Rouge","Indeterminer"]
        li2=["Trappiste","D'Abbaye","Pils","Triple","Quadruple","Double","Indeterminer","Fruite","Simple","Houblon"]
        def traitement(path,r,hj,liste):
            document=open("base2.txt","r")
            enreg=json.load(document)
            document.close()
            liste1=[]
            liste2=[]
            liste3=[]
            liste4=[]
            liste5=[]
            liste6=[]
            liste7=[]
            liste8=[]
            liste9=[]
            liste10=[]
            listebis=[liste1,liste2,liste3,liste4,liste5,liste6,liste7,liste8,liste9,liste10]
            dico={}
            i=0
            while i<len(liste):
                dico[liste[i]]=listebis[i]
                i+=1

            for n in enreg:
                l=[]
                a=enreg[n]
                for t in a:
                    dico1={}
                    if t==hj:
                        h=a[t]
                        l.append(h)
                    if t == "cote":
                        m=a[t]
                        l.append(m)
                    if t==r:
                        for f in dico:
                            if f==a[t]:
                                dico1[n]=l
                                dico[f].append(dico1)
            réintegration=open(path,"w")
            réintegration.write(json.dumps(dico,sort_keys=True,indent=4,ensure_ascii=False))
            réintegration.close()
        traitement("traitement.txt","couleur","type/fermentation",li1)
        traitement("traitement2.txt","type/fermentation","couleur",li2)
#fonction qui créé une interface permettant qui permet de faire une recherche
    def recherche(self):
        self.julien1=Tk()
        self.julien1.title("Recherche")
        Label(self.julien1,text="tapez voter recherche :").grid(row=0,column=0)
        self.__entré4=Entry(self.julien1)
        self.__entré4.grid(row=1,column=0)
        self.__bouton4=Button(self.julien1,text='Ok',command=self.trouver)
        self.__bouton4.grid(row=2,column=0)
        self.__reponse1=Label(self.julien1,text='')
        self.__reponse1.grid(row=3,column=0)
#fonction permettant d'aller chercher les donnée de l'interface recherche dans la base de donnée principal
    def trouver(self):
        a=self.__entré4.get()
        try:
            b=float(a)
            document=open("base2.txt",'r')
            enreg=json.load(document)
            document.close()
            dico5={}
            for n in enreg:
                p=enreg[n]
                for t in p:
                    print(p[t])
                    if p[t]==b:
                        dico5[n]=p
            if dico5=={}:
                self.__reponse1['text']="n'existe pas dans la base de donnée"

            else:
                self.__reponse1['text'] = "{}".format(dico5)
        except:
            document=open("base2.txt",'r')
            enreg=json.load(document)
            document.close()
            dico5={}
            for n in enreg:
                if n == a:
                    dico5[n]=enreg[n]
                else:
                    p=enreg[n]
                    for t in p:
                        if p[t]==a:
                            dico5[n]=p
            if dico5=={}:
                self.__reponse1['text']="n'existe pas dans la base de donnée"

            else:
                self.__reponse1['text'] = "{}".format(dico5)











f=page()
f.julien.mainloop()

