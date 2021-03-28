# coding=UTF-8

## Import des bibliothèques

from RPLCD.gpio import CharLCD # LCD Display
import bme280 # Code pour la récupération des données du capteur bme280
import time # Pour permettre une pause entre les mesures et dater chaque mesure
import datetime # Pour avoir une date et un typage permettant une chronologie (type = datetime.time or date or datetime)

lcd = CharLCD(cols = 16, rows = 2, pin_rs = 37, pin_e = 35, pins_data = [33, 31, 29, 23]) # Déclaration de la taille du LCD et des pins du LCD

## Fonctions

def Time(date): # Chronologie associée à une variable
    """fonction préparant le forçage le typage de la variable var en datetime.datetime ou datetime.date
    en fonction du booléen date (True = datetime.date; False = datetime.datetime)"""
    if not(date): # si on veut un '.datetime'
        var = time.strftime("%Y-%m-%d|%H:%M:%S") # Récupération de l'année (%Y), du mois (%m), du jour (%d), de l'heure (%H), de la minute (%M) et de la seconde (%S)
        # la ponctuation -|: sont des séparrateurs
    else: # si on veut un '.date'
        var = time.strftime("%Y-%m-%d")
    return DatePourComparaison(var) # utilisation de la fonction forçant le typage


def DatePourComparaison(lst):
    """fonction qui force le typage comme décris plus tôt"""
    #assert(len(lst) == )
    list(lst) # forçage du type de la variable lst en liste
    j = 0 # index de la liste b
    b = [] # création préalable de la liste b
    
    if len(lst) > 10: # liste supposée correspondre à un '.datetime'
        b = ["","","","","",""] # Y-M-D | H:M:S
    else: # liste supposée correspondre à un '.date'
        b = ["", "", ""] #Y-M-D
        
    for i in range(len(lst)): # parcours de la liste
        if lst[i] != "-" and lst[i] != ":" and lst[i] != "|" and type(lst[i]) == str: # décompose la liste
            b[j] = b[j] + lst[i] # concaténation des chaines de caractères
        else:
            j = j + 1 # si on tombe sur un élément de séparation (-|:) on incrémente l'index de la liste b
            
    for k in range(len(b)): # parcours de la liste b
        if b[k] == "": # vérification de la présence d'une information vide
            b[k] = 0 # remplissage manuel d'un élément si vide pour éviter l'érreur "ValueError: invalid literal for int() with base 10: '' " 
            
    if len(lst) > 10: # liste supposée '.datetime'
        d = datetime.datetime(int(b[0]), int(b[1]), int(b[2]), int(b[3]), int(b[4]), int(b[5]))
        # entiers correspondant à Y-m-d|H:M:S
    else: # liste supposée '.date'
        d = datetime.date(int(b[0]), int(b[1]), int(b[2]))
        # entiers correspondant à Y-m-d
    return d # renvoi du datetime.date ou .datetime


def AffichagePrLCD(lcd): 
    """Procédure qui affiche les informations sur le moniteur LCD"""
    lcd.clear() # efface l'écran
    lcd.cursor_pos = (0, 0) # positionne le 'curseur'
    lcd.write_string(str(round(temperature, 2))) # écris les valeurs de température
    lcd.cursor_pos = (0, 5)
    lcd.write_string("C") # écris l'unité des valeurs
    
    lcd.cursor_pos = (0, 7)
    lcd.write_string(str(round(pression, 2))) # Pression
    lcd.cursor_pos = (0, 13)
    lcd.write_string("hPa")
    
    lcd.cursor_pos = (1, 0)
    lcd.write_string(str(round(humidite, 2))) # humidité
    lcd.cursor_pos = (1, 4)
    lcd.write_string("%")
    
    
def PartieDecimale(nb):
    """Fonction qui renvoi la partie décimale d'un flottant"""
    a = nb
    b = int(nb)
    a = a - b
    a = list(str(a))
    b = ""
    for i in range(len(a)):
        if i > 1:
            b = b + str(a[i])
    return b
    
## Application des fonctions    

demarrage = input("Souhaitez-vous un démarrage des mesures tardif ? [o/n] ") # permet de démarrer ou non les mesures à une date donnée
date = Time(False) # variable date de type '.datetime'

if demarrage == "o" or demarrage == "O": # options pour le démarrage à une date donnée
    date_dbt = input("Date de début (Y-M-D) & Heure de début (|H:M:S) : ")
    date_dbt = DatePourComparaison(date_dbt)
    date_fin = input("Date de fin (Y-M-D) & Heure de fin (|H:M:S) : ")
    date_fin = DatePourComparaison(date_fin)
    tpsEntreMesures = int(input("Temps entre chaque mesures en secondes : "))
    
    while date_dbt > date: # tant que l'on est avant la date de démarrage choisie on attend
        date = Time(False) # à optimiser avec un time.sleep pour économiser des ressources processeur
        
else: # option de démarrage instantanné
    date_fin = input("Date de fin (Y-M-D) & Heure de fin (|H:M:S): ")
    date_fin = DatePourComparaison(date_fin)
    tpsEntreMesures = int(input("Temps entre chaque mesures en secondes : "))

date_expT = time.strftime("%d-%m-%Y") # date .csv
date_exp = Time(True) # comparateur pour chronologie .csv (à optimiser si possible)

file_csv = open("/home/pi/Documents/pythonScripts/meteoStat/Temp&Press&Humi {} .csv".format(str(date_expT)), "w")
file_csv.write("DateMesure (H M S); Temperature; Pression; Humidite \n")
# création du fichier pour la sauvegarde des données


date = Time(False) # comparateur avec la date de fin des mesures

dateC = Time(True) # comparateur avec la date journalière du .csv (pour avoir un .csv par jour)

while date_fin >= date: # mesures et affichage
    
    if dateC > date_exp: # gestion du .csv
        
        file_csv.close() # fermeture du .csv du jour précédent
        date_expT = time.strftime("%d-%m-%Y") # date du .csv
        date_exp = Time(True) # comparateur pour chronologie du .csv
        dateC = Time(True) # comparateur pour chronologie du .csv
        
        file_csv = open("/home/pi/Documents/pythonScripts/meteoStat/Temp&Press&Humi {} .csv".format(str(date_expT)), "w")
        file_csv.write("DateMesure (H M S); Temperature; Pression; Humidite \n")
        # création du fichier pour la sauvegarde des données


    temperature, pression, humidite = bme280.readBME280All() # récupération des données
    # sauvegarde des données
    file_csv.write(str(time.strftime("%H:%M:%S"))+ ";" + str(int(temperature)) + "," + str(PartieDecimale(round(temperature, 2 ))) + ";" + str(int(pression)) + "," + str(PartieDecimale(round(pression, 2))) + ";" + str(int(humidite))  + "," + str(PartieDecimale(round(humidite, 2))) + " \n")
    # remplacement des "." par des "," pour les nombres flottants au moment de l'écriture avec la concaténation et à l'aide de la fonction PartieDecimale pour libre office
    
    # affichage provisoire des données
    print(str(temperature) + "C" + str(pression) + "hPa" + str(humidite) + "%")

    AffichagePrLCD(lcd) # affichage des dernières mesures

    time.sleep(tpsEntreMesures) # attente entre les mesures

    date = Time(False) # msie à jour de la date
    dateC = Time(True)

file_csv.close() # fermeture du dernier ficher .csv des mesures
lcd.clear() # effacer le LCD
