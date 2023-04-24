from tkinter import *
import numpy as np

# coordonnees initiales
x0, y0 = 10, 200

# vitesse initiale
alpha = np.pi/3
V0 = 50

# 'pas' du temps
h = 0.1

# coefficient de frottement
k = 0.02

z = np.array([x0, y0, V0*np.cos(alpha), -V0*np.sin(alpha)])


def f(z):
    v = np.array([z[2], z[3]])  # vecteur vitesse (Vx, Vy)
    frottement = -k * v  # force de frottement

    # conditions de rebondissement
    if z[0] < 0 or z[0]+30 > W:
        z[2] = -z[2]

    if z[1] < 0 or z[1]+30 > H:
        z[3] = -z[3]

    # retourne les équations du mouvement
    return np.array([z[2], z[3], frottement[0], 9.81 + frottement[1]])


def Euler():
    global z

    z = z + h*f(z)  # la balle ne s'arrête pas

    # deplacement de la balle a la nouvelle position
    can1.coords(balle, z[0], z[1], z[0] + 30, z[1] + 30)
    # La fenetre fen1 est actualisee en executant la
    # fonction Euler toutes les 10 millisecondes
    fen1.after(10, Euler)


def Heun():
    global z

    k1 = f(z)
    k2 = h*f(z + k1)
    z = z + 1/2*(k1 + k2)  # c'est rapide de zinzin

    can1.coords(balle, z[0], z[1], z[0] + 30, z[1] + 30)
    fen1.after(10, Heun)


# ========== Programme principal =============
# Creation de la fenetre principale :
fen1 = Tk()
fen1.title("Probleme de tir")
# creation du canvas :
H = W = 750
can1 = Canvas(fen1, bg='dark grey', height=H, width=W)
can1.pack()
# creation de la balle
balle = can1.create_oval(x0, y0, x0 + 30, y0 + 30, width=2, fill='red')
# Lancement de la fonction Euler/Heun
Euler()
# demarrage de la boucle principale:
fen1.mainloop()
