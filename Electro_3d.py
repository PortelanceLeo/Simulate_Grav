#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 08:57:27 2018

@author: leoportelance
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as mplAnim



def DirectionRadiusVect(pos,PosFixe):
    O = int(pos.size/3)
    P = int(PosFixe.size/3)
    r = np.empty([O,P + O])
    direct = np.empty([O,P + O,3])
    for i in range(O):
        direct[i][:-O] = pos[i] - PosFixe
        direct[i][P:] = pos[i] - pos
    r = np.sqrt(direct.transpose()[0]**2 + direct.transpose()[1]**2 + direct.transpose()[2]**2).transpose() #L'on génère un tableau de N rayon pour chaque N planet
    r[np.where(r == 0)] = 1  #L'on rend le rayon nulle égale a 1 afin déviter le division par 0    
    return r,direct.transpose()

def para(x,y,z,a,U,du):
    TabPos = np.zeros([int(U/du),3])
    for i in range(int(U/du)):
        TabPos[i][0] = x(i*du,a)
        TabPos[i][1] = y(i*du,a)
        TabPos[i][2] = z(i*du)
    return TabPos



def MovObject(NObject,Niter,dt,Charge,SignCharge,PosFixe):
    
    

    a = np.zeros([NObject,3])
    TabPos = np.empty([Niter,NObject,3]) #"""WATCH OUT RIGHT HERE"""
    pos = np.array([[0,.9,0],[0,.2,0],[0,.8,0]])
    v = np.array([[0,0,2],[0,0,3],[0,0,3]])
    #B = np.array([0,0,1e19])
    
    print("Please stand by...Loading")
    for n in range(Niter):
        if not n%(Niter/20):
            print(int(100 * n/Niter), '%' )
         #L'on trouve nos position estimer selon euler    
            
        
        r1,direction1 = DirectionRadiusVect(pos,PosFixe) # L'on trouve nos tableau de rayon et tableau de vecteur directeur au point présent

        cross = np.empty(PosFixe.shape[1])
        dl = PosFixe - np.roll(PosFixe,1,0)
        cross = np.empty([3,dl.shape[0],3])
        
        for i in range(dl.shape[0]):    
            cross[0][i] = np.cross(dl[i],direction1[0][i])
            cross[1][i] = np.cross(dl[i],direction1[1][i])
            cross[2][i] = np.cross(dl[i],direction1[2][i])
        
        #dl = np.cross((PosFixe - np.roll(PosFixe,1,0)),r1.transpose()[:-NObject].transpose(),axis = 1)
        
        B = np.sum((((H*Charge[:-NObject])/r1.transpose()[:-NObject].transpose()**3).transpose() * cross).transpose(),1)
        #aElectro = np.sum((Charge[-NObject:] * ((G*Charge)/r1**3).transpose() * direction1).transpose(),1) # L'on trouve les accélérations pau point présent
        aMagnet = Charge[-NObject:] * np.cross(v,B).transpose()
        a1 = 1e8* aMagnet
       
    
        pos2 = pos + v*dt
        
        r2,direction2 = DirectionRadiusVect(pos2,PosFixe)# L'on trouve nos tableau de rayon et tableau de vecteur directeur au point prédit
        B = np.sum((((H*Charge[:-NObject])/r2.transpose()[:-NObject].transpose()**3).transpose() * cross).transpose(),1)
        #aElectro = np.sum((Charge[-NObject:] * ((G*Charge)/(r2**3)).transpose() * direction2).transpose(),1)# L'on trouve les accélérations au point prédit
        aMagnet = Charge[-NObject:] * np.cross(v,B).transpose()
        a2 =    1e8*aMagnet
        a = 0.5*(a1 + a2) #L'on trouve la moyenne de nos accélération
        vEuler = v 
        v = v + a * dt #L'on trouve nos nouvelle vitesse
        
        
        
    
        
        pos = pos + 0.5*(v + vEuler)*dt #L'on trouve nos nouvelle position
        
        
    
    
        
        TabPos[n] = pos #Saves position for later use
        
    return TabPos.transpose()

def LiveAnimation(x,y,xFixe,yFixe,limAx,limAy,NObject,TimeStep,N):
    
    
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
    
    
    
    fig=plt.figure(N,figsize=[4,4],dpi=200)
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
"""
def getinput(dt): 
    
    
    info = np.empty(3)
    print("SVP Rentrez des paramètre approprié!!")
    print("Mouvement d'une charge dans un système électromagnétique(Perspective 2d))
    Shape = int(input("Choisir forme: cercle(0) , ellipse (1) , cardioid (2), Carré (3)))
    
    print("\n Mode 0 : Sans champ magnétique") 
    print("\n Mode 1 : Avec champ magnétique")
    print("\n Mode 2 : Avec champ magnétique et intéraction intercharge)
    Type = int(input("Choisir mode -->))
    NObject = int(input("Choisir nombre de charge -->"))
    
    
        
    if Type == 1 | Type == 2:
        champ = float(input("Intensité du champ en z --> " )
        B = np.array([0,0,champ])
    adv = int(input("voir paramètre avancé Non(0)/oui(1) -->"))
    if adv == 1:
        ChargeTotal = float(input("Charge Total de notre courbe"))
        ChargeMob = float(input("Charge des charges mobiles"))
        
    
    return 
"""

x = lambda t,a : a*np.cos(t)
y = lambda t,a : a*np.sin(t)
z = lambda t: 0











#L'on fixe nos constante
G = 1 / (4 * np.pi * 8.85e-12)
H = 12.566370614e-7/(2*np.pi)
dt = 2e-4


Niter= 1000
U = 2*np.pi
du = 0.001 * 2*np.pi
NObject = 3

PosFixe = para(x,y,z,1,U,du)
#for k in np.arange(-2,2.1,0.5):
    #if k != 0:
        #PosFixe = np.insert(PosFixe,0,para(x,y,z,2.1 - np.abs(k),k,U,du),0)





ChargeTotal = - 800
ChargeFixe = np.empty(PosFixe.shape[0])
ChargeFixe.fill(ChargeTotal / PosFixe.shape[0])
ChargeMob = np.empty(NObject)
ChargeMob.fill(1)




Charge = np.append(ChargeFixe,ChargeMob)
TabPos = MovObject(NObject,Niter,dt,Charge,np.sign(ChargeTotal),PosFixe)
PosFixe = PosFixe.transpose()


LiveAnimation(TabPos[0],TabPos[1],PosFixe[0],PosFixe[1],(-2,2),(-2,2),NObject,dt,1)
LiveAnimation(TabPos[0],TabPos[2],PosFixe[0],PosFixe[2],(-2,2),(-2,2),NObject,dt,1)
LiveAnimation(TabPos[1],TabPos[2],PosFixe[1],PosFixe[2],(-2,2),(-2,2),NObject,dt,1)


