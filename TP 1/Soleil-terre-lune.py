from tkinter import *
import numpy as np
import sys


def f(z):  # Acceleration et Vitesse
    rts = np.sqrt((z[0] - a) ** 2 + (z[1] - b) **
                  2)  # Distance Terre-Soleil \\ sqrt(x^2+y^2) \\
    rtl = np.sqrt((z[4] - z[0]) ** 2 + (z[5] - z[1])
                  ** 2)  # Distance Terre-Lune
    rls = np.sqrt((z[4] - a) ** 2 + (z[5] - b) ** 2)  # Distance Lune-Soleil

    # D'après les équations du système STL données dans l'énoncé :

    Ats = -G * Ms / rts ** 2  # Acceleration induise par le Soleil sur la Terre
    Als = -G * Ms / rls ** 2  # Acceleration induise pas le Soleil sur la Lune
    Alt = -G * Mt / rtl ** 2  # Acceleration induise par la Terre sur la Lune
    Atl = G * Ml / rtl ** 2  # Acceleration induise par la Lune sur la Terre

    # Acceleration selon le vecteur unitaire correspondant i.e. Unitaire_x = Vecteur_x / norme(Vecteur) et Unitaire_y = Vecteur_y / norme(Vecteur)
    Atsx, Atsy = Ats * (z[0] - a) / rts, Ats * (z[1] - b) / rts
    Atlx, Atly = Atl * (z[4] - z[0]) / rtl, Atl * (z[5] - z[1]) / rtl
    Altx, Alty = Alt * (z[4] - z[0]) / rtl, Alt * (z[5] - z[1]) / rtl
    Alsx, Alsy = Als * (z[4] - a) / rls, Als * (z[5] - b) / rls

    # renvoie une liste sous forme (xt', yt', xt'', yt'', xl', yl', xl'', yl'')
    return np.array([z[2], z[3], Atsx + Atlx, Atsy + Atly, z[6], z[7], Altx + Alsx, Alty + Alsy])
    # Exemple : xt'' = Atsx + Atlx car l'accélaration de la Terre en x est la somme de l'accélération provoqué par le Soleil en x et de celle \
    # provoqué par la Lune en x


def Euler():
    global z, h

    # Fonction Euler classique pour résondre z'=f(z)
    z = z + h * f(z)
    x1, y1 = z[0] // k, z[1] // k

    can1.coords(terre, x1, y1, x1 + 20, y1 + 20)
    fen1.after(1, Euler)


def Euler_ameliore():
    global z, h

    # Euler ordre 2 pour résoudre z'=f(z)
    k0 = z + h * f(z)
    z = z + h / 2 * (f(z) + f(k0))
    x1, y1 = z[0] // k, z[1] // k

    can1.coords(terre, x1, y1, x1 + 20, y1 + 20)
    fen1.after(1, Euler_ameliore)


def Range_Kutta():
    global z, h, temps_simulation

    # On résout z' = f(z)
    k1 = f(z)
    k2 = f(z + k1 * h / 2)
    k3 = f(z + k2 * h / 2)
    k4 = f(z + k3 * h)
    z += h/6 * (k1 + 2*k2 + 2*k3 + k4)

    # Nouvelles positions de la Terre avec le bon ordre de grandeur
    x1, y1 = z[0] // k, z[1] // k
    # Nouvelles positions de la Lune avec le bon ordre de grandeur
    xl, yl = (z[4] + 30 * (z[4] - z[0])) // k, (z[5] + 30 * (z[5] - z[1])) // k

    # Deplacement de la Terre et de la Lune a leur nouvelle position
    can1.coords(terre, x1, y1, x1 + 20, y1 + 20)
    can1.coords(lune, xl, yl, xl + 10, yl + 10)

    # La fonction Range_Kutta est executé toutes les milisecondes, on ajoute le pas de temps a chaque exécution
    temps_simulation += h

    if z[0] <= x0:  # Condition d'arret pour 1 révolution
        # On continue de calculer les nouvelles "coordonées" de la Terre et de la Lune en actualisant notre fenêtre
        fen1.after(1, Range_Kutta)
    else:
        print(temps_simulation)
        # permet d'afficher le nombre de jour par an puis par mois
        jours_ecoules = temps_simulation / (24 * 3600)

        # Modifie les arguments var des textes pour afficher le nombre de jour par an et par mois directement sur la fenêtre tkinter
        var2.set("Nombre de jours écoulés pour une révolution: {} // erreur de {} %".format(
            round(jours_ecoules, 2), round(abs(duree_annee-jours_ecoules)/duree_annee*100)))
        var3.set("Nombre de jours écoulés par mois: {} // erreur de {} %".format(round(
            jours_ecoules / 12, 2), round(abs(duree_mois - jours_ecoules/12)/duree_mois*100)))

        # On continue de calculer les nouvelles "coordonées" de la Terre et de la Lune en actualisant notre fenêtre
        fen1.after(1, Range_Kutta)

    if temps_simulation >= 31320000 * 2:  # En imprimant temps_simulation, on a remarqué qu'en un tour la dernière valeure imprimé était 31320000
        sys.exit()  # fermer le système au bout de 2 tours de la Terre autour du Soleil


