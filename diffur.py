"""import libraries"""
import math

import matplotlib
from tqdm import trange
import os
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
import sdy_form
import scipy
from scipy.integrate import RK45, solve_ivp
import time

"""create function, system of DE"""


# Функция составления и использования СДУ, файл с СДУ необходимо назвать "sdy.txt"
# Считываем файлы с параметрами E, k0, T
# Создаем копию системы диффуров и два списка с названием химических элементов и со значениями коэффициентов в СДУ
# Производим замену всех неизвестных в СДУ на значения из двух списков выше
# С помощью метода eval превратим СДУ из строкового типа в математические формулы

def funct():
    R = 8.314
    # R = 0.002
    E = []
    # with open("E.txt") as f:
    with open("каталитический риформинг бензина\E.txt") as f:
        # with open("Каталитический синтез бензилбутилового эфира\E.txt") as f:
        for line_E in f:
            E.append(float(line_E))
    k0 = []
    # with open("k0.txt") as f:
    with open("каталитический риформинг бензина\k0.txt") as f:
        for line_k0 in f:
            k0.append(float(line_k0))
    # with open("Каталитический синтез бензилбутилового эфира\k0.txt") as f:
    #     for line_k0 in f:
    #         k0.append(math.exp(float(line_k0)))
    T0 = []
    # with open("T.txt") as f:
    with open("каталитический риформинг бензина\T.txt") as f:
        # with open("Каталитический синтез бензилбутилового эфира\T.txt") as f:
        for line_T0 in f:
            T0.append(float(line_T0))
    T0 = T0[0]
    k = []

    for i in range(len(E)):
        k.append(str(k0[i]) + '*(math.exp(' + str(-E[i] / R) + '/T))')

    sdy = []
    product = []
    str_k = []
    for j in range(len(k)):
        str_k.append('k' + str(j + 1))
    with open("sdy.txt") as f:
        for line in f:
            sdy.append(line[:-1])
        product = sdy[-1].split()
    sdy = sdy[0:len(sdy) - 1]
    sdy_copy = sdy.copy()
    for m in range(len(sdy)):
        for n in range(len(product)):
            # sdy_copy[m] = sdy_copy[m].replace(product[n] + '**', 'zamena_c[' + str(n) + ']**')
            # доп уравнения
            sdy_copy[m] = sdy_copy[m].replace(product[n] + '/', 'zamena_c[' + str(n) + ']/')
            # доп уравнения
        for v in range(len(k)):
            sdy_copy[m] = sdy_copy[m].replace(str_k[v] + '*', k[v] + '*')

    #####################################################################################################
    # Если реакция неизотермическая
    for q in range(len(product)):
        sdy_copy[-2] = sdy_copy[-2].replace('(' + product[q] + ')', 'zamena_c[' + str(q) + ']')
    #####################################################################################################

    return sdy_copy


def f_ode(C0, t):
    # T не меняется
    # sdy_c, k = funct()
    # zamena_K = k
    # T = 766
    # T не меняется
    # T меняется
    sdy_c = funct()
    T = C0[-2]
    Q = C0[-1]
    # T меняется
    zamena_c = C0
    return_sdy = []
    for ret in range(len(sdy_c)):
        return_sdy.append(eval(sdy_c[ret]))
    return np.array(return_sdy)


def f_rkt_gira(t, C0):
    # T не меняется
    # sdy_c, k = funct()
    # zamena_K = k
    # T = 766
    # T не меняется
    # T меняется
    sdy_c = funct()
    T = C0[-2]
    Q = C0[-1]
    # T меняется
    zamena_c = C0
    return_sdy = []
    for ret in range(len(sdy_c)):
        return_sdy.append(eval(sdy_c[ret]))
    return np.array(return_sdy)


