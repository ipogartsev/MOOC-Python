"""
Jeu: Le château au sommet du Python des Neiges
le but du jeu - parcourir le chateau pour trouver la sortie
en chemin: les objects à ramasser, les portes à franchir en répondant aux questions
Auteur: Irina Pogartsev
Date: 20 octobre 2021
"""
from CONFIGS import *
import turtle
import time


def lire_matrice(fichier):
    """creation de la matrice de plan à partir du fichier de données """
    matrice = []
    with open(fichier) as file:
        for line in file:
            line = [int(elem) for elem in line if elem.isdigit()]
            matrice.append(line)
    return matrice


def calculer_pas(matrice):
    """ le calcul de dimensions de la case de plan"""
    pas_lignes = (abs(ZONE_PLAN_MINI[1]) + abs(ZONE_PLAN_MAXI[1])) / len(matrice)
    pas_colognes = (abs(ZONE_PLAN_MINI[0]) + abs(ZONE_PLAN_MAXI[0])) / len(matrice[1])
    if pas_lignes < pas_colognes:
        dimension_case = pas_lignes
    else:
        dimension_case = pas_colognes
    return dimension_case


def coordonnees(case, pas):
    """le calcul des coordonnées du coin inférieur gauche du plan"""
    x = (ZONE_PLAN_MINI[0] + pas * case[1])
    y = (ZONE_PLAN_MAXI[1] - pas * (case[0] + 1))
    return x, y


def tracer_carre(dimension):
    """tracer un carré de la dimension donnée"""
    turtle.down()
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)


def tracer_case(case, couleur, pas):
    """tracer une case sur le plan"""
    turtle.speed(0)
    turtle.ht()
    turtle.up()
    turtle.goto(case)
    turtle.color('White', couleur)
    turtle.down()
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()
    turtle.up()


def afficher_plan(matrice):
    """tracer et afficher le plan de labirynth de la matrice donnée"""
    turtle.speed(0)
    turtle.tracer(10000)
    for ligne in range(len(matrice)):
        for cologne in range(len(matrice[ligne])):
            tracer_case(coordonnees((ligne, cologne), pas), COULEURS[(matrice[ligne][cologne])], pas)


def deplacer(matrice, position, mouvement):
    """Deplacer le personnage de la case de sa position (position) dans la case demandée (mouvement) """
    global case_personnage
    if matrice[mouvement[0]][mouvement[1]] == 2:  # si la case demandée est la case de sortie: afficher le final
        tracer_case(coordonnees(position, pas), COULEURS[5], pas)  # retrace la case de position
        turtle.goto((coordonnees((mouvement), pas)[0] + pas * 0.5, coordonnees((mouvement), pas)[1] + pas * 0.5))
        turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)  # afficher le personnage dans une nouvelle case
        tracer_zone_affichage((52, 220), 230, 470)
        t_zone_affichage((-240, 240), 'Vous avez gagné!', False)
        turtle.onkeypress(None, "Left")  # desactiver la touche Left pendant l'affichage d'annonce d'object
        turtle.onkeypress(None, "Right")
        turtle.onkeypress(None, "Up")
        turtle.onkeypress(None, "Down")
    elif matrice[mouvement[0]][mouvement[1]] == 0:  # vérification si la case est vide
        tracer_case(coordonnees(position, pas), COULEURS[5], pas)  # retrace la case de position
        turtle.goto((coordonnees((mouvement), pas)[0] + pas * 0.5, coordonnees((mouvement), pas)[1] + pas * 0.5))
        turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)  # affiche le personnage dans une nouvelle case
        case_personnage = mouvement
    elif matrice[mouvement[0]][mouvement[1]] == 4:  # vérification d'objet dans une case
        ramasser_objet(position, mouvement)
        case_personnage = mouvement
    elif matrice[mouvement[0]][mouvement[1]] == 3:  # vérification de la porte fermée
        case_personnage = poser_question(matrice, position, mouvement)


def deplacer_gauche():
    """Deplace le personnage dans la case à gauche de la case actuelle si la touche Left a été appuiée"""
    turtle.onkeypress(None, "Left")  # Désactive la touche Left
    case_mouvement = (case_personnage[0], case_personnage[1] - 1)
    if case_personnage[1] != 0 :
        deplacer(plan, case_personnage, case_mouvement)
    turtle.onkeypress(deplacer_gauche, "Left")  # Réassocie la touche Left à  fonction


def deplacer_droite():
    turtle.onkeypress(None, "Right")  # Désactiver la touche Left
    case_mouvement = (case_personnage[0], case_personnage[1] + 1)
    if case_personnage[1] != len(plan[0]) :
       deplacer(plan, case_personnage, case_mouvement) #retracer le personnage dans une nouvelle case
    turtle.onkeypress(deplacer_droite, "Right") #Activer la touche Left

def deplacer_haut():
    turtle.onkeypress(None, "Up")
    case_mouvement = (case_personnage[0] - 1, case_personnage[1])
    if case_personnage[0] != 0 :
        deplacer(plan, case_personnage, case_mouvement)
    turtle.onkeypress(deplacer_haut, "Up")


def deplacer_bas():
    turtle.onkeypress(None, "Down")  # Désactive la touche Left
    case_mouvement = (case_personnage[0] + 1, case_personnage[1])
    if case_personnage[0] != (len(plan) - 1) :
        deplacer(plan, case_personnage, case_mouvement)
    turtle.onkeypress(deplacer_bas, "Down")

