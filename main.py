"""
Création d'une application pour la saisie de données des sociétés

La 1ère version ne comprenait que les liens internets (non définis dans ce script)
La 2ème version comprenait en supplément de la saisie et la sauvegarde des données des sociétés
La 3ème version a remplacé le menu déroulant des sociétés sauvegardées par une zone de liste, compte tenu que le menu
déroulant a ses limites (pas de possibilité de mise à jour des données sauf si on fermet et on ouvre l'application...)
La 4ème version porte sur l'alimentation des données des sociétés françaises avec l'API du site pappers.fr
La 5ème version comprend en complément la possibilité de rechercher les sociétés françaises/étrangères en saisissant les
premiers caractères

-> L'enregistrement des données saisies des entreprises françaises et étrangères se fait via le module sqlite3 (base de
données)
-> L'alimentation des données du site pappers.fr se fait via son API en recourant aux modules requests et json pour
récupérer le fichier du site
-> L'enregistrement de la clé du site pappers se fait en se connectant sur le site avec le module webbrowser et la
sauvegarde de la clé, compte tenu de la faible importance de la sauvegarde des données, se fait par sérialisation avec
le module pickle


Éditeur : Laurent REYNAUD
Date : 27-01-2021
"""

from tkinter import messagebox, ttk
from tkinter.tix import *  # pour les infos-bulles
import sqlite3  # bases de données
import requests  # données API -> package installé
import json  # récupération des données API sous format json
import webbrowser  # accès au site pappers.fr
import pickle  # sérialisation de la clé obtenue du site pappers.fr

window = Tk()

"""Configuration de la fenêtre"""
window.title('LRCompta - Données des sociétés')
window.geometry('740x450')
window.resizable(width=False, height=False)

"""Liaison avec la BD des sociétés françaises"""
conn_fr = sqlite3.connect('french_company.db')
c_fr = conn_fr.cursor()
data_fr = c_fr.execute("""SELECT * FROM company""")
my_list_fr = []
for recordfr in data_fr:
    my_list_fr.append(recordfr[2])  # affichage par défaut le nom de la société
    my_list_fr.sort(reverse=True)  # trie par ordre croissant

"""Liaison avec la BD des sociétés étrangères"""
connfo = sqlite3.connect('foreign_company.db')
cursorfo = connfo.cursor()
datafo = cursorfo.execute("""SELECT * FROM company""")
my_list_fo = []
for recordfo in datafo:
    my_list_fo.append(recordfo[2])
    my_list_fo.sort(reverse=True)  # trie par ordre croissant

"""Configuration des onglets"""
my_notebook = ttk.Notebook(window)
my_notebook.pack()

"""Configuration des cadres"""
my_frame1 = Frame(my_notebook, width=500, height=500)
my_frame2 = Frame(my_notebook, width=500, height=500)

"""Affichage des cadres sur toute la longueur et la largeur configurée ci-avant"""
my_frame1.pack(fill='both', expand=1)
my_frame2.pack(fill='both', expand=1)

"""Ajout des onglets"""
my_notebook.add(my_frame1, text='Sociétés françaises')
my_notebook.add(my_frame2, text='Sociétés étrangères')