# Функция построения графика изменения концентраций веществ с течением времени
def plot_graphics_odeint(t, func, type):
    list_el = []
    sdy_list = []
    with open("sdy.txt") as f:
        for line in f:
            sdy_list.append(line[:-1])
        list_el = sdy_list[-1].split()
    print(f"Концентрация продуктов в различные моменты времени по методу {type}")
    fig = plt.figure(facecolor='white')
    for line in range(len(func[0]) - 2):
        # for line in range(0,1):
        plt.plot(t, func[:, line], '-o', label='C_' + list_el[line] + '(t)', linewidth=2, markersize=3.5)
    # plt.title(f"Кинетические кривые по методу {type}")
    plt.figtext(0.05, 0.6, 'C, моль/л', fontname='Times New Roman', fontsize=10, color='#000000')
    plt.ylabel("C, моль/л", color='#000000')
    plt.xlabel("τ, условные часы", color='#000000')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontname='Times New Roman', fontsize=10,
               color='#000000')
    plt.locator_params(axis='x', nbins=11)
    plt.grid(True)
    plt.show()  # display


def plot_graphics_rk45_bdf(t, func, type, c_start, c_finish, el_list):
    list_el = []
    sdy_list = []
    with open("sdy.txt") as f:
        for line in f:
            sdy_list.append(line[:-1])
        list_el = sdy_list[-1].split()
    print(f"Концентрация продуктов в различные моменты времени по методу {type}")
    fig = plt.figure(facecolor='white', figsize=(10, 10))
    plt.subplots_adjust(right=0.8)
    for line in range(c_start, c_finish, 1):
        # plt.plot(t, func[line], '-o', label='C_' + list_el[line] + '(t)', linewidth=2, markersize=3.5)
        plt.plot(t, func[line], '-o', label=el_list[line], linewidth=2, markersize=3.5)
    # plt.title(f"Кинетические кривые по методу {type}")
    plt.figtext(0.80, 0.07, 'τ, условные', color='#000000')
    plt.figtext(0.82, 0.03, 'часы', color='#000000')
    plt.figtext(0.1, 0.9, 'C, моль/л', color='#000000')
    legend_properties = {'weight': 'bold'}
    plt.legend(loc='center left', bbox_to_anchor=(0.995, 0.5), labelcolor='black', fontsize='22', prop=legend_properties)
    # plt.ylabel("C, моль/л")
    # plt.xlabel("τ, условные часы")
    plt.locator_params(axis='x', nbins=11)
    plt.grid(True)
    plt.show()  # display


# # Функция построения графика по двум методам (сравнение точности двух методов)
# def plot_graphics_comparsion(func1, func2, type):
#     fig = plt.figure(facecolor='white')
#     list_el = []
#     sdy_list = []
#     with open("sdy.txt") as f:
#         for line in f:
#             sdy_list.append(line[:-1])
#     for i in range(len(sdy_list) - 1):
#         list_el.append(sdy_list[-1][i])
#     for line1 in range(len(func1[0]) - 2):
#         plt.plot(t, func1[:, line1], '-o', label='C_' + list_el[line1] + '(t)_odeint', linewidth=2, markersize=3.5)
#     for line2 in range(len(func2[0]) - 2):
#         plt.plot(t, func2[:, line2], '--', label='C_' + list_el[line2] + '(t)_rkt4', linewidth=2, markersize=3.5)
#     plt.title(f"Сравнение кинетических кривых по методам {type}")
#     plt.ylabel("C, моль/л")
#     plt.xlabel("t, сек")
#     plt.legend()
#     plt.locator_params(axis='x', nbins=11)
#     plt.grid(True)
#     plt.show()  # display


# Функция построения графика температуры
def plot_T(t, func, type):
    fig = plt.figure(facecolor='white')
    plt.subplots_adjust(right=0.8)
    plt.plot(t, func, '-o', label='T(t)', linewidth=2, markersize=3.5)
    # plt.title(f"Кривая изменения температуры по методу {type}")
    plt.figtext(0.80, 0.07, 'τ, условные', color='#000000')
    plt.figtext(0.82, 0.03, 'часы', color='#000000')
    plt.figtext(0.09, 0.92, 'T, К', color='#000000')
    # plt.ylabel("T, К")
    # plt.xlabel("τ, условные часы")
    legend_properties = {'weight': 'bold'}
    plt.legend(loc='center left', bbox_to_anchor=(0.995, 0.5), labelcolor='black', fontsize='22', prop=legend_properties)
    plt.locator_params(axis='x', nbins=11)
    plt.grid(True)
    plt.show()  # display