def onkeypress_none():
    """Desactivation des touches de mouvement"""
    turtle.onkeypress(None, "Left")
    turtle.onkeypress(None, "Right")
    turtle.onkeypress(None, "Up")
    turtle.onkeypress(None, "Down")

def onkeypress_up():
    """Activation des touches de mouvement"""
    turtle.onkeypress(deplacer_gauche, "Left")  # activer la touche Left
    turtle.onkeypress(deplacer_droite, "Right")
    turtle.onkeypress(deplacer_haut, "Up")
    turtle.onkeypress(deplacer_bas, "Down")

def creer_dictionnaire_des_objets(fichier_des_objets):
    """Création d'une dictionnaire des objets sur le plan selon le fichier donné"""
    dict = {}
    with open(fichier_des_objets, encoding='utf-8') as f:
        for line in f:
            dict.update({eval(line)})
    return dict


def t_zone_affichage(place, texte, bool):
    """l'affichage d'un texte dans une zone d'annonce ou d'inventaire """
    t_zone = turtle.Turtle()
    t_zone.hideturtle()
    t_zone.up()
    t_zone.goto(place)
    t_zone.pencolor('Black')
    if bool:
        for i in range(len(texte)):
            t_zone.write(texte[i], False, 'left', font=("Arial", 7, 'normal', 'bold', 'italic'))
            x, y = t_zone.position()
            t_zone.goto(x, y - 20)
    else:
        t_zone.write(texte, False, 'left', font=("Arial", 8, 'normal', 'bold', 'italic'))


def tracer_zone_affichage(place, longuer, largeur):
    """tracer une zone d'affichage d'annonce ou une zone d'inventaire selon la place indiquée"""
    turtle.speed(0)
    turtle.hideturtle()
    turtle.up()
    turtle.goto(place)
    turtle.color('White')
    turtle.down()
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(longuer)
        turtle.right(90)
        turtle.forward(largeur)
        turtle.right(90)
    turtle.end_fill()
    turtle.up()


def ramasser_objet(position, mouvement):
    """Deplace le personnage, affiche l'annonce d'object trouvée, ajoute et affiche l'object dans l'inventaire"""
    tracer_case(coordonnees(mouvement, pas), COULEURS[0], pas)
    plan[mouvement[0]][mouvement[1]] = 0
    tracer_case(coordonnees(position, pas), COULEURS[5], pas)  # retracer la case de position
    turtle.goto((coordonnees((mouvement), pas)[0] + pas * 0.5, coordonnees((mouvement), pas)[1] + pas * 0.5))
    turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
    onkeypress_none()
    t_zone_affichage((-240, 240), (annonce_objet[:] + dict_objets[mouvement]), False)# afficher l'object trouvé
    time.sleep(1)
    tracer_zone_affichage((-240, 260), 530, 40)  # effacer la zone d'annonce
    inventaire.append(dict_objets[mouvement])  # ajouter d'un object trouvé à inventaire
    tracer_zone_affichage((52, 220), 230, 470)  # effacer la zone d'inventaire
    t_zone_affichage((55, 210), inventaire, True)  # reafficher la zone d'inventaire
    onkeypress_up()

def poser_question(matrice, case, mouvement):
    """Affiche une question à repondre pour ouvrir une porte fermée, deplace le personnage si la réponse est correcte"""
    t_zone_affichage((-240, 240), 'Cette porte est fermée!', False)
    onkeypress_none()
    time.sleep(1)
    tracer_zone_affichage((-240, 260), 530, 40)
    question_reponse = dict_portes[mouvement]
    reponse = turtle.textinput('Question!', question_reponse[0])
    turtle.listen()
    if reponse == question_reponse[1]:
        tracer_case(coordonnees(mouvement, pas), COULEURS[0], pas)
        t_zone_affichage((-240, 240), "La porte s'ouvre!", False)
        time.sleep(1)
        tracer_zone_affichage((-240, 260), 530, 40)
        matrice[mouvement[0]][mouvement[1]] = 0
        tracer_case(coordonnees(case, pas), COULEURS[5], pas)  # retrace la case de position
        turtle.goto((coordonnees((mouvement), pas)[0] + pas * 0.5, coordonnees((mouvement), pas)[1] + pas * 0.5))
        turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE)
        case = mouvement
    else:
        t_zone_affichage((-240, 240), 'Mauvaise réponse !', False)
        time.sleep(1)
        tracer_zone_affichage((-240, 260), 530, 40)
    onkeypress_up()
    turtle.listen()
    return case

plan = lire_matrice('plan_chateau.txt') # créer la matrice du chateau à partire du fichier de données
pas = calculer_pas(plan) # calculer la dimension d'une case
afficher_plan(plan) #  dessiner le plan du chateau
case_personnage = POSITION_DEPART # position d'un personage au debut de jeu
turtle.hideturtle()
turtle.goto(coordonnees((POSITION_DEPART), pas)[0] + pas * 0.5, coordonnees((POSITION_DEPART), pas)[1] + pas * 0.5)
turtle.dot(RATIO_PERSONNAGE * pas, COULEUR_PERSONNAGE) # dessiner le personnage sur la case de départ
dict_objets = creer_dictionnaire_des_objets('dico_objets.txt')
dict_portes = creer_dictionnaire_des_objets('dico_portes.txt')
inventaire = ['  Inventaire :'] # creation d'une liste de l'inventaire
annonce_objet = 'Vous avez trouvé un object: '
turtle.listen()  # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left une fonction appelée
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()  # Place le programme en position d’attente d’une action du jouer