class FrenchCompanies(Frame):
    """Données de la société française"""

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.widgets()

    def checkfr(self, e):
        """Fonction permettant d'afficher dans la zone de liste les sociétés selon les premiers caractères saisis"""

        """Assignation du texte saisi dans le champ entry"""
        typed = self.entryResearch.get()

        if typed == '':  # si rien n'est saisi
            """Les données de la zone de liste sont inchangées"""
            self.my_listbox.delete(0, END)  # réinitialisation des données
            for item in my_list_fr:  # mise à jour des données
                self.my_listbox.insert(0, item)

        else:  # sinon...
            self.my_listbox.delete(0, END)  # réinitialisation des données
            """Initialisation d'une liste vide"""
            data = []
            """Pour chaque caractère de la liste des sociétés figurant"""
            for item in my_list_fr:
                """Si le caractère saisi est un caractère de la liste d'une des sociétés"""
                if typed.lower() in item.lower():
                    """Ajout du caractère dans la liste 'data'"""
                    data.append(item)
                    """Mise à jour de la zone de liste"""
                    self.my_listbox.insert(END, item)

    def retrieveFr(self):
        """Cette fonction permet de récupérer dans le SGBD les données saisies"""

        title_fr = (self.my_listbox.get(ANCHOR),)
        conn_fr = sqlite3.connect('french_company.db')
        c_fr = conn_fr.cursor()
        request_fr = c_fr.execute("""SELECT * FROM company WHERE Company_name =?""", title_fr)
        res_fr = request_fr.fetchone()
        conn_fr.close()

        """Affichage des données enregistrées"""
        try:
            self.entrySiren.delete(0, END)
            self.entrySiren.insert(0, res_fr[0])
            self.entryFrLegalform.delete(0, END)
            self.entryFrLegalform.insert(0, res_fr[1])
            self.entryFrCompanyname.delete(0, END)
            self.entryFrCompanyname.insert(0, res_fr[2])
            self.entryFrAddress1.delete(0, END)
            self.entryFrAddress1.insert(0, res_fr[3])
            self.entryFrAddress2.delete(0, END)
            self.entryFrAddress2.insert(0, res_fr[4])
            self.entryFrAddress3.delete(0, END)
            self.entryFrAddress3.insert(0, res_fr[5])
            self.entryFrZipcodeCity.delete(0, END)
            self.entryFrZipcodeCity.insert(0, res_fr[6])
            self.entryActivity.delete(0, END)
            self.entryActivity.insert(0, res_fr[7])
            self.entryCreationDate.delete(0, END)
            self.entryCreationDate.insert(0, res_fr[8])
            self.entryCessation.delete(0, END)
            self.entryCessation.insert(0, res_fr[9])
            self.entryEffective.delete(0, END)
            self.entryEffective.insert(0, res_fr[10])
        except TypeError:
            pass

    def destroyFr(self):
        """Cette fonction permet de supprimer dans le SGBD les données saisies"""

        try:
            title_fr = (self.my_listbox.get(ANCHOR),)
            conn_fr = sqlite3.connect('french_company.db')
            c_fr = conn_fr.cursor()
            c_fr.execute("""DELETE FROM company WHERE Company_name =?""", title_fr)
            conn_fr.commit()
            conn_fr.close()
            self.my_listbox.delete(ANCHOR)
            self.entrySiren.delete(0, END)
            self.entryFrLegalform.delete(0, END)
            self.entryFrCompanyname.delete(0, END)
            self.entryFrAddress1.delete(0, END)
            self.entryFrAddress2.delete(0, END)
            self.entryFrAddress3.delete(0, END)
            self.entryFrZipcodeCity.delete(0, END)
            self.entryActivity.delete(0, END)
            self.entryCreationDate.delete(0, END)
            self.entryCessation.delete(0, END)
            self.entryEffective.delete(0, END)
            self.warningDestroyFr = messagebox.showwarning('Suppression', 'Donnée supprimée... dommage !')
            Label(self, text=self.warningDestroyFr).pack()
        except TclError:
            pass

    def deleteFrEntry(self):
        """Fonction permettant d'effacer la saisie faite dans les données de la société française"""
        self.entrySiren.delete(0, END)
        self.entryFrLegalform.delete(0, END)
        self.entryFrCompanyname.delete(0, END)
        self.entryFrAddress1.delete(0, END)
        self.entryFrAddress2.delete(0, END)
        self.entryFrAddress3.delete(0, END)
        self.entryFrZipcodeCity.delete(0, END)
        self.entryActivity.delete(0, END)
        self.entryCreationDate.delete(0, END)
        self.entryCessation.delete(0, END)
        self.entryEffective.delete(0, END)

    def updateFr(self):
        """Cette fonction permet de modifier les données saisies dans le SGBD"""

        title_fr = (self.my_listbox.get(ANCHOR),)
        conn_fr = sqlite3.connect('french_company.db')
        c_fr = conn_fr.cursor()
        myData_fr = (self.entrySiren.get(), self.entryFrLegalform.get(), self.entryFrAddress1.get(),
                     self.entryFrAddress2.get(), self.entryFrAddress3.get(), self.entryFrZipcodeCity.get(),
                     self.entryActivity.get(), self.entryCreationDate.get(), self.entryCessation.get(),
                     self.entryEffective.get(), self.entryFrCompanyname.get())
        c_fr.execute("""UPDATE company SET Siren =?, Legal_form =?, Address1 =?, Address2 =?,
         Address3 =?, ZipcodeCity =?, Activity =?, CreationDate =?, Cessation =?, Effective =? 
         WHERE Company_name =?""", myData_fr)
        conn_fr.commit()
        conn_fr.close()

    def submitFr(self):
        """Fonction permettant d'ajouter les données dans le SGBD"""

        title_fr = (self.my_listbox.get(ANCHOR),)
        conn_fr = sqlite3.connect('french_company.db')
        c_fr = conn_fr.cursor()
        request_fr = c_fr.execute("""SELECT * FROM company WHERE Company_name =?""", title_fr)
        res_fr = request_fr.fetchone()

        try:
            conn_fr = sqlite3.connect('french_company.db')
            c_fr = conn_fr.cursor()
            myData_fr = (self.entrySiren.get(), self.entryFrLegalform.get(), self.entryFrCompanyname.get(),
                         self.entryFrAddress1.get(), self.entryFrAddress2.get(), self.entryFrAddress3.get(),
                         self.entryFrZipcodeCity.get(), self.entryActivity.get(), self.entryCreationDate.get(),
                         self.entryCessation.get(), self.entryEffective.get())
            c_fr.execute("""INSERT INTO company VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", myData_fr)
            conn_fr.commit()
            conn_fr.close()
        except sqlite3.IntegrityError:
            pass

        """Mise à jour de la zone de liste"""
        self.my_listbox.insert(0, self.entryFrCompanyname.get())

    def account_creation(self):
        """Fonction permettant d'enregistrer sa clé sur le site pappers.fr"""

        def callback(url):
            """Fonction pour accéder à l'url pappers.fr - inscription"""
            webbrowser.open_new(url)

        def save_file():
            """Fonction permettant de sauvegarder la clé saisie du site pappers.fr"""
            backup = entry_key.get()
            file_name = 'key_pappers'
            output_file = open(file_name, 'wb')
            pickle.dump(backup, output_file)
            entry_key.delete(0, END)

        """Configuration de la nouvelle fenêtre"""
        new_window = Toplevel(self)
        new_window.title('Enregistrement sur le site pappers.fr')
        new_window.geometry('400x250')
        new_window.resizable(width=False, height=False)

        """Commentaire n° 1 pour expliquer comment s'inscrire sur le site pappers.fr"""
        label_comment1 = Label(new_window,
                               text='Pour pouvoir alimenter les données du site pappers.fr,\n'
                                    'cliquez sur le lien suivant :', font='arial 10 italic')
        label_comment1.pack(pady=10)

        """Accès à l'url : https://www.pappers.fr/api/register"""
        label_access = Label(new_window, text='www.pappers.fr/api/register', font='arial 10 italic', fg='blue')
        label_access.pack()
        label_access.bind('<Button-1>', lambda e: callback('https://www.pappers.fr/api/register'))

        """Commentaire n° 2 pour enregistrer la clé obtenue du site pappers.fr"""
        label_comment2 = Label(new_window,
                               text="puis saisir ci-dessous le n° de la clé obtenu et\n"
                                    "appuyez sur le bouton 'Enregistrer' :",
                               font='arial 10 italic')
        label_comment2.pack(pady=10)

        """Saisie de la clé obtenue"""
        entry_key = Entry(new_window, justify='center', width=60)
        entry_key.pack(pady=10)

        """Bouton pour enregistrer la clé obtenue"""
        button_record = Button(new_window, text='Enregistrer', command=save_file)
        button_record.pack(pady=10)

    def update_data(self):
        """Fonction permettant d'alimenter les données issues du site pappers.fr"""

        """Chargement du fichier contenant la clé saisie sur le site pappers.fr"""
        try:
            file_name = 'key_pappers'
            input_file = open(file_name, 'rb')
            backup = pickle.load(input_file)
        except FileNotFoundError:
            self.entryFrCompanyname.delete(0, END)
            self.entryFrCompanyname.insert(0, "Enregistrer votre clé obtenue du site pappers.fr svp !")

        """Récupération de l'URL de l'API afin d'insérer les données dans le fichier JSON"""
        try:
            """URL de l'API -> https://api.pappers.fr/v1/"""
            api_token = requests.get(
                'https://api.pappers.fr/v1/entreprise?api_token='+f"{backup}"+'&siren='
                + f"{self.entrySiren.get()}")
            """Contenu de l'URL de l'API inséré dans le fichier JSON qui est un dictionnaire"""
            api = json.loads(api_token.content)

            """Réinitialisation des données"""
            self.entryFrLegalform.delete(0, END)
            self.entryFrCompanyname.delete(0, END)
            self.entryActivity.delete(0, END)
            self.entryCreationDate.delete(0, END)
            self.entryCessation.delete(0, END)
            self.entryEffective.delete(0, END)
            self.entryFrAddress1.delete(0, END)
            self.entryFrAddress2.delete(0, END)
            self.entryFrZipcodeCity.delete(0, END)
            self.entryActivity.delete(0, END)
            self.entryCreationDate.delete(0, END)
            self.entryCessation.delete(0, END)
            self.entryEffective.delete(0, END)

            """Alimentation des champs de saisie"""
            self.entryFrLegalform.insert(0, api['forme_juridique'])
            self.entryFrCompanyname.insert(0, api['nom_entreprise'])
            self.entryActivity.insert(0, api['domaine_activite'])
            self.entryCreationDate.insert(0, api['date_creation_formate'])
            if api['entreprise_cessee'] == 0:
                self.entryCessation.insert(0, 'Entreprise en activité')
            else:
                self.entryCessation.insert(0, 'Entreprise cessée')
            self.entryEffective.insert(0, api['effectif'])
            self.entryFrZipcodeCity.insert(0, f"{api['siege']['code_postal']} {api['siege']['ville']}")
            self.entryFrAddress1.insert(0, api['siege']['adresse_ligne_1'])
            self.entryFrAddress2.insert(0, api['siege']['adresse_ligne_2'])
        except Exception as e:
            api = 'Erreur...'

        """Si après téléchargement des données du site pappers, rien ne s'affiche..."""
        if self.entryFrLegalform.get() == '':
            self.entryFrLegalform.insert(0, 'SIREN inconnu...')

    def tvaIntracom(self, *args):
        """Traceur : la saisie du n° SIREN de la société va se générer dans le widget n° TVA intracommunautaire selon
        la formule suivante : [12 + 3 × (SIREN modulo 97)] modulo 97"""

        """Générération du n° de TVA intracommunautaire"""
        if self.varSiren.get() == '':  # si rien est saisi dans ce champ
            self.varTva.set('')
        else:
            try:
                conversion = int(self.varSiren.get())
                if conversion < 100_000_000 or conversion > 999_999_999:  # si la saisi comporte +/- 9 chiffres
                    self.varTva.set('')
                else:
                    res = int((12 + 3 * (conversion % 97)) % 97)  # formule scientifique du n° de TVA intracom
                    if res < 10:
                        res2 = '0' + str(res)
                    else:
                        res2 = res
                    display = f"N° de TVA intracommunautaire : FR{res2} {self.varSiren.get()}"
                    self.varTva.set(display)
            except ValueError:
                self.varTva.set('Erreur de saisie')

    def widgets(self):

        """Titre"""
        self.labelFrTitle = Label(self, text='Identification de la société française', font='Arial 10 bold italic',
                                  bd=1, relief='groove', width=91)
        self.labelFrTitle.grid(row=0, column=0, columnspan=6, pady=10, ipady=5)

        """Recherche d'un société dans la zone de liste"""
        self.labelResearch = Label(self, text='Recherche de société(s) :', font='arial 10 italic')
        self.labelResearch.grid(row=1, column=0, columnspan=2)
        self.entryResearch = Entry(self, justify='center', width=40)
        self.entryResearch.grid(row=2, column=0, columnspan=2)

        """Lien entre le champ de saisi et la zone de liste"""
        self.entryResearch.bind('<KeyRelease>', self.checkfr)

        """Information que le champ de recherche ne permet pas de récupérer les données récemment rajoutées dans la
        zone de liste : il faut refermer l'application et réouvrir pour une mise à jour des données..."""
        tip_research = Balloon(self)
        tip_research.bind_widget(self.entryResearch,
                                 balloonmsg="Attention !\nLa recherche ne prend pas en compte les sociétés\n "
                                            "nouvellement rajoutées :\nIl faut relancer l'application pour une mise à "
                                            "jour\ndes données")

        """Cadre pour la zone de liste et la barre de défilement"""
        self.frame_listbox = Frame(self)
        self.frame_listbox.grid(row=4, column=0, rowspan=8, columnspan=2)

        """Création de la barre de défilement"""
        self.my_scrollbar = Scrollbar(self.frame_listbox, orient=VERTICAL)

        """Listbox"""
        self.my_listbox = Listbox(self.frame_listbox, height=12, width=38, justify='center', activestyle='none',
                                  highlightthickness=0, selectbackground='blue', yscrollcommand=self.my_scrollbar.set)
        for item in my_list_fr:  # Si tu ne mets pas de boucles rien ne se passe...
            self.my_listbox.insert(0, item)

        """Configuration de la barre de défilement"""
        self.my_scrollbar.config(command=self.my_listbox.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        """Affichage de la barre de défilement (instruction à insérer après la config de la barre de défilement"""
        self.my_listbox.pack()

        """SIREN"""
        self.labelInsee = Label(self, text='SIREN :')
        self.labelInsee.grid(row=1, column=2)
        self.varSiren = StringVar()
        self.entrySiren = Entry(self, justify='center', width=60, textvariable=self.varSiren)
        self.varSiren.trace('w', self.tvaIntracom)
        self.entrySiren.grid(row=1, column=3, columnspan=3)

        """Forme juridique"""
        self.labelFrLegalform = Label(self, text='Forme juridique :')
        self.labelFrLegalform.grid(row=2, column=2)
        self.entryFrLegalform = Entry(self, justify='center', width=60)
        self.entryFrLegalform.grid(row=2, column=3, columnspan=3)

        """Dénomination"""
        self.labelFrCompanyname = Label(self, text='Dénomination :')
        self.labelFrCompanyname.grid(row=3, column=2)
        self.entryFrCompanyname = Entry(self, justify='center', width=60)
        self.entryFrCompanyname.grid(row=3, column=3, columnspan=3)

        """Adresse ligne 1"""
        self.labelFrAddress1 = Label(self, text='Adresse 1 :')
        self.labelFrAddress1.grid(row=4, column=2)
        self.entryFrAddress1 = Entry(self, justify='center', width=60)
        self.entryFrAddress1.grid(row=4, column=3, columnspan=3)

        """Adresse ligne 2"""
        self.labelFrAddress2 = Label(self, text='Adresse 2 :')
        self.labelFrAddress2.grid(row=5, column=2)
        self.entryFrAddress2 = Entry(self, justify='center', width=60)
        self.entryFrAddress2.grid(row=5, column=3, columnspan=3)

        """Adresse ligne 3"""
        self.labelFrAddress3 = Label(self, text='Adresse 3 :')
        self.labelFrAddress3.grid(row=6, column=2)
        self.entryFrAddress3 = Entry(self, justify='center', width=60)
        self.entryFrAddress3.grid(row=6, column=3, columnspan=3)

        """Code postal & ville"""
        self.labelFrZipcodeCity = Label(self, text='CP & ville :')
        self.labelFrZipcodeCity.grid(row=7, column=2)
        self.entryFrZipcodeCity = Entry(self, justify='center', width=60)
        self.entryFrZipcodeCity.grid(row=7, column=3, columnspan=3)

        """Activité exercée"""
        self.labelActivity = Label(self, text='Activité :')
        self.labelActivity.grid(row=8, column=2)
        self.entryActivity = Entry(self, justify='center', width=60)
        self.entryActivity.grid(row=8, column=3, columnspan=3)

        """Date de création"""
        self.labelCreationDate = Label(self, text='Date de création :')
        self.labelCreationDate.grid(row=9, column=2)
        self.entryCreationDate = Entry(self, justify='center', width=60)
        self.entryCreationDate.grid(row=9, column=3, columnspan=3)

        """Cessation"""
        self.labelCessation = Label(self, text='Cessation :')
        self.labelCessation.grid(row=10, column=2)
        self.entryCessation = Entry(self, justify='center', width=60)
        self.entryCessation.grid(row=10, column=3, columnspan=3)

        """Effectif"""
        self.labelEffective = Label(self, text='Effectif :')
        self.labelEffective.grid(row=11, column=2)
        self.entryEffective = Entry(self, justify='center', width=60)
        self.entryEffective.grid(row=11, column=3, columnspan=3)

        """Boutons pour la base de données"""
        self.btnFrRead = Button(self, text='Récupérer', width=10, command=self.retrieveFr)
        self.btnFrRead.grid(row=12, column=0, pady=10)
        self.btnFrDestroy = Button(self, text='Supprimer', width=10, command=self.destroyFr)
        self.btnFrDestroy.grid(row=12, column=1, pady=10)
        self.btnFrDelete = Button(self, text='Effacer', width=10, command=self.deleteFrEntry)
        self.btnFrDelete.grid(row=12, column=3, pady=10)
        self.btnFrUpdate = Button(self, text='Modifier', width=10, command=self.updateFr)
        self.btnFrUpdate.grid(row=12, column=4, pady=10)
        self.btnFrCreate = Button(self, text='Ajouter', width=10, command=self.submitFr)
        self.btnFrCreate.grid(row=12, column=5, pady=10)

        """Boutons pour les données du site de pappers.fr"""
        self.btnAccount = Button(self, text='Enregistrement sur le site pappers.fr', command=self.account_creation)
        self.btnAccount.grid(row=13, column=0, columnspan=2, pady=10)
        self.btnDataPappers = Button(self, text='Alimenter les données du site pappers.fr', command=self.update_data)
        self.btnDataPappers.grid(row=13, column=3, columnspan=3, pady=10)

        """N° de TVA intracommunautaire"""
        self.varTva = StringVar()
        self.resTva = Label(self, justify='center', fg='red', textvariable=self.varTva)
        self.resTva.grid(row=14, column=0, columnspan=5, pady=5)

        """Information que le n° de TVA intracommunautaire est un 'calculateur' qu'importe le nombre de chiffres saisis
        dans le champ 'SIREN'"""
        tip_intrac = Balloon(self)
        tip_intrac.bind_widget(self.resTva,
                                 balloonmsg="Attention !\nLe n° de TVA intracommunautaire se calcule\nautomatiquement, "
                                            "il ne permet pas de vérifier si\nle n° SIREN saisi existe !'")


class ForeignCompany(Frame):
    """Données de la société étrangère"""

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.widgets()

    def retrieveFo(self):
        """Cette fonction permet de récupérer dans le SGBD les données saisies"""

        title_fo = (self.my_listboxfo.get(ANCHOR),)
        conn_fo = sqlite3.connect('foreign_company.db')
        c_fo = conn_fo.cursor()
        request_fo = c_fo.execute("""SELECT * FROM company WHERE Company_name =?""", title_fo)
        res_fo = request_fo.fetchone()
        conn_fo.close()

        """Affichage des données enregistrées"""
        try:
            self.entryIdentif.delete(0, END)
            self.entryIdentif.insert(0, res_fo[0])
            self.entryFoLegalform.delete(0, END)
            self.entryFoLegalform.insert(0, res_fo[1])
            self.entryFoCompanyname.delete(0, END)
            self.entryFoCompanyname.insert(0, res_fo[2])
            self.entryFoAddress1.delete(0, END)
            self.entryFoAddress1.insert(0, res_fo[3])
            self.entryFoAddress2.delete(0, END)
            self.entryFoAddress2.insert(0, res_fo[4])
            self.entryFoAddress3.delete(0, END)
            self.entryFoAddress3.insert(0, res_fo[5])
            self.entryFoZipcodeCity.delete(0, END)
            self.entryFoZipcodeCity.insert(0, res_fo[6])
            self.entryFoState.delete(0, END)
            self.entryFoState.insert(0, res_fo[7])
        except TypeError:
            pass

    def destroyFo(self):
        """Cette fonction permet de supprimer dans le SGBD les données saisies"""

        try:
            title_fo = (self.my_listboxfo.get(ANCHOR),)
            conn_fo = sqlite3.connect('foreign_company.db')
            c_fo = conn_fo.cursor()
            c_fo.execute("""DELETE FROM company WHERE Company_name =?""", title_fo)
            conn_fo.commit()
            conn_fo.close()
            self.my_listboxfo.delete(ANCHOR)
            self.entryIdentif.delete(0, END)
            self.entryFoLegalform.delete(0, END)
            self.entryFoCompanyname.delete(0, END)
            self.entryFoAddress1.delete(0, END)
            self.entryFoAddress2.delete(0, END)
            self.entryFoAddress3.delete(0, END)
            self.entryFoZipcodeCity.delete(0, END)
            self.entryFoState.delete(0, END)
            self.warningDestroyFo = messagebox.showwarning('Suppression', 'Donnée supprimée... dommage !')
            Label(self, text=self.warningDestroyFo).pack()
        except TclError:
            pass

    def deleteFoEntry(self):
        """Fonction permettant d'effacer la saisie faite dans les données de la société française"""
        self.entryIdentif.delete(0, END)
        self.entryFoLegalform.delete(0, END)
        self.entryFoCompanyname.delete(0, END)
        self.entryFoAddress1.delete(0, END)
        self.entryFoAddress2.delete(0, END)
        self.entryFoAddress3.delete(0, END)
        self.entryFoZipcodeCity.delete(0, END)
        self.entryFoState.delete(0, END)

    def updateFo(self):
        """Cette fonction permet de modifier les données saisies dans le SGBD"""

        title_fo = (self.my_listboxfo.get(ANCHOR),)
        conn_fo = sqlite3.connect('foreign_company.db')
        c_fo = conn_fo.cursor()
        myData_fo = (self.entryIdentif.get(), self.entryFoLegalform.get(), self.entryFoAddress1.get(),
                     self.entryFoAddress2.get(), self.entryFoAddress3.get(), self.entryFoZipcodeCity.get(),
                     self.entryFoState.get(), self.entryFoCompanyname.get())
        c_fo.execute("""UPDATE company SET Identification =?, Legal_form =?, Address1 =?, Address2 =?,
         Address3 =?, Zipcode_City =?, State =? WHERE Company_name =?""", myData_fo)
        conn_fo.commit()
        conn_fo.close()

    def submitFo(self):
        """Fonction permettant d'ajouter les données dans le SGBD"""

        title_fo = (self.my_listboxfo.get(ANCHOR),)
        conn_fo = sqlite3.connect('foreign_company.db')
        c_fo = conn_fo.cursor()
        request_fo = c_fo.execute("""SELECT * FROM company WHERE Company_name =?""", title_fo)
        res_fo = request_fo.fetchone()

        try:
            conn_fo = sqlite3.connect('foreign_company.db')
            c_fo = conn_fo.cursor()
            myData_fo = (self.entryIdentif.get(), self.entryFoLegalform.get(), self.entryFoCompanyname.get(),
                         self.entryFoAddress1.get(), self.entryFoAddress2.get(), self.entryFoAddress3.get(),
                         self.entryFoZipcodeCity.get(), self.entryFoState.get())
            c_fo.execute("""INSERT INTO company VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", myData_fo)
            conn_fo.commit()
            conn_fo.close()
        except sqlite3.IntegrityError:
            pass

        """Mise à jour de la zone de liste"""
        self.my_listboxfo.insert(0, self.entryFoCompanyname.get())

    def checkfo(self, e):
        """Fonction permettant d'afficher dans la zone de liste les sociétés selon les premiers caractères saisis"""

        """Assignation du texte saisi dans le champ entry"""
        typed = self.entryResearch.get()

        if typed == '':  # si rien n'est saisi
            """Les données de la zone de liste sont inchangées"""
            self.my_listboxfo.delete(0, END)  # réinitialisation des données
            for item in my_list_fo:  # mise à jour des données
                self.my_listboxfo.insert(0, item)

        else:  # sinon...
            self.my_listboxfo.delete(0, END)  # réinitialisation des données
            """Initialisation d'une liste vide"""
            data = []
            """Pour chaque caractère de la liste des sociétés figurant"""
            for item in my_list_fo:
                """Si le caractère saisi est un caractère de la liste d'une des sociétés"""
                if typed.lower() in item.lower():
                    """Ajout du caractère dans la liste 'data'"""
                    data.append(item)
                    """Mise à jour de la zone de liste"""
                    self.my_listboxfo.insert(END, item)

    def widgets(self):

        """Titre"""
        self.labelFoTitle = Label(self, text='Identification de la société étrangère', font='Arial 10 bold italic',
                                  bd=1, relief='groove', width=81)
        self.labelFoTitle.grid(row=0, column=0, columnspan=5, pady=10, ipady=5)

        """Recherche d'un société dans la zone de liste"""
        self.labelResearch = Label(self, text='Recherche de société(s) :', font='arial 10 italic')
        self.labelResearch.grid(row=1, column=0, columnspan=2)
        self.entryResearch = Entry(self, justify='center', width=40)
        self.entryResearch.grid(row=2, column=0, columnspan=2)

        """Lien entre le champ de saisi et la zone de liste"""
        self.entryResearch.bind('<KeyRelease>', self.checkfo)

        """Information que le champ de recherche ne permet pas de récupérer les données récemment rajoutées dans la
        zone de liste : il faut refermer l'application et réouvrir pour une mise à jour des données..."""
        tip_research = Balloon(self)
        tip_research.bind_widget(self.entryResearch,
                                 balloonmsg="Attention !\nLa recherche ne prend pas en compte les sociétés\n "
                                            "nouvellement rajoutées :\nIl faut relancer l'application pour une mise à "
                                            "jour\ndes données")

        """Cadre pour la zone de liste et la barre de défilement"""
        self.frame_listbox = Frame(self)
        self.frame_listbox.grid(row=4, column=0, rowspan=8, columnspan=2, pady=10)

        """Création de la barre de défilement"""
        self.my_scrollbar = Scrollbar(self.frame_listbox, orient=VERTICAL)

        """Listbox"""
        self.my_listboxfo = Listbox(self.frame_listbox, height=12, width=38, justify='center', activestyle='none',
                                    highlightthickness=0, selectbackground='red',
                                    yscrollcommand=self.my_scrollbar.set)
        for item in my_list_fo:  # Si tu ne mets pas de boucles rien ne se passe :p
            self.my_listboxfo.insert(0, item)

        """Configuration de la barre de défilement"""
        self.my_scrollbar.config(command=self.my_listboxfo.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        """Affichage de la barre de défilement (instruction à insérer après la config de la barre de défilement"""
        self.my_listboxfo.pack()

        """N° d'identification"""
        self.labelIdentif = Label(self, text="N° d'identification :")
        self.labelIdentif.grid(row=4, column=2)
        self.entryIdentif = Entry(self, justify='center', width=38)
        self.entryIdentif.grid(row=4, column=3, columnspan=2)

        """Forme juridique"""
        self.labelFoLegalform = Label(self, text='Forme juridique :')
        self.labelFoLegalform.grid(row=5, column=2)
        self.entryFoLegalform = Entry(self, justify='center', width=38)
        self.entryFoLegalform.grid(row=5, column=3, columnspan=2)

        """Dénomination"""
        self.labelFoCompanyname = Label(self, text='Dénomination :')
        self.labelFoCompanyname.grid(row=6, column=2)
        self.entryFoCompanyname = Entry(self, justify='center', width=38)
        self.entryFoCompanyname.grid(row=6, column=3, columnspan=2)

        """Adresse ligne 1"""
        self.labelFoAddress1 = Label(self, text='Adresse 1 :')
        self.labelFoAddress1.grid(row=7, column=2)
        self.entryFoAddress1 = Entry(self, justify='center', width=38)
        self.entryFoAddress1.grid(row=7, column=3, columnspan=2)

        """Adresse ligne 2"""
        self.labelFoAddress2 = Label(self, text='Adresse 2 :')
        self.labelFoAddress2.grid(row=8, column=2)
        self.entryFoAddress2 = Entry(self, justify='center', width=38)
        self.entryFoAddress2.grid(row=8, column=3, columnspan=2)

        """Adresse ligne 3"""
        self.labelFoAddress3 = Label(self, text='Adresse 3 :')
        self.labelFoAddress3.grid(row=9, column=2)
        self.entryFoAddress3 = Entry(self, justify='center', width=38)
        self.entryFoAddress3.grid(row=9, column=3, columnspan=2)

        """Code postal & ville"""
        self.labelFoZipcodeCity = Label(self, text='CP & Ville :')
        self.labelFoZipcodeCity.grid(row=10, column=2)
        self.entryFoZipcodeCity = Entry(self, justify='center', width=38)
        self.entryFoZipcodeCity.grid(row=10, column=3, columnspan=2)

        """Pays"""
        self.labelFoCity = Label(self, text='Pays :')
        self.labelFoCity.grid(row=11, column=2)
        self.entryFoState = Entry(self, justify='center', width=38)
        self.entryFoState.grid(row=11, column=3, columnspan=2)

        """Boutons pour la base de données"""
        self.btnFoRead = Button(self, text='Récupérer', width=10, command=self.retrieveFo)
        self.btnFoRead.grid(row=12, column=0, pady=10)
        self.btnFoDestroy = Button(self, text='Supprimer', width=10, command=self.destroyFo)
        self.btnFoDestroy.grid(row=12, column=1, pady=10)
        self.btnFoDelete = Button(self, text='Effacer', width=10, command=self.deleteFoEntry)
        self.btnFoDelete.grid(row=12, column=2, pady=10)
        self.btnFoUpdate = Button(self, text='Modifier', width=10, command=self.updateFo)
        self.btnFoUpdate.grid(row=12, column=3, pady=10)
        self.btnFoCreate = Button(self, text='Ajouter', width=10, command=self.submitFo)
        self.btnFoCreate.grid(row=12, column=4, pady=10)


"""Instanciation des classes"""
frenchCompanies = FrenchCompanies(my_frame1)  # onglet sociétés françaises
foreignCompany = ForeignCompany(my_frame2)  # onglet sociétés étrangères

"""Commit et arrêts de la connection avec les SGBD"""
conn_fr.commit()
conn_fr.close()
connfo.commit()
connfo.close()

"""Fermeture de fenêtre et arrêt du programme tkinter"""
window.mainloop()