# Функция построения графика объема по веществам
def plot_Q(t, func, type):
    fig = plt.figure(facecolor='white')
    plt.subplots_adjust(right=0.8)
    fig.set_figwidth(5)
    fig.set_figheight(4)
    plt.plot(t, func, '-o', label='Q(t)', linewidth=2, markersize=3.5)
    # plt.title(f"Кривая изменения объема реакционной смеси по методу {type}")
    plt.figtext(0.80, 0.07, 'τ, условные', color='#000000')
    plt.figtext(0.82, 0.03, 'часы', color='#000000')
    plt.figtext(0.09, 0.92, 'Q, моль', color='#000000')
    # plt.ylabel("Q, моль")
    # plt.xlabel("τ, условные часы")
    legend_properties = {'weight': 'bold'}
    plt.legend(loc='center left', bbox_to_anchor=(0.995, 0.5), labelcolor='black', fontsize='22', prop=legend_properties)
    plt.locator_params(axis='x', nbins=11)
    plt.grid(True)
    plt.show()  # display


matplotlib.rc('font', family='Times New Roman', size=22, weight='bold')
"""stex-matrix input"""
# sdy_form.stex_matrix_to_sdy('stex_matrix.txt')
# sdy_form.stex_matrix_to_sdy(r'каталитический риформинг бензина\stex_matrix.xlsx')
# sdy_form.stex_matrix_to_sdy('Каталитический синтез бензилбутилового эфира/stex_matrix.txt')

C = []
# with open("C0.txt") as f:
with open("каталитический риформинг бензина\C0.txt") as f:
    # with open("Каталитический синтез бензилбутилового эфира\C0.txt") as f:
    for line_C in f:
        C.append(float(line_C))
######################################################################################
# Если система неизотермическая
T0 = []
with open("каталитический риформинг бензина\T.txt") as f:
    for line_T0 in f:
        T0.append(float(line_T0))
T0 = T0[0]
Q = sum(C)
C.append(T0)
C.append(Q)
######################################################################################
"""Decision odeint()"""

# t = np.linspace(0, 60, 61)  # vector of time
t1 = np.linspace(0, 9.6, 10)  # vector of time 1
t2 = np.linspace(9.6, 32.3, 10)  # vector of time 2
t3 = np.linspace(32.3, 60, 10)  # vector of time 3
tt = [t1, t2, t3]
him_el_list = ['nP1', 'nP2', 'nP3', 'nP4', 'iP4', 'nP5', 'iP5', 'nP6', 'iP6', 'nP7', 'iP7', 'nP8', 'iP8', 'nP9', 'iP9',
               'nP10', 'iP10', 'nP11', 'iP11', 'ACH6', 'ACH7', 'ACH8', 'ACH9', 'ACH10', 'ACH11', 'ACP6', 'ACP7', 'ACP8',
               'ACP9', 'ACP10', 'ACP11', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'H2']
# start1 = time.time()
# w1 = odeint(f_ode, C, t1)  # solve eq.
# end1 = time.time()
# print("The time of odeint :", (end1 - start1), "second")
# print('Значения времени t по методу odeint')
# print(t1)
# print('Значения функции по методу odeint')
# print(w1)

"""Decision Runge-Kutty_4"""

# f1 = lambda t, C0: np.array(f_rkt_gira(t, C0))
# start2 = time.time()
# w2 = solve_ivp(f1, (t[0], t[-1]), C, method='RK45', max_step=10, t_eval=t)
# end2 = time.time()
# print("The time of rkt4 :", (end2 - start2), "second")
# print('Значения времени t по методу rk45')
# print(w2.t, '\n')
# print('Значения функции по методу rk45')
# print(w2.y, '\n')
#
"""Decision Gira"""

