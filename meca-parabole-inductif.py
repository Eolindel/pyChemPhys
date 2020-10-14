#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Importer un fichier csv pour un pointage à 25 images par secondes, puis tracer 
y=f(x)
x,y = f(t)
v_x,v_y = f(t)
a_x,a_y = f(t)
et animer le tout. Le fichier csv doit avoir x en première colonne, y en deuxième colonne sans aucune ligne de commentaire (sinon, il faut utiliser le paramètre skiprows de la fonction genfromtxt. L'échelle de temps est recrée à partir de la donnée du nombre d'image par seconde de la vidéo (souvent 25 images par seconde, mais ça peut être 30, 60 ou toute autre valeur, donc il faut adapter judicieusement la valeur). Le fichier d'entrée doit correspondre au format csv donc les champs doivent être séparé par des virgules et les chiffres décimaux doivent être avec des points : donc "3.14" et pas "3,14" pour le nombre correspondant. (il est éventuellement possible de changer le délimiteur dans la fonction genfromtxt) 

Ce script a été réalisé par Martin Vérot, ENS de Lyon sur une idée d'une professeure de physique-chimie dans le secondaire. ( http://chiphoumie.free.fr/ )

Ce script est sous licence CC-BY-NC-SA, ce qui veut dire que vous pouvez l'utiliser, le ré-utiliser, mais en citant l'auteur, il n'est pas possible d'en faire un quelconque usage commercial et si vous ré-utilisez ce script, il faut le distribuer sous la même licence.
"""

# Importation des librairies
import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
from scipy.interpolate import UnivariateSpline


# Definition des fonctions
def animate(time, x, y, t, vx, vy, a_x, a_y):
    """
    Animer les points sur le graphique
    """
    pointTraj.set_data(x[time], y[time])
    pointx.set_data(t[time], x[time])
    pointy.set_data(t[time], y[time])
    pointvx.set_data(t[time],vx[time])
    pointvy.set_data(t[time],vy[time])
    pointax.set_data(t[time],a_x[time])
    pointay.set_data(t[time],a_y[time])
    vx_plot = np.zeros_like(vx)
    vx_plot[time]=vx[time]
    vy_plot = np.zeros_like(vx)
    vy_plot[time]=vy[time]
    vTraj.set_UVC(vx_plot,vy_plot)
    ax_plot = np.zeros_like(vx)
    ax_plot[time]=a_x[time]
    ay_plot = np.zeros_like(vx)
    ay_plot[time]=a_y[time]
    aTraj.set_UVC(ax_plot,ay_plot)
    return [pointTraj,pointx,pointy,pointvx,pointvy,pointax,pointay,vTraj,aTraj]





# Programme principal
if __name__ == "__main__":
    """
    Variables à initialiser
    """
    filename = 'meca-point_parabole_ok.csv'
    movie = "meca-parabolique.mp4" #filename if the animation is saved
    saveMovie = True #Sauvegarder au format mp4 (film)
    fps = 25.
    #Type de fit à faire pour les données : pas de fit avec une formule numérique (nofit) avec un spline quadratique (fitSpline) ou avec un polynôme quadratique en x et y (fitPoly)
    fitSpline = False 
    fitPoly = True
    nofit = False



    """
    Le programme commence après
    """
    #Lire les points dans le fichier, pas de première ligne, x en premier, y en deuxième
    data = np.genfromtxt(filename, delimiter=',')
    x = data[:,0]
    y = data[:,1]
    #Création des valeur du temps t à partir du nombre d'image par seconde 
    t,dt = np.linspace(0,1./fps*(x.size-1),x.size,retstep=True)
    #Fit pour réduire les problèmes d'erreur numérique
    if fitSpline == True:
        y_spl = UnivariateSpline(t,y,k=2)
        x_spl = UnivariateSpline(t,x,k=2)
        vy=y_spl.derivative(n=1)(t)
        vx=x_spl.derivative(n=1)(t)
        a_y=y_spl.derivative(n=2)(t)
        a_x=x_spl.derivative(n=2)(t)
    elif nofit == True: 
        vy=np.gradient(y,dt)
        vx=np.gradient(x,dt)
        a_y=np.gradient(vy,dt)
        a_x=np.gradient(vx,dt)
    elif fitPoly == True:
        py = np.polyfit(t,y,2)
        px = np.polyfit(t,x,2)
        vxf = np.polyder(px)
        vyf = np.polyder(py)
        vx = np.polyval(vxf,t)
        vy = np.polyval(vyf,t)
        a_xf = np.polyder(vxf)
        a_yf = np.polyder(vyf)
        a_x=np.polyval(a_xf,t)
        a_y=np.polyval(a_yf,t)
    else:
        print ('Il manque une option pour appliquer un fit ou non au données')

    #Affichage de la valeur moyenne de l'accélération selon y et x pour voir si on retrouve g
    print('moyenne a_y : {} moyenne a_x {}'.format(np.mean(a_y),np.mean(a_x)))

    #On créé les différents graphs
    fig, ax = plt.subplots(3,2,figsize=(14,7))
    
    #dessin de y=f(x)
    ax1=plt.subplot(1,2,1)
    ax1.plot(x,y, label='trajectoire')
    ax1.set_xlabel('x (m)')
    ax1.set_ylim(bottom = np.min(y+a_y/15),top = np.max(y)*1.1)
    ax1.set_ylabel('y (m)')
    #dessin de x,y = f(t)
    ax2=plt.subplot(3,2,2)
    ax2.plot(t,y, label='y')
    ax2.plot(t,x, label='x')
    ax2.legend(loc='upper right')
    ax2.set_xlabel('t (s)')
    ax2.set_ylabel('y/x (m)')
    #dessin de v_x,v_y=f(t)
    ax3=plt.subplot(3,2,4)
    ax3.plot(t,vy, label='v_y')
    ax3.plot(t,vx, label='v_x')
    ax3.legend(loc='upper right')
    ax3.set_xlabel('t (s)')
    ax3.set_ylabel('v_y/v_x (m)')
    #dessin de a_x, a_y = f(t)
    ax4=plt.subplot(3,2,6)
    ax4.plot(t,a_y, label='a_y')
    ax4.plot(t,a_x, label='a_x')
    ax4.legend(loc='upper right')
    ax4.set_xlabel('t (s)')
    ax4.set_ylabel('a_y/a_x (m)')
    #Tracé des droites horizontales à 0 pour avoir un indice visuel du changement de signe de v_y, de même, le tracé est fait à partir de zéro.
    figs = [ax1, ax2, ax3, ax4] 
    for fi in figs:
        fi.axhline(0., linestyle='-', color='#dddddd')
        fi.set_xlim(left=0.)
    #lignes et points à animer
    pointTraj, = ax1.plot([],[])
    vTraj = ax1.quiver(x,y,[],[],scale = 30,label='v',color='blue')
    aTraj = ax1.quiver(x,y,[],[],scale = 30,label='a',color='red')
    pointx, = ax2.plot([],[],marker='o')
    pointy, = ax2.plot([],[],marker='o')
    pointvx, = ax3.plot([],[],marker='o')
    pointvy, = ax3.plot([],[],marker='o')
    pointax, = ax4.plot([],[],marker='o')
    pointay, = ax4.plot([],[],marker='o')
    #Faire l'animation
    ani = animation.FuncAnimation(fig, animate, fargs =(x, y, t, vx, vy, a_x, a_y), frames=range(t.size), blit=True, save_count=t.size)
    #Pour enregistrer le film ou non en format mp4
    writermp4 = animation.FFMpegWriter() 
    if saveMovie == True:
        ani.save(movie, writer=writermp4)
    plt.tight_layout()
    plt.show()
    pass


