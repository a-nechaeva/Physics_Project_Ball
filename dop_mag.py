# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from math import sin, pi, radians, cos, sqrt, acos, asin
import numpy as np
import copy

C = 0.51  # коэффициент подъемной силы (0.45 для футбольного мяча) (0.51 для теннисного мяча)
R = 0.0325  # радиус сферы (м) (0.11 для футбольного мяча) (0.0325 для теннисного мяча)
m = 0.055  # масса мяча (кг) (0.430 для футбольного мяча) (0.055 для теннисного мяча)
p = 1.225  # плотность воздуха (кг/м^3)
w_z = 50  # скорость мяча угловая вдоль оси z
alpha = pi / 2  # Угол между v и w
w_x = w_y = 0.0
g = 9.81


dt = 0.001
lT = [0]
lX = [0]
lZ = [0]
lY = [0]

v_y = 0
lYPrim = [v_y]  # как выразить скорость?


def x_second(x_first, y_first, z_first, C, R, p, v, w_z, alpha):
    return (8 / 3) * pi * (R ** 3) * p * sin(alpha) * (w_y * z_first - w_z * y_first) / m


def y_second(x_first, y_first, z_first, C, R, p, v, w_z, alpha):
    return (8 / 3) * pi * (R ** 3) * p * sin(alpha) * (w_z * x_first - w_x * z_first) / m


def z_second(x_first, y_first, z_first, C, R, p, v, w_z, m, g, alpha):
    return -g


def XprimSuiv(x_first, XSecond, dt):
    return x_first + dt * XSecond


def YprimSuiv(y_first, YSecond, dt):
    return y_first + dt * YSecond


def ZprimSuiv(z_first, ZSecond, dt):
    return z_first + dt * ZSecond


def XSuiv(X, x_first, dt):
    return X + dt * x_first


def YSuiv(Y, y_first, dt):
    return Y + dt * y_first


def ZSuiv(Z, z_first, dt):
    return Z + dt * z_first


def tSuiv(t, dt):
    return t + dt

def F_poisk(Xpr, Ypr, Rpr, R, p, m, v_z, g):
    Yo = (Xpr**2 + Ypr**2 - Rpr**2)/((Ypr - Rpr) * 2)
    Deg = (8 * pi * R**3 * p * Yo)/ (3 * m)   # отношение v/w
    KOF = (2 * Yo * Ypr)/(Xpr**2 + Ypr**2)
    S = Yo * 2 * asin((KOF * sqrt(Xpr**2 + Ypr**2))/(2 * Yo))
    Vmin = (S * g) / (2 * v_z)
    Wvmin = Vmin/ Deg
    return Yo, Deg, KOF, S, Vmin, Wvmin


def constructor(lT, lX, lXPrim, lY, lYPrim, lZ, lZPrim, dt, C, R, p, v_1, wz, m, g, alpha):
    while lZ[-1] >= 0:
        lT.append(tSuiv(lT[-1], dt))
        lX.append(XSuiv(lX[-1], lXPrim[-1], dt))
        lY.append(YSuiv(lY[-1], lYPrim[-1], dt))
        lZ.append(ZSuiv(lZ[-1], lZPrim[-1], dt))
        lXPrim.append(XprimSuiv(lXPrim[-1], x_second(lXPrim[-1], lYPrim[-1], lZPrim[-1], C, R, p, v_1, wz, alpha), dt))
        lYPrim.append(YprimSuiv(lYPrim[-1], y_second(lXPrim[-1], lYPrim[-1], lZPrim[-1], C, R, p, v_1, wz, alpha), dt))
        lZPrim.append(
            ZprimSuiv(lZPrim[-1], z_second(lXPrim[-1], lYPrim[-1], lZPrim[-1], C, R, p, v_1, wz, m, g, alpha), dt))
    return lT, lX, lXPrim, lY, lYPrim, lZ, lZPrim



print('Введите координаты по Х и по У, а так же радиус препятствия')
Xpr = int(input())
Ypr = int(input())
Rpr = int(input())
print('Введите начальную скорость по вертикали')
v_z = int(input())

Poisk = F_poisk(Xpr, Ypr, Rpr, R, p, m, v_z, g)
lXPrim_1 = [Poisk[4]]
lZPrim = [v_z]


Tuple = constructor(lT, lX, lXPrim_1, lY, lYPrim, lZ, lZPrim, dt, C, R, p, Poisk[4], Poisk[5], m, g, alpha)

plt.axis([-2, 20, -1, 25])
# добавляем подписи к осям и заголовок диаграммы
plt.xlabel('w, рад/c', fontsize=16)
plt.ylabel('v, м/c', fontsize=16)
plt.title('Множество значений')
# Независимая (x) и зависимая (y) переменные
x = np.linspace(0, 20, 50)
y = x * 1/Poisk[1]
plt.plot(x, y)
yy = np.linspace(0, 25, 50)
xx = Poisk[4] + yy* 0
plt.plot(xx, yy, "r--")
plt.grid(which='major')
plt.show()

plt.axis([-2, 20, -1, 25])
# добавляем подписи к осям и заголовок диаграммы
plt.xlabel('x, м', fontsize=16)
plt.ylabel('y, м', fontsize=16)
plt.title('Траектория полета мяча в плоскости XY')
plt.plot(Tuple[1], Tuple[3])
plt.grid(which='major')
# включаем дополнительную сетку
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
c = plt.Circle((Xpr, Ypr), radius=Rpr)
plt.gca().add_artist(c)
plt.show()


plt.axis([0, 20, -2, 10])
plt.xlabel('x, м', fontsize=16)
plt.ylabel('z, м', fontsize=16)
plt.title('Проекция траектории полета мяча в плоскости XZ')
plt.plot(Tuple[1], Tuple[5])
plt.grid(which='both')
# включаем дополнительную сетку
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.show()

plt.axis([0, 20, -2, 10])
plt.xlabel('y, м', fontsize=16)
plt.ylabel('z, м', fontsize=16)
plt.title('Проекция траектории полета мяча в плоскости YZ')
plt.plot(Tuple[3], Tuple[5])
plt.grid(which='major')
# включаем дополнительную сетку
plt.grid(which='minor', linestyle=':')
plt.tight_layout()
plt.show()