# f2 = lambda t, C0: np.array(f_rkt_gira(t3, C0))
# start3 = time.time()
# w3 = solve_ivp(f2, (t3[0], t3[-1]), C, method='BDF', max_step=10, t_eval=t3)
# end3 = time.time()
# print("The time of bdf(gira) :", (end3 - start3), "second")
# print('Значения времени t по методу bdf')
# print(w3.t, '\n')
# print('Значения функции по методу bdf')
# print(w3.y, '\n')
#
# """Graphics"""
#
# plot_graphics_odeint(t1, w1, "odeint()")
# plot_graphics_rk45_bdf(w2.t, w2.y, "rk45")
# plot_graphics_rk45_bdf(w3.t, w3.y, "BDF")
# plot_T(t3, w3.y, "gira()")
# plot_Q(t3, w3.y, "gira()")
#
# """Сomparison of methods"""
#
# mse_ode_rk = mean_squared_error(w1, np.transpose(w2.y))
# mse_ode_bdf_gira = mean_squared_error(w1, np.transpose(w3.y))
# mse_rk_bdf_gira = mean_squared_error(np.transpose(w2.y), np.transpose(w3.y))


# print("Mean Squared Error ode_rk", mse_ode_rk)
# print("Mean Squared Error ode_bdf_gira", mse_ode_bdf_gira)
# print("Mean Squared Error rk_bdf_gira", mse_rk_bdf_gira)

#######################################################################
# 1
f_bdf = lambda t, C0: np.array(f_rkt_gira(t1, C0))
start3 = time.time()
w3 = solve_ivp(f_bdf, (t1[0], t1[-1]), C, method='BDF', max_step=10, t_eval=t1)
end3 = time.time()
print("The time of bdf(gira) :", (end3 - start3), "second")
print('Значения времени t по методу bdf')
print(w3.t, '\n')
print('Значения функции по методу bdf')
print(w3.y, '\n')
# plot_graphics_rk45_bdf(w3.t, w3.y, "BDF")
# plot_T(w3.t, w3.y[-2], "gira()")
# plot_Q(w3.t, w3.y[-1], "gira()")

##################
wy = w3.y
wt = w3.t
C0 = wy.copy()
C0 = C0[:, -1]
C0[-2] = 763
C = C0
##################

# 2
f_bdf = lambda t, C0: np.array(f_rkt_gira(t2, C0))
start3 = time.time()
w3 = solve_ivp(f_bdf, (t2[0], t2[-1]), C, method='BDF', max_step=10, t_eval=t2)
end3 = time.time()
print("The time of bdf(gira) :", (end3 - start3), "second")
print('Значения времени t по методу bdf')
print(w3.t, '\n')
print('Значения функции по методу bdf')
print(w3.y, '\n')
# plot_graphics_rk45_bdf(w3.t, w3.y, "BDF")
# plot_T(w3.t, w3.y[-2], "gira()")
# plot_Q(w3.t, w3.y[-1], "gira()")

##################
wy = np.hstack((wy, w3.y))
wt = np.hstack((wt, w3.t))
C0 = wy.copy()
C0 = C0[:, -1]
C0[-2] = 768
C = C0
##################

# 3
f_bdf = lambda t, C0: np.array(f_rkt_gira(t3, C0))
start3 = time.time()
w3 = solve_ivp(f_bdf, (t3[0], t3[-1]), C, method='BDF', max_step=10, t_eval=t3)
end3 = time.time()
print("The time of bdf(gira) :", (end3 - start3), "second")
print('Значения времени t по методу bdf')
print(w3.t, '\n')
print('Значения функции по методу bdf')
print(w3.y, '\n')
# plot_graphics_rk45_bdf(w3.t, w3.y, "BDF")
# plot_T(w3.t, w3.y[-2], "gira()")
# plot_Q(w3.t, w3.y[-1], "gira()")

##################
wy = np.hstack((wy, w3.y))
wt = np.hstack((wt, w3.t))
##################
print(wt)
print(wy[-2])
print(wy[-1])
plot_graphics_rk45_bdf(wt, wy, "BDF", 0, 38, him_el_list)
plot_T(wt, wy[-2], "Гира")
plot_Q(wt, wy[-1], "Гира")
########################################################################
plot_graphics_rk45_bdf(wt, wy, "Гира", 0, 13, him_el_list)
plot_graphics_rk45_bdf(wt, wy, "Гира", 13, 26, him_el_list)
plot_graphics_rk45_bdf(wt, wy, "Гира", 26, 38, him_el_list)
