# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from math import *
from mpl_toolkits.mplot3d import Axes3D
import copy

v_x = 10
v_y = 5
v = sqrt(v_x**2+v_y**2)
v_z = 10

C = 0.   # коэффициент подъемной силы (0.45 для футбольного мяча) (0.51 для теннисного мяча)
R = 0.11      # радиус сферы (м) (0.11 для футбольного мяча) (0.0325 для теннисного мяча)
m = 0.430      # масса мяча (кг) (0.430 для футбольного мяча) (0.055 для теннисного мяча)
p = 1.225     # плотность воздуха (кг/м^3)

w_z = 0 # скорость мяча угловая вдоль оси z
alpha = pi/2      # Угол между v и w
w_x = w_y = 0.0			
g = 9.81


dt = 0.001
lT=[0]
lX=[0]
lXPrim=[v_x]
lZ=[0]
lZPrim=[v_z]
lY=[0]
lYPrim=[v_y]



def x_second(x_first, y_first, z_first, C, R, p, v, w_z, alpha):
    return (8 / 3) * pi * (R**3) * p * sin(alpha) * (w_y * z_first - w_z * y_first) / m


def y_second(x_first,y_first, z_first, C, R, p, v, w_z, alpha):
    return (8 / 3) * pi * (R**3) * p * sin(alpha) * (w_z * x_first - w_x * z_first) / m


def z_second(x_first, y_first, z_first, C, R, p, v, w_z, m, g, alpha):
    return -g
  

def X_firstt(x_first,XSecond, dt):
    return x_first + dt * XSecond

def Y_firstt(y_first,YSecond, dt):
    return y_first + dt * YSecond

def Z_firstt(z_first,ZSecond, dt):
	return z_first + dt * ZSecond

def XSuiv(X,x_first, dt):
    return X + dt * x_first 

def YSuiv(Y,y_first, dt):
    return Y + dt * y_first 

def ZSuiv(Z,z_first, dt):
    return Z + dt * z_first
              
def tSuiv(t,dt):
    return t + dt
    
def constructor(lT,lX,lXPrim,lY,lYPrim,lZ,lZPrim,dt,C, R, p, v, wz, m, g, alpha):
   # temp = 10000
    while lZ[-1] >= 0 :
    #while temp >= 0 :
        #temp -= 1
        lT.append(tSuiv(lT[-1],dt))
        lX.append(XSuiv(lX[-1],lXPrim[-1],dt))
        lY.append(YSuiv(lY[-1],lYPrim[-1],dt))
        lZ.append(ZSuiv(lZ[-1],lZPrim[-1],dt))
        lXPrim.append(X_firstt(lXPrim[-1],x_second(lXPrim[-1],lYPrim[-1],lZPrim[-1], C, R, p, v, wz, alpha), dt))
        lYPrim.append(Y_firstt(lYPrim[-1],y_second(lXPrim[-1],lYPrim[-1],lZPrim[-1], C, R, p, v, wz, alpha), dt))
        lZPrim.append(Z_firstt(lZPrim[-1],z_second(lXPrim[-1],lYPrim[-1],lZPrim[-1], C, R, p, v, wz, m, g , alpha), dt))
    return lT, lX, lXPrim,lY,lYPrim, lZ, lZPrim


Tuple = constructor(lT,lX,lXPrim,lY,lYPrim,lZ,lZPrim,dt,C, R, p, v, w_z, m, g, alpha)
plt.axis([-1,25,-1,20])
# добавляем подписи к осям и заголовок диаграммы
plt.xlabel('x, м', fontsize=16)
plt.ylabel('y, м', fontsize=16)
plt.title('Проекция траектории полета мяча в плоскости XY')
plt.plot(Tuple[1],Tuple[3])
'''c = plt.Circle((2, 3), radius=1)
plt.gca().add_artist(c)
'''
plt.grid(which='major')
# включаем дополнительную сетку
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.show()

plt.axis([0,25,-2,6])
plt.xlabel('x, м', fontsize=16)
plt.ylabel('z, м', fontsize=16)
plt.title('Проекция траектории полета мяча в плоскости XZ')
plt.plot(Tuple[1],Tuple[5])
plt.grid(which='both')
# включаем дополнительную сетку
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.show()

plt.axis([0,15,-2,6])
plt.xlabel('y, м', fontsize=16)
plt.ylabel('z, м', fontsize=16)
plt.title('Проекция траектории полета мяча в плоскости YZ')
plt.plot(Tuple[3],Tuple[5])
plt.grid(which='major')
# включаем дополнительную сетку
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(Tuple[1], Tuple[3], Tuple[5], label='parametric curve')

                  
             
               