# ========== Programme principal =============
H, W = 3.0E11, 5.0E11  # La fenêtre est plus lisible qu'en format 4:4
a, b = W / 2, H / 2  # centre de la terre
k = 4.0E8  # Utile pour diminuer l'ordre de grandeur des tailles et distances

# coordonnees initiales
x0, y0 = a + 1.47E11, H / 2  # Terre
# Lune (D'après wikipedia, la distance Terre-Lune est de 384 467 km. On initialise la lune en la décalant uniquement sur X \
# pour simplifier les calculs et avoir une seule composante)
xl0, yl0 = x0 + 3.85E8, y0

# vitesse initiale
V0 = 30200  # Terre
Vl0 = 30200 + 1000  # Lune (D'après wikipedia, V_lune = V_terre + 1000)
alpha = np.pi / 2

# Constante
Ms = 1.989E30
Mt = 5.972E24
Ml = 7.36E22
G = 6.67E-11

# Liste composée des vitesses et positions de la Terre et de la Lune
z = np.array([x0, y0, V0 * np.cos(alpha), -V0 * np.sin(alpha),
             xl0, yl0, Vl0 * np.cos(alpha), -Vl0 * np.sin(alpha)])

# 'pas' du temps
h = 3600

# Pour comparer avec la durée calculée par le programme et avoir une erreur en pourcentage
duree_annee = 365
duree_mois = 30  # Idem
# Variable qui permet de connaitre le temps réel pour que la Terre fasse une révolution autour du Soleil
temps_simulation = 0

fen1 = Tk()
fen1.title("Soleil-Terre-Lune")

# Permet d'écrire sur la fenêtre Tkinter
var = StringVar()
label = Label(fen1, textvariable=var, relief=RAISED)
var.set("Le programme s'arrête automatiquement au bout de 2 révolutions")
label.pack()

var2 = StringVar()
label2 = Label(fen1, textvariable=var2, relief=RAISED)
var2.set("Nombre de jours écoulés pour une révolution:")
label2.pack()

var3 = StringVar()
label3 = Label(fen1, textvariable=var3, relief=RAISED)
var3.set("Nombre de jours écoulés par mois:")
label3.pack()

can1 = Canvas(fen1, bg='dark grey', height=H // k, width=W // k)
can1.pack()

xt, yt = z[0] // k, z[1] // k
terre = can1.create_oval(xt, yt, xt + 20, yt + 20, width=2, fill='blue')
R = 6963400000
R = R*5
x1, y1 = (a - R) // k, (b - R) // k
x2, y2 = (a + R) // k, (b + R) // k
soleil = can1.create_oval(x1, y1, x2, y2, width=2, fill='yellow')

# Création de la Lune avec ses coordonées initiales et de taille 10 car plus petite que la Terre
xl, yl = z[4] // k, z[5] // k
lune = can1.create_oval(xl, yl, xl + 10, yl + 10, width=2, fill='white')

# Lancement de la fonction Range_Kutta
Range_Kutta()
# Boucle principale:
fen1.mainloop()
