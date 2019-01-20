#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 11:03:19 2018

@author: leoportelance
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as mplAnim
import random

def DirectionRadiusVect(pos,PosFixe):   #Nous sort les vecteur directeur et leur normes
    O = int(pos.size/2)
    P = int(PosFixe.size/2)
    r = np.empty([O,P + O])
    direct = np.empty([O,P + O,2])
    for i in range(O):
        direct[i][:-O] = pos[i] - PosFixe
        direct[i][P:] = pos[i] - pos
    r = np.sqrt(direct.transpose()[0]**2 + direct.transpose()[1]**2).transpose() #L'on génère un tableau de N rayon pour chaque N planet
    r[np.where(r == 0)] = 1  #L'on rend le rayon nulle égale a 1 afin déviter le division par 0    
    return r,direct.transpose()

def Para(x,y,U,du):     #Nous permet de crée des charge ponctuelle pour une courbe paramétrique
    TabPos = np.zeros([int(U/du),2])
    for i in range(int(U/du)):
        TabPos[i][0] = x(i*du)
        TabPos[i][1] = y(i*du)
    return TabPos



def MovObject(NObject,Niter,dt,Charge,SignCharge,PosFixe,shape):
    
    
    ##L'on génère nos condition initiale##
    a = np.zeros([NObject,2])
    TabPos = np.empty([Niter,NObject,2])  
    pos = np.random.rand(NObject,2)
    if shape in [0,1]:
        pos = pos*np.sqrt(2)/2
    elif shape == 2 :
        pos = pos*np.sqrt(2)
        
    v = np.zeros([NObject,2])
    
    print("Please stand by...Loading")
    for n in range(Niter):
        if not n%(Niter/20):
            print(int(100 * n/Niter), '%' )
         #L'on trouve nos position estimer selon euler    
            
        r1,direction1 = DirectionRadiusVect(pos,PosFixe) # L'on trouve nos tableau de rayon et tableau de vecteur directeur au point présent
        a1 = np.sum((Charge[-NObject:] * ((G*Charge)/(r1**3)).transpose() * direction1).transpose(),1) # L'on trouve les accélérations pau point présent
        
        
        pos2 = pos + v*dt
        r2,direction2 = DirectionRadiusVect(pos2,PosFixe)# L'on trouve nos tableau de rayon et tableau de vecteur directeur au point prédit
        a2 = np.sum((Charge[-NObject:] * ((G*Charge)/(r2**3)).transpose() * direction2).transpose(),1)# L'on trouve les accélérations au point prédit
        
        a = 0.5*(a1 + a2) #L'on trouve la moyenne de nos accélération
        vEuler = v 
        v = v + a * dt #L'on trouve nos nouvelle vitesse
        
        cls = np.where(r1 < 1e-2)
        cls = np.unique(cls[0])
        pull = np.where(np.sign(Charge[-NObject:]) != SignCharge)
        stp = np.intersect1d(cls,pull)
        
        a[stp] = 0
        v[stp] = 0
        
        pos = pos + 0.5*(v + vEuler)*dt #L'on trouve nos nouvelle position
        
        
    
    
        
        TabPos[n] = pos #Saves position for later use
        
    return TabPos.transpose()

def LiveAnimation(x,y,xFixe,yFixe,limAx,limAy,NObject,TimeStep):
    """Nous permet d'animé notre simulation"""
    
    ColList = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w','b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    def initAnim():
        lines = []
        plt.plot(xFixe,yFixe, color = 'b' ,linestyle = '',marker = ".", markersize = 0.8)  
        for k in range(NObject):
            ax.add_line(ligne[k])
            ax.add_patch(cercle[k])
            lines.append(ligne[k])
            lines.append(cercle[k])
            
        return lines


    def anime(i):
        lines = []
        xAni = np.empty(NObject)
        yAni = np.empty(NObject)
        for k in range(NObject):
            xAni[k]=x[k,i *20]
            yAni[k]=y[k,i *20]
            ligne[k].set_data(x[k,:i *20],y[k,:i *20 ])
            cercle[k].center=(xAni[k],yAni[k])
            lines.append(ligne[k])
            lines.append(cercle[k])
        return lines
    
    
    
    fig=plt.figure(figsize=[4,4],dpi=200)
    ax=plt.axes(xlim=limAx,ylim=limAy,aspect='equal',autoscale_on=0)
    plt.axvline(linestyle=':')
    plt.axhline(linestyle=':')
    ligne = [plt.plot([],[])[0] for j in range(NObject)]
    cercle = [plt.plot([],[])[0] for j in range(NObject)]
    for k in range(NObject):
        ligne[k]=plt.Line2D((), (),color=ColList[k%10],lw=0.5,zorder=1)
        cercle[k]=plt.Circle((None,None),0.01,color=ColList[k%10],zorder=2)

    animation = mplAnim.FuncAnimation(fig, anime, frames=int(x.size/(40*NObject)), interval=TimeStep * 1000000, repeat=True, init_func=initAnim,blit=False)
    plt.show()
#definie fonction


def getinput(): 
    """nous permet de recevoir du input de l'utilisateur"""
    
    info = np.empty(3)
    print("SVP Rentrez des paramètre approprié!!")
    print("Mouvement d'une  ou plusieurs charge dans un champ électrostatique avec intéraction intercharge")
    Shape = int(input("Choisir forme: cercle(0) , ellipse (1) , cardioid (2),carré  (3) --> "))
    NObject = int(input("Choisir nombre de charge -->"))
    

    return Shape, NObject





shape,NObject = getinput()
""" détermine la paramétrisation de notre courbe selon le choix de l'utilisateur"""
if shape in  [0,1,2]:
    if shape == 0: 
        x = lambda t : np.cos(t)
        y = lambda t: np.sin(t)
    if shape == 1:
        x = lambda t : 3 * np.cos(t)
        y = lambda t: 1 *  np.sin(t)
    elif shape == 2:
        x = lambda t : np.cos(t)*(1+np.cos(t))
        y = lambda t : np.sin(t)*(1+np.cos(t)) 
    U = 2*np.pi
    du = 0.001 * U
    PosFixe = Para(x,y,U,du)

if shape == 3:
    U = 2
    du = 0.01 * U
    x = lambda t : t - 1
    y = lambda t: 1
    PosFixe = Para(x,y,U,du)
    x = lambda t : t - 1
    y = lambda t: -1
    PosFixe = np.insert(PosFixe,0,Para(x,y,U,du),0)
    
    x = lambda t : -1
    y = lambda t: t - 1
    PosFixe = np.insert(PosFixe,0,Para(x,y,U,du),0)
    
    x = lambda t : 1
    y = lambda t: t - 1
    PosFixe = np.insert(PosFixe,0,Para(x,y,U,du),0)
#L'on fixe nos constante
G = 1 / (4 * np.pi * 8.85e-12)
dt = 1e-4


Niter= 10000

"""Détermine la charge de nos charge mobile et de notre courbe fixe"""
ChargeTotal = 50
ChargeFixe = np.empty(PosFixe.shape[0])
ChargeFixe.fill(ChargeTotal / PosFixe.shape[0])
ChargeMob = np.empty(NObject)
ChargeMob.fill(1e-8)




Charge = np.append(ChargeFixe,ChargeMob)
    
TabPos = MovObject(NObject,Niter,dt,Charge,np.sign(ChargeTotal),PosFixe,shape)
PosFixe = PosFixe.transpose()
LiveAnimation(TabPos[0],TabPos[1],PosFixe[0],PosFixe[1],(-2,2),(-2,2),NObject,dt)
