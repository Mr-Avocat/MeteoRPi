def Lecture(fichier):
    """enregistre dans une variable le contenu d'un fichier et renvoi cette variable"""
    file = open(fichier, "r+")
    txt = file.read()
    print(txt)
    file.close()
    return txt

def Concat(*txt):
    """concatène de un à n textes et renvoi la concaténation"""
    assert(len(txt) >= 2, "on ne peut concaténer un seul texte")
    concat = ""
    for i in range(len(txt)):
        concat = concat + str(txt[i])
    return concat

def Ecriture(txt, fichier):
    """ecris un texte dans un fichier"""
    file = open(fichier, "w+")
    file.writelines(txt)
    file.close()

fichier1 = "Temp&Press&Humi 07-08-2020 .csv"
fichier2 = "Temp&Press&Humi 08-08-2020 .csv"
fichierCat = "7-8-20 + 8-8-20.csv"

txtFichier1 = Lecture(fichier1)
txtFichier2 = Lecture(fichier2)

txt = Concat(txtFichier1, txtFichier2)

Ecriture(txt, fichierCat)