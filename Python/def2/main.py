from math import *

def get_f(s: str):
    def f(x: float):
        return eval(s)
    return f

def find_root(f, start: float, stop: float, eps: float, n_max: int):
    a = start
    b = stop
    c = eps
    c_prev = 0
    k = 0
    iter_overload = False
    while abs(c - c_prev) >= eps:
        k += 1
        c_prev = c
        c = a - f(a)/(f(b) - f(a))*(b-a)
        fa = f(a)
        fc = f(c)
        if fa*fc < 0:
            b = c
        else:
            a = c
        if k > n_max:
            iter_overload = True
            break

    return c, iter_overload


func = get_f(input('Введите функцию: '))
a = float(input('Введите левый край отрезка: '))
b = float(input('Введите правый край отрезка: '))
eps = float(input('Введите требуемую точность: '))
n_max = int(input('Введите макс. число итераций: '))
root, over = find_root(func, a, b, eps, n_max)
print('Корень: ', root)
if over:
    print('Максимальное число итераций превышено!')
