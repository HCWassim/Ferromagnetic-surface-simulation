# LIBRARY:
import pygame
import math
import random
import numpy as np
import matplotlib.backends.backend_agg as agg
from pygame.locals import *
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import pylab

# CONSTANTE:
# Couleur:
CBlack = (13,13,13)
CDarkGrey = (67, 82, 105) #(68, 68, 68)
CLightGrey = (204, 220, 245) #(166,166,166)
CDarkBlue = (67,82,105)
CLightBlue = (96, 130, 153) #(48, 97, 108)
CRouge = (237, 152, 16) #(245, 103, 83)
CLightBeige = (250,197,50)
# Police:
pygame.font.init()
fontObj1 = pygame.font.SysFont("bahnschrift", 25)
fontObj0 = pygame.font.SysFont("bahnschrift", 20)
escape = "                       "
# Scene Parameter:
pygame.display.set_caption("Ferromagnetism")
SWidth, SHeight = 1500, 800 #HD à noter que 1500 * 800 est un bon format à exploiter
W,H = 250,720
FPS = 100
# Fenetre:
FWindow = pygame.display.set_mode((SWidth,SHeight))
# Constante:
N = 100
K = 1 #.380649 * math.pow(10, -23)
T = 2
BETA = 1 / (K * T)
lst = [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
GRILLE = np.array(lst, dtype=int)
BlockSize = SHeight/N

# BUTTON_AREA = [SWidth-SHeight - 60, 10, 40, 40]
# FONCTION D'UTILITE MULTIPLE:

# Détermine si la souris est dans l'aire du slider:
def MouseIn(x,y,dx,dy,limX,limY):
    return limX<x<limX+dx and limY<y<limY+dy
# Slider:
class Slider:
    def __init__(self,
                 SliderPos:tuple,
                 valMax:int=100,
                 SliderVal:float=100,
                 text:str="T",
                 border:tuple=(200,25)) -> None:
        self.SliderPos = SliderPos # Position ou l'on place le slider
        self.valMax = valMax # Valeur maximal qui peut être atteinte
        self.SliderVal = SliderVal # Valeur du slider
        self.text = text # Text destiné à l'affichage de la température
        self.border = border # Dimension du slider
    # Retourne la valeur du slider:
    def ValeurSlider(self)->float:
        # Produit en croix pour retourner la température
        return self.SliderVal*self.valMax/self.border[0]
    # Affichage du slider avec valeur:
    def AffichageSlider(self,display:pygame.display)->None:
        # Forme du Slider:
        # Fond du slider:
        pygame.draw.rect(display,CRouge,
                         (self.SliderPos[0],
                          self.SliderPos[1],
                          self.border[0],
                          self.border[1]))
        # Position où se situe la température:
        pygame.draw.rect(display,CLightBlue,
                         (self.SliderPos[0],
                          self.SliderPos[1],
                          self.SliderVal,
                          self.border[1]))
        # Bordure du slider:
        pygame.draw.rect(display,CLightGrey,
                         (self.SliderPos[0],
                          self.SliderPos[1],
                          self.border[0],
                          self.border[1]),3)
        # police:
        self.font = pygame.font.Font(pygame.font.get_default_font(), 
                                     int((0.5)*self.border[1]))
        # valeur au milieu du slider:
        # Text:
        valText = self.text+" = "+str(round(self.ValeurSlider(),1))+" °K"
        Temperature = self.font.render(valText,True,CLightGrey)
        # Text centré au centre du slider:
        XTemp = self.SliderPos[0] + (self.border[0]/2) - (Temperature.
                                                          get_rect().width/2)
        # Text au milieu du slider:
        YTemp = self.SliderPos[1] + (self.border[1]/2) - (Temperature.
                                                          get_rect().height/2)
        # Ajout sur Pygame:
        display.blit(Temperature,(XTemp,YTemp))
    # Changer la valeur du slider avec la souris:
    def SliderUpdate(self)->None:
        PSouris = pygame.mouse.get_pos() # Position de la souris
        # On vérifie si la souris est dans le slider:
        if MouseIn(PSouris[0],PSouris[1],
                   self.border[0],
                   self.border[1],
                   self.SliderPos[0],
                   self.SliderPos[1]):
            # Changer la valeur du curseur pour la position de la souris:
            self.SliderVal = PSouris[0] - self.SliderPos[0]
            # Limitation de la taille du slider:
            if self.SliderVal < 0.5:
                self.SliderVal = 0.01
            if self.SliderVal > self.border[0]:
                self.SliderVal = self.border[0]
# Ajouter du Texte:
def NewText(text,h,fontSize=0,allignement="L",color="W"):
    if fontSize:
        if color == "W":
            textobj = fontObj1.render(text,True,CLightGrey)
        else:
            textobj = fontObj1.render(text,True,CDarkGrey)
    else:
        if color == "W":
            textobj = fontObj0.render(text,True,CLightGrey)
        else:
            textobj = fontObj0.render(text,True,CDarkGrey)
    if allignement == "C":
        textrect = textobj.get_rect(center=((SWidth-SHeight)/2,h))
    elif allignement == "L":
        textrect = textobj.get_rect(center=((SWidth-SHeight)/6,h))
    FWindow.blit(textobj,textrect)

# AFFICHAGE:
dimSlider = (630,30)
slider = Slider(
    (SWidth/(SWidth/W)-7*W/8, 80),
    SliderVal=dimSlider[0]/2,
    border=dimSlider,
    valMax=10)

def LivePlotter(screen,x_vec,y_vec,line,position=(0,455),size=(7,3)):
    # Initialisation des figures
    fig = pylab.figure(figsize=size,dpi=100)
    ax = fig.gca()
    # Couleur du graphe, des axes:
    ax.set_facecolor((67/255, 82/255, 105/255))
    fig.patch.set_facecolor((67/255, 82/255, 105/255))
    ax.tick_params(axis='x', colors=(204/255, 220/255, 245/255))
    ax.tick_params(axis='y', colors=(204/255, 220/255, 245/255))
    plt.setp(ax.spines.values(), color=(204/255,220/255,245/255))
    # Couleur des bordures du tableau:
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    # Lissage du tracé :
    XSmooth = np.linspace(x_vec.min(), x_vec.max(), 200)
    spl = make_interp_spline(x_vec,y_vec,k=7) # K coeff de lissage
    YSmooth = spl(XSmooth)
    # Plotting des listes x et y "lissé" et couleur du tracé:
    line, = ax.plot(XSmooth,YSmooth,color=(237/255,152/255,16/255))
    # Transformation de la figure en image lisible par PyGame:
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    # Insertion dans PyGame:
    surf = pygame.image.fromstring(raw_data, canvas.get_width_height(), "RGB")
    screen.blit(surf, position)
    pygame.display.flip()
    # MAJ des données:
    line.set_ydata(y_vec)
    # Suppression de la figure sous matplotlib
    plt.close(fig)
    plt.close("all") #A priori ne sert pas mais on ne sait jamais
    # retour de la liste des données:
    return (line)

# Grille en fond:
def Grid(n=12):
    global BlockSize
    for i in range(n):
        for j in range(n):
            x,y = BlockSize*i + SWidth-SHeight, BlockSize*j
            # rect = pygame.Rect(x,y,BlockSize,BlockSize)
            val = GRILLE[j][i]
            if val == -1:
                pygame.draw.rect(
                    FWindow,
                    CRouge,
                    pygame.Rect(x,y,BlockSize,BlockSize))
            else:
                pygame.draw.rect(
                    FWindow,
                    CLightBlue,
                    pygame.Rect(x,y,BlockSize,BlockSize))

def remplir_cell(cellule):
    x,y = BlockSize*cellule[1] + SWidth-SHeight, BlockSize*cellule[0]
    # rect = pygame.Rect(x,y,BlockSize,BlockSize)
    val = GRILLE[cellule[0]][cellule[1]]
    if val == -1:
        pygame.draw.rect(
            FWindow,
            CRouge,
            pygame.Rect(x,y,BlockSize,BlockSize))
    else:
        pygame.draw.rect(
            FWindow,
            CLightBlue,
            pygame.Rect(x,y,BlockSize,BlockSize))

def variation_energie(coord): # coord = (ligne, colonne) = (y,x)
    y = coord[0]
    x = coord[1]

    cumul = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (j, i) == (0, 0):
                continue
            y_voisin = (y + j + N) % N
            x_voisin = (x + i + N) % N
            cumul += GRILLE[y_voisin][x_voisin]
    
    return 2 * GRILLE[coord[0]][coord[1]] * cumul 

def Beta(T):
    return 1 / (K * T)

def changer_spin(dE, Beta):
    return dE < 0 or random.random() < math.exp(-1 * Beta * dE)

def deplacer(direction):
    global GRILLE
    
    index_axe = {"droite":(-1, 1), #(indice, axe)
                "gauche": (1, 1),
                "haut": (1, 0),
                "bas": (-1, 0)}
    
    index, axe = index_axe[direction]
    partie_une, partie_deux = np.split(GRILLE, [index], axis=axe)
    GRILLE = np.append(partie_deux, partie_une, axis=axe)

# Initialisation:
SOMME_GRILLE = np.sum(GRILLE)
def main():
    Grid(N)
    iteration = 1000
    i = 0
    clock = pygame.time.Clock()
    run = True
    k = 0
    L = 50000
    line1 = []
    global SOMME_GRILLE
    y_vec = np.array([])
    while run:
        k += 1
        clock.tick(FPS)
        T = slider.ValeurSlider()
        # Arrêt du programme:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_DOWN]:
            deplacer("haut")
            Grid(N)
        elif pressed_keys[K_LEFT]:
            deplacer("droite")
            Grid(N)
        elif pressed_keys[K_RIGHT]:
            deplacer("gauche")
            Grid(N)
        elif pressed_keys[K_UP]:
            deplacer("bas")
            Grid(N)  
        for _ in range(iteration):
            cellule = (random.randint(0, N - 1), random.randint(0, N - 1))
            if changer_spin(variation_energie(cellule),Beta(T)):
                GRILLE[cellule[0], cellule[1]] *= -1
                remplir_cell(cellule)
                SOMME_GRILLE += 2 * GRILLE[cellule[0], cellule[1]]
        i += 1
        if i*iteration<L:
            y_vec = np.append(y_vec, SOMME_GRILLE) #rand_val
            x_vec = np.linspace(0,i*iteration,i)
        else:
            y_vec = np.append(y_vec[1:], SOMME_GRILLE)
            x_vec = np.append(x_vec[1:], x_vec[-1] + iteration)
        # Grid(N)
        options(i*iteration,round(clock.get_fps(),2),T,N)
        
        if i > 7:
            line1 = LivePlotter(FWindow,x_vec,y_vec,line1)
        pygame.display.update()
    pygame.quit()
# Panneau de Configuration:
def options(i,fps,t,N):
    pygame.draw.rect(FWindow,CDarkGrey,pygame.Rect(0,0,SWidth-SHeight,SHeight))
    NewText("Panneau de configuration",25,10,allignement="C")
    NewText("Température:", 60)
    slider.AffichageSlider(FWindow)
    slider.SliderUpdate()
    phrase1 = """Utiliser les flèches du clavier pour\
    vous mouvoir à travers la toroïde"""
    NewText(phrase1, 150, allignement="C")
    # Panneau des informations diverses:
    pygame.draw.rect(FWindow,CLightGrey\
        ,pygame.Rect(SWidth/(SWidth/W)-7*W/8,200,630,200),3)
    NewText("Information du système:",220,10,allignement="C")
    phrase2 = 3*escape+"Aimentation:"
    NewText(phrase2,250)
    NewText(
        escape+str(abs(round((np.sum(GRILLE)*100)/(N*N))))+" %",
        250,
        allignement="C")
    NewText(3*escape+"   Itérations:",280) # "                                                                         "
    NewText(escape+str(int(i/1000))+" k",280,allignement="C")
    NewText(3*escape+"             FPS:",310) #                                                                                   
    NewText(escape+str(fps),310,allignement="C")
    NewText(3*escape+"       Beta(T):",340) # "                                                                             "
    NewText(escape+str(round(1/t,2)),340,allignement="C")
    NewText(3*escape+"Taille grille:",370) # "                                                                      "
    NewText(escape+str(N)+"×"+str(N),370,allignement="C")
    NewText(
        "Variation d'Energie en fonction des itérations:",
        440,
        10,
        allignement="C")
    
# Fonctionnement du programme uniquement si l'on utilise ce fichier:
if __name__ == "__main__":
    main()
