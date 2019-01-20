#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:03:47 2017

@author: leoportelance
"""

"""
Created on Sat Nov  4 11:40:28 2017

@author: leoportelance
"""
"""


"""
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as mplAnim



Vectdirect = lambda theta: np.array([np.cos(theta),np.sin(theta)])

def orbital(PosPlanet, Mass ,NObject,Radius): 
    """Create NObject orbital position and speed around a central mass at variating radius"""
    
    RandTheta = np.random.rand(NObject) *  2*np.pi
    Vorbital = np.sqrt(G * Mass/Radius)
    v = np.empty([NObject, 2])
    pos =  np.empty([NObject, 2])
    for i in range(NObject):
        pos[i] = PosPlanet[0] + Radius[i] * Vectdirect(RandTheta[i])
        v[i] = Vorbital[i] * Vectdirect(RandTheta[i] - np.pi/2)
       
    return pos,v


def getinput(dt): 
    """Gets require input from the user"""
    
    info = np.empty(3)
    print("Please enter the proper input!")
    print("Units : using Au as distance, solar mass for mass and years for time")
    print("\n Mode 0 : similar to orbital : will places N - 1 masses in random position with the appropirate speed for it to orbit a single central mass") 
    print("\n Mode 1 : Mass,position and speed are chosen randomly inside intervals ")
    Type = int(input("Choose Système Type : similar to orbital(0),purely random(1) -->"))
    NObject = int(input("Choose number of Masses in système -->"))
    Nyear = float(input("Choose number of year to simulate -->"))
    
    if Type == 1:
        info[0] = float(input("Whats is maximum inital distance from center --> ")) 
        info[1] = float(input("Whats is the maximum inital speed  --> "))  
        info[2] = float(input("Whats is maximum mass of bodies  --> "))
        
    if Type == 0:
        info[0] = 10
        if NObject > 20:
            info[0] = 20
        if NObject > 60:
            info[0] = 30
    Niter=int(Nyear/dt)
    return Type,NObject,Niter,info    


def DirectionRadiusVect(pos):
    """ Create an array of radius for each mass to each other body and an array
    of direction vectors for each mass to each other body"""
    O = int(pos.size/2)
    r = np.empty([O,O])
    direct = np.empty([O,O,2])
    for i in range(O):
        x = pos[i] - pos
        r[i] = np.sqrt(x.transpose()[0]**2 + x.transpose()[1]**2) 
        direct[i] = pos - pos[i]
    r[np.where(r == 0)] = 1   
    return r,direct.transpose()




def MovPlanet(NObject,Niter,dt,Type,info):
    """Update de the positon of our masses using the gravity formula and heun's method""" 
    a = np.zeros([NObject,2])
    TabPos = np.empty([Niter,NObject,2])
    
    if (Type == 1):
        pos = np.random.rand(NObject,2) * info[0] * np.random.choice([1,-1],[NObject,2])
        v = np.random.rand(NObject,2) * info[1] * np.random.choice([1,-1],[NObject,2])
        Mass = np.random.rand(NObject) * info[2]
    if Type == 0:
        pos = np.zeros([NObject,2])
        v = np.zeros([NObject,2])
        Mass = np.random.rand(NObject)*0.6
        intRadius = np.random.rand(NObject - 1) * info[0]
        Mass[0] = 10
        pos[1:],v[1:] = orbital(pos[0],Mass[0],NObject - 1,intRadius) 
        
    TabPos = np.empty([Niter,NObject,2])
    
    
    print("Please stand by...Loading")
    for n in range(Niter):
        if not n%(Niter/20):
            print(int(100 * n/Niter), '%' )
             
            
        r1,direction1 = DirectionRadiusVect(pos) 
        a1 =np.sum((((G*Mass)/(r1**3)).transpose() * direction1).transpose(),1) 
        
        
        pos2 = pos + v*dt
        r2,direction2 = DirectionRadiusVect(pos2)
        a2 = np.sum((((G*Mass)/(r1**3)).transpose() * direction1).transpose(),1)
        
        a = 0.5*(a1 + a2)
        
        
        vEuler = v 
        v = v + a * dt 
        pos = pos + 0.5*(v + vEuler)*dt 
    
    
    
        
        TabPos[n] = pos 
        
    return TabPos.transpose()

def LiveAnimation(x,y,limAx,limAy,NObject,TimeStep):
    """Animates our result"""
    
    ColList = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w','b','g']
    def initAnim():
        lines = []
        for k in range(NObject):
            ax.add_line(ligne[k])
            ax.add_patch(cercle[k])
            lines.append(ligne[k])
            lines.append(cercle[k])
        return lines


    def anime(i):
        lines = []
        print(i)
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
        cercle[k]=plt.Circle((None,None),0.1,color=ColList[k%10],zorder=2)

    animation = mplAnim.FuncAnimation(fig, anime, frames=int(x.size/(40*NObject)), interval=TimeStep * 10000, repeat=False, init_func=initAnim,blit=False)
    plt.show()

"""Our constants"""
G = 4 * np.pi**2
dt = 1.e-4

"""Core of Simulation"""

Type,NObject,Niter,info = getinput(dt)   
TabPos = MovPlanet(NObject,Niter,dt,Type,info)
LiveAnimation(TabPos[0],TabPos[1],(-info[0],info[0]),(-info[0],info[0]),NObject,dt)


