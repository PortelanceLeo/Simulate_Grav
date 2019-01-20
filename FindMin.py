#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 17:26:54 2018

@author: leoportelance
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def DirectionRadiusVect(pos,PosFixe):
    
    P = int(PosFixe.size/2)
    direct = np.empty([P,2])
    direct = pos - PosFixe
    r = np.sqrt(direct.transpose()[0]**2 + direct.transpose()[1]**2).transpose() #L'on génère un tableau de N rayon pour chaque N planet
    r[np.where(r == 0)] = 1  #L'on rend le rayon nulle égale a 1 afin déviter le division par 0    
    return r,direct.transpose()

def para(x,y,U,du):
    TabPos = np.zeros([int(U/du),2])
    for i in range(int(U/du)):
        TabPos[i][0] = x(i*du)
        TabPos[i][1] = y(i*du)
    return TabPos



def MovObject(NObject,Niter,dt,Charge,SignCharge,PosFixe):
    
    debX = 1
    finX = 1.8
    stepX = 0.01
    Nsteps = (finX - debX)/0.01
    
    debY = -.5
    finY = .5
    stepY = (finY - debY)/Nsteps
    #TabMax = np.empty(int((fin-deb)/step)
    
    TabJ =  np.arange(debY,finY,stepY)
    TabI = np.arange(debX,finX,stepX)
    TabV = np.zeros([TabI.size,TabJ.size])
    for i in TabI:
        print(i)
        for j in TabJ:
            a = np.zeros([2])
            #TabPos = np.empty([Niter,2]) #"""WATCH OUT RIGHT HERE"""
        
            pos = np.array([i,j])
            v = np.array([0,0])
            
            Vmax = 0
            for n in range(Niter):
                
                    
                r1,direction1 = DirectionRadiusVect(pos,PosFixe) # L'on trouve nos tableau de rayon et tableau de vecteur directeur au point présent
                a1 = np.sum((Charge[-NObject] * ((G*Charge[:-1])/(r1**3)).transpose() * direction1).transpose(),0) # L'on trouve les accélérations pau point présent
                
                
                pos2 = pos + v*dt
                r2,direction2 = DirectionRadiusVect(pos2,PosFixe)# L'on trouve nos tableau de rayon et tableau de vecteur directeur au point prédit
                a2 = np.sum((Charge[-NObject:] * ((G*Charge[:-1])/(r1**3)).transpose() * direction1).transpose(),0)# L'on trouve les accélérations au point prédit
                
                
                a = 0.5*(a1 + a2) #L'on trouve la moyenne de nos accélération
                vEuler = v 
                v = v + a * dt #L'on trouve nos nouvelle vitesse
                
                
                
                pos = pos + 0.5*(v + vEuler)*dt #L'on trouve nos nouvelle position
                if np.linalg.norm(v) > Vmax:
                    Vmax = np.linalg.norm(v)
            
                
        
                
                #TabPos[n] = pos #Saves position for later use
               
            TabV[int((i - debX)/stepX)][int((j - debY)/stepY)] = Vmax
        #TabMax[int((j - deb)/step)] = np.abs(TabPos[0].max() - TabPos[0].min())
        
        
    return TabV,TabJ,TabI


x = lambda t : np.cos(t)*(1+np.cos(t))
y = lambda t : np.sin(t)*(1+np.cos(t)) 
    



#L'on fixe nos constante
G = 1 / (4 * np.pi * 8.85e-12)
dt = 1e-4


Niter= 10
U = 2*np.pi
du = 0.001 * 2*np.pi
NObject = 1


ChargeTotal = 40
ChargeFixe = np.empty(int(U/du))
ChargeFixe.fill(ChargeTotal / (U/du))
ChargeMob = np.array([1.e-8])


PosFixe = para(x,y,U,du)


ChargeTotal = 50
ChargeFixe = np.empty(PosFixe.shape[0])
ChargeFixe.fill(ChargeTotal / PosFixe.shape[0])
ChargeMob = np.array([1.e-8])




Charge = np.append(ChargeFixe,ChargeMob)
TabV,TabJ,TabI = MovObject(NObject,Niter,dt,Charge,np.sign(ChargeTotal),PosFixe)
PosFixe = PosFixe.transpose()

fig = plt.figure(figsize = [10,10])
ax = fig.gca(projection='3d')
TabV[np.where(TabV > 1e10)] = 0
# Make data.
x, y = np.meshgrid(TabI, TabJ)

# Plot the surface.
surf = ax.plot_surface(y,x, TabV, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
