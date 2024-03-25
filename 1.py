"""import libraries"""

import math
from threading import Thread
import matplotlib
import sdy_form_izoterma
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
import tkinter
from tkinter import *

# библиотеки для интерфейса
from tkinter import Tk, Listbox, Button, Scrollbar, MULTIPLE, END, RIGHT, Y, filedialog, messagebox, ttk
from tkinter import *

"""create function, system of DE"""


# Функция составления и использования СДУ, файл с СДУ необходимо назвать "sdy.txt"
# Считываем файлы с параметрами E, k0, T
# Создаем копию системы диффуров и два списка с названием химических элементов и со значениями коэффициентов в СДУ
# Производим замену всех неизвестных в СДУ на значения из двух списков выше
# С помощью метода eval превратим СДУ из строкового типа в математические формулы

def interface_of_graphics(file_E, file_k0, file_T0, file_C0, path_sdy):
    def k_k():
        R = 2
        E = []
        with open(file_E) as f:
            for line_E in f:
                E.append(float(line_E))
        k0 = []
        with open(file_k0) as f:
            for line_k0 in f:
                k0.append(float(line_k0))

        global T0
        T0 = []
        with open(file_T0) as f:
            for line_T0 in f:
                T0.append(float(line_T0))
        T0 = T0[0]

        k = []
        for i in range(len(E)):
            k.append(k0[i]*(math.exp(-E[i] / (R * T0))))

        f_k = open(path_sdy + 'K_izoterma.txt', 'w') # открытие в режиме записи, если нет такого файла, то создаается
        for i in range(len(k) - 1):
            f_k.write(str(k[i]) + '\n')
        f_k.write(str(k[len(k) - 1]))

    def funct():
        R = 2
        E = []
        with open(file_E) as f:
            for line_E in f:
                E.append(float(line_E))
        k0 = []
        with open(file_k0) as f:
            for line_k0 in f:
                k0.append(float(line_k0))

        global T0
        T0 = []
        with open(file_T0) as f:
            for line_T0 in f:
                T0.append(float(line_T0))
        T0 = T0[0]

        k = []
        for i in range(len(E)):
            k.append(str(k0[i]) + '*(math.exp(' + str(-E[i] / R) + '/T))')
        # print(k)
        sdy = []
        product = []
        str_k = []
        for j in range(len(k)):
            str_k.append('k' + str(j + 1))
        with open(path_sdy + "sdy_izoterma.txt") as f:
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

        return sdy_copy

    def f_ode(C0, t):
        # T не меняется
        sdy_c = funct()
        # zamena_K = k
        T = T0
        Q = C0[-1]
        # T не меняется
        zamena_c = C0
        return_sdy = []
        for ret in range(len(sdy_c)):
            return_sdy.append(eval(sdy_c[ret]))
        return np.array(return_sdy)

    def f_rkt_gira(t, C0):
        # T не меняется
        sdy_c = funct()
        # zamena_K = k
        T = T0
        # T не меняется
        Q = C0[-1]
        zamena_c = C0
        return_sdy = []
        for ret in range(len(sdy_c)):
            return_sdy.append(eval(sdy_c[ret]))
        return np.array(return_sdy)

    # Функция для построения графиков с использованием интерфейса
    def plot_graphics_rk45_bdf_interface(times_Gira, values_Gira, el_list):
        plt.subplots_adjust(right=0.75)
        for i in range(len(values_Gira)):
            plt.plot(times_Gira, values_Gira[i], '-o', label=him_el_list[el_list[i]], linewidth=2, markersize=3.5)
        # plt.title(f"Кинетические кривые по методу")
        legend_properties = {'weight': 'bold'}
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), labelcolor='black', fontsize='12',
                   prop=legend_properties)
        plt.ylabel("C, моль/л")
        plt.xlabel("τ, условные минуты")
        plt.locator_params(axis='x', nbins=11)
        plt.grid(True)
        plt.show()

    # Функция обработки события нажатия на кнопку
    def button_click_Gira():
        selected_indices_Gira = listbox_concentration.curselection()  # возвращает набор индексов выделенных элементов
        selected_values_Gira = [values_Gira[i] for i in selected_indices_Gira]
        plot_graphics_rk45_bdf_interface(times_Gira, selected_values_Gira, selected_indices_Gira)

    def button_click_Gira_T():
        plot_T_interface(times_Gira)

    def button_click_Gira_Q():
        plot_Q_interface(times_Gira, values_Gira)

    def button_click_Gira_W():
        selected_indices_Gira_W = listbox_stad.curselection()  # возвращает набор индексов выделенных элементов
        selected_values_Gira_W = [return_w_all_gira[i] for i in selected_indices_Gira_W]
        plot_W_interface(times_Gira, selected_values_Gira_W, selected_indices_Gira_W)

    def button_click_RK45():
        selected_indices_RK45 = listbox_concentration.curselection()  # возвращает набор индексов выделенных элементов
        selected_values_RK45 = [values_RK45[i] for i in selected_indices_RK45]
        plot_graphics_rk45_bdf_interface(times_RK45, selected_values_RK45, selected_indices_RK45)

    def button_click_RK45_T():
        plot_T_interface(times_RK45)

    def button_click_RK45_Q():
        plot_Q_interface(times_RK45, values_RK45)

    def button_click_RK45_W():
        selected_indices_RK45_W = listbox_stad.curselection()  # возвращает набор индексов выделенных элементов
        selected_values_RK45_W = [return_w_all_rk45[i] for i in selected_indices_RK45_W]
        plot_W_interface(times_RK45, selected_values_RK45_W, selected_indices_RK45_W)

    def plot_graphics_rk45_bdf(t, func, type, c_start, c_finish, el_list):
        list_el = []
        sdy_list = []
        with open(path_sdy + "sdy_izoterma.txt") as f:
            for line in f:
                sdy_list.append(line[:-1])
            list_el = sdy_list[-1].split()
        print(f"Концентрация продуктов в различные моменты времени по методу {type}")
        fig = plt.figure(facecolor='white')
        for line in range(c_start, c_finish, 1):
            # plt.plot(t, func[line], '-o', label='C_' + list_el[line] + '(t)', linewidth=2, markersize=3.5)
            plt.plot(t, func[line], '-o', label=el_list[line], linewidth=2, markersize=3.5)
        # plt.title(f"Кинетические кривые по методу {type}")
        plt.figtext(0.91, 0.11, 'τ, условные', color='#000000')
        plt.figtext(0.93, 0.09, 'минуты', color='#000000')
        plt.figtext(0.09, 0.9, 'C, моль/л', color='#000000')
        legend_properties = {'weight': 'bold'}
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), labelcolor='black', fontsize='16',
                   prop=legend_properties)
        # plt.ylabel("C, моль/л")
        # plt.xlabel("τ, условные часы")
        plt.locator_params(axis='x', nbins=11)
        plt.grid(True)
        plt.show()  # display

    def plot_T_interface(time):
        fig = plt.figure(facecolor='white')
        plt.plot(time, [T0] * len(time), '-o', label='T(t)', linewidth=2, markersize=3.5)
        plt.title("Кривая изменения температуры")
        # plt.figtext(0.91, 0.11, 'τ, условные', color='#000000')
        # plt.figtext(0.93, 0.09, 'часы', color='#000000')
        # plt.figtext(0.12, 0.9, 'T, К', color='#000000')
        plt.ylabel("T, К")
        plt.xlabel("τ, условные минуты")
        legend_properties = {'weight': 'bold'}
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), labelcolor='black', fontsize='16',
                   prop=legend_properties)
        plt.locator_params(axis='x', nbins=11)
        plt.grid(True)
        plt.show()  # display

    def plot_Q_interface(time, val):
        fig = plt.figure(facecolor='white')
        plt.plot(time, val[-1], '-o', label='Q(t)', linewidth=2, markersize=3.5)
        plt.title("Кривая изменения объема реакционной смеси")
        # plt.figtext(0.91, 0.11, 'τ, условные', color='#000000')
        # plt.figtext(0.93, 0.09, 'часы', color='#000000')
        # plt.figtext(0.1, 0.9, 'Q, моль', color='#000000')
        plt.ylabel("Q, моль")
        plt.xlabel("τ, условные минуты")
        legend_properties = {'weight': 'bold'}
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), labelcolor='black', fontsize='16',
                   prop=legend_properties)
        plt.locator_params(axis='x', nbins=11)
        plt.grid(True)
        plt.show()  # display

    def plot_W_interface(time, val, el_list):
        plt.subplots_adjust(right=0.75)
        for i in range(len(val)):
            plt.plot(time, val[i], '-o', label=list_of_stad[el_list[i]], linewidth=2, markersize=3.5)
        plt.title("Кривые изменения скоростей стадий")
        legend_properties = {'weight': 'bold'}
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), labelcolor='black', fontsize='12',
                   prop=legend_properties)
        plt.ylabel("V, моль/л*сек")
        plt.xlabel("τ, условные минуты")
        plt.locator_params(axis='x', nbins=11)
        plt.grid(True)
        plt.show()

    def progress_start():
        global progress_window
        global progress_bar
        progress_window = Tk()
        progress_window.title("Progress Bar")
        progress_window.geometry("200x100")

        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(pady=20)
        progress_bar.start()
        progress_window.mainloop()

    def progress_stop():
        progress_bar.stop()
        progress_window.destroy()

    def change_rk45():
        # Создание GUI-интерфейса
        root_rk45 = Tk()
        root_rk45.geometry("1024x720")  # устанавливаем размеры окна
        root_rk45.title("Вывод рассчитанных графиков по методу Рунге-Кутты 4-го порядка")

        frame1_rk45 = tkinter.Frame(root_rk45, width=200, height=400)
        frame2_rk45 = tkinter.Frame(root_rk45, width=200, height=400)
        frame3_rk45 = tkinter.Frame(root_rk45, width=200, height=400)

        # Устанавливаем расположение рамок на окне
        frame1_rk45.pack(side=tkinter.LEFT)
        frame1_rk45.config(padx=20, pady=-20)
        frame2_rk45.pack(side=tkinter.RIGHT)
        frame2_rk45.config(padx=20, pady=-20)
        frame3_rk45.pack(side=tkinter.BOTTOM)
        frame3_rk45.config(pady=40)
        # Создание элементов интерфейса
        scrollbar1 = Scrollbar(frame1_rk45)
        scrollbar1.pack(side=TOP, fill=Y)

        scrollbar2 = Scrollbar(frame2_rk45)
        scrollbar2.pack(side=TOP, fill=Y)
        # расположение виджетов внутри контейнера tkinter
        label_concentration = Label(frame1_rk45, text="")
        label_concentration.config(text="Выберите компоненты для вывода \n концентрационных зависимостей",
                                        font=("Helvetica", 16))
        label_concentration.pack()

        listbox_concentration = Listbox(frame1_rk45, selectmode=MULTIPLE, yscrollcommand=scrollbar1.set)
        listbox_concentration.config(font=("Helvetica", 20), width=25, height=12)
        listbox_concentration.pack()
        #
        label_stad = Label(frame2_rk45, text="")
        label_stad.config(text="Выберите стадии для вывода \n изменения скоростей", font=("Helvetica", 16))
        label_stad.pack()

        listbox_stad = Listbox(frame2_rk45, selectmode=MULTIPLE, yscrollcommand=scrollbar2.set)
        listbox_stad.config(font=("Helvetica", 20), width=25, height=12)
        listbox_stad.pack()

        # Метод Рунге Кутты
        label_RK45 = Label(frame3_rk45, text="")
        label_RK45.config(text="Метод Рунге-Кутты 4 - го порядка", font=("Helvetica", 16))
        label_RK45.pack()

        button_RK45_rk45 = Button(frame3_rk45, text="Построить кривые изменения концентраций", command=button_click_RK45,
                                  width=45)
        button_RK45_rk45.config(font=("Helvetica", 16))
        button_RK45_rk45.pack()

        scrollbar1.config(command=listbox_concentration.yview)  # прокрутка по вертикали

        button_T_rk45 = Button(frame3_rk45, text="Построить кривую изменения температуры", command=button_click_RK45_T,
                               width=45)
        button_T_rk45.config(font=("Helvetica", 16))
        button_T_rk45.pack()

        button_Q_rk45 = Button(frame3_rk45, text="Построить кривую изменения объема", command=button_click_RK45_Q,
                               width=45)
        button_Q_rk45.config(font=("Helvetica", 16))
        button_Q_rk45.pack()

        button_W_rk45 = Button(frame3_rk45, text="Построить кривые изменения скоростей стадий",
                               command=button_click_RK45_W, width=45)
        button_W_rk45.config(font=("Helvetica", 16))
        button_W_rk45.pack()

        scrollbar2.config(command=listbox_stad.yview)  # прокрутка по вертикали

        # Заполнение списка векторов времени и значений (пример)
        times_Gira = wt
        values_Gira = wy
        # Скорости стадий
        q_all_gira = values_Gira[-1]
        zam_gira = values_Gira[0:len(values_Gira) - 1]

        w_gira = []
        with open(path_sdy + "W_izoterma.txt") as f:
            for line in f:
                w_gira.append(line[:-1])

        product_gira = w_gira[-1].split()
        w_gira = w_gira[0:len(w_gira) - 1]

        k_gira = []
        with open(path_sdy + "K_izoterma.txt") as f_kk:
            for line_k in f_kk:
                k_gira.append(float(line_k))

        for m in range(len(w_gira)):
            for n in range(len(product_gira)):
                w_gira[m] = w_gira[m].replace(product_gira[n] + '/', 'zamena[' + str(n) + ']/')
            for v in range(len(k_gira)):
                w_gira[m] = w_gira[m].replace('k' + str(v + 1) + '*', str(k_gira[v]) + '*')
            for v in range(len(k_gira)):
                w_gira[m] = w_gira[m].replace('Q', 'q')

        # print(w_gira, len(w_gira))

        return_w_all_gira = []
        for i in range(len(q_all_gira)):
            q = q_all_gira[i]
            return_w_gira = []
            zamena = zam_gira[:, i]
            for j in range(len(w_gira)):
                return_w_gira.append(eval(w_gira[j]))
            return_w_all_gira.append(return_w_gira)

        # print(return_w_all_gira)
        return_w_all_gira = np.array(return_w_all_gira).T
        # print(return_w_all_gira)

        list_of_stad = []
        for stad in range(len(return_w_all_gira)):
            list_of_stad.append('Стадия ' + str(stad + 1))

        # Добавление значений в список w
        for i in range(len(list_of_stad)):
            listbox_stad.insert(END, list_of_stad[i])

        # Добавление значений в список concentration
        for i in range(len(values_Gira) - 2):
            listbox_concentration.insert(END, him_el_list[i])

        times_RK45 = wt2
        values_RK45 = wy2

        # Скорости стадий
        q_all_rk45 = values_RK45[-1]
        zam_rk45 = values_RK45[0:len(values_RK45) - 1]

        w_rk45 = []
        with open(path_sdy + "W_izoterma.txt") as f:
            for line in f:
                w_rk45.append(line[:-1])

        product_rk45 = w_rk45[-1].split()
        w_rk45 = w_rk45[0:len(w_rk45) - 1]

        k_rk45 = []
        with open(path_sdy + "K_izoterma.txt") as f_kk:
            for line_k in f_kk:
                k_rk45.append(float(line_k))

        for m in range(len(w_rk45)):
            for n in range(len(product_rk45)):
                w_rk45[m] = w_rk45[m].replace(product_rk45[n] + '/', 'zamena[' + str(n) + ']/')
            for v in range(len(k_rk45)):
                w_rk45[m] = w_rk45[m].replace('k' + str(v + 1) + '*', str(k_rk45[v]) + '*')
            for v in range(len(k_rk45)):
                w_rk45[m] = w_rk45[m].replace('Q', 'q')

        # print(w_rk45, len(w_rk45))

        return_w_all_rk45 = []
        for i in range(len(q_all_rk45)):
            q = q_all_rk45[i]
            return_w_rk45 = []
            zamena = zam_rk45[:, i]
            for j in range(len(w_rk45)):
                return_w_rk45.append(eval(w_rk45[j]))
            return_w_all_rk45.append(return_w_rk45)

        # print(return_w_all_rk45)
        return_w_all_rk45 = np.array(return_w_all_rk45).T
        # print(return_w_all_rk45)

        list_of_stad = []
        for stad in range(len(return_w_all_rk45)):
            list_of_stad.append('Стадия ' + str(stad + 1))

        root_rk45.mainloop()

    progress_thread1 = Thread(target=progress_start)
    progress_thread1.start()

    matplotlib.rc('font', family='Times New Roman', size=14, weight='bold')

    C = []
    # with open("C0.txt") as f:
    with open(file_C0) as f:
        for line_C in f:
            C.append(float(line_C))

    Q = sum(C)
    C.append(Q)

    t = np.linspace(0, 60, 61)  # vector of time
    # t1 = np.linspace(0, 9.6, 10)  # vector of time 1
    # t2 = np.linspace(9.6, 32.3, 10)  # vector of time 2
    # t3 = np.linspace(32.3, 60, 10)  # vector of time 3
    # tt = [t1, t2, t3]
    global him_el_list
    him_el_list = ['бутилбензол', 'водород', 'бутилциклогексан', 'бензол', 'бутан', 'нафталин', 'тетралин', 'декалин',
                   'бифенил', 'циклогексилбензол', 'бициклогексил', 'циклогексан', 'метилиндан',
                   '1-метилоктагидро-1-инден', 'метилциклопентан', '3-метилпентан', 'гексан']

    # Метод Гира
    # 1
    f_bdf = lambda t, C0: np.array(f_rkt_gira(t, C0))
    start3 = time.time()
    w3 = solve_ivp(f_bdf, (t[0], t[-1]), C, method='BDF', max_step=10, t_eval=t)
    end3 = time.time()
    # print("The time of bdf(gira) :", (end3 - start3), "second")
    # print('Значения времени t по методу bdf')
    # print(w3.t, '\n')
    # print('Значения функции по методу bdf')
    # print(w3.y, '\n')

    ##################
    global wy, wt
    wy = w3.y
    wt = w3.t
    ##################

    # Метод Рунге-Кутты 4-го порядка
    # 1ф
    f_rk45 = lambda t, C0: np.array(f_rkt_gira(t, C0))
    start2 = time.time()
    w2 = solve_ivp(f_rk45, (t[0], t[-1]), C, method='RK45', max_step=10, t_eval=t)
    end2 = time.time()
    # print("The time of rk45 :", (end2 - start2), "second")
    # print('Значения времени t по методу rk45')
    # print(w2.t, '\n')
    # print('Значения функции по методу rk45')
    # print(w2.y, '\n')

    ##################
    global wy2, wt2
    wy2 = w2.y
    wt2 = w2.t
    ##################

    # Создание GUI-интерфейса
    root = Tk()
    root.geometry("1024x720")  # устанавливаем размеры окна
    root.title("Вывод рассчитанных графиков по методу Гира")

    button_change_rk45 = Button(root, text="Изменить метод расчета на \n Рунге-Кутты 4-го порядка",
                                command=change_rk45, width=45)
    button_change_rk45.config(font=("Helvetica", 16))
    button_change_rk45.pack()

    frame1 = tkinter.Frame(root, width=200, height=400)
    frame2 = tkinter.Frame(root, width=200, height=400)
    frame3 = tkinter.Frame(root, width=200, height=400)

    # Устанавливаем расположение рамок на окне
    frame1.pack(side=tkinter.LEFT)
    frame1.config(padx=20, pady=-20)
    frame2.pack(side=tkinter.RIGHT)
    frame2.config(padx=20, pady=-20)
    frame3.pack(side=tkinter.BOTTOM)
    frame1.config(pady=40)
    # Создание элементов интерфейса
    scrollbar1 = Scrollbar(frame1)
    scrollbar1.pack(side=TOP, fill=Y)

    scrollbar2 = Scrollbar(frame2)
    scrollbar2.pack(side=TOP, fill=Y)
    # расположение виджетов внутри контейнера tkinter
    label_concentration = Label(frame1, text="")
    label_concentration.config(text="Выберите компоненты для вывода \n концентрационных зависимостей",
                               font=("Helvetica", 16))
    label_concentration.pack()

    listbox_concentration = Listbox(frame1, selectmode=MULTIPLE, yscrollcommand=scrollbar1.set)
    listbox_concentration.config(font=("Helvetica", 20), width=25, height=12)
    listbox_concentration.pack()
    #
    label_stad = Label(frame2, text="")
    label_stad.config(text="Выберите стадии для вывода \n изменения скоростей", font=("Helvetica", 16))
    label_stad.pack()

    listbox_stad = Listbox(frame2, selectmode=MULTIPLE, yscrollcommand=scrollbar2.set)
    listbox_stad.config(font=("Helvetica", 20), width=25, height=12)
    listbox_stad.pack()
    # Метод Гира
    label_Gira = Label(frame3, text="")
    label_Gira.config(text="Метод Гира", font=("Helvetica", 16))
    label_Gira.pack()

    button_Gira = Button(frame3, text="Построить кривые изменения концентраций", command=button_click_Gira, width=45)
    button_Gira.config(font=("Helvetica", 16))
    button_Gira.pack()

    button_T = Button(frame3, text="Построить кривую изменения температуры", command=button_click_Gira_T, width=45)
    button_T.config(font=("Helvetica", 16))
    button_T.pack()

    button_Q = Button(frame3, text="Построить кривую изменения объема", command=button_click_Gira_Q, width=45)
    button_Q.config(font=("Helvetica", 16))
    button_Q.pack()

    button_W = Button(frame3, text="Построить кривые изменения скоростей стадий", command=button_click_Gira_W, width=45)
    button_W.config(font=("Helvetica", 16))
    button_W.pack()

    scrollbar1.config(command=listbox_concentration.yview)  # прокрутка по вертикали
    scrollbar2.config(command=listbox_stad.yview)  # прокрутка по вертикали

    k_k()

    # Заполнение списка векторов времени и значений (пример)
    times_Gira = wt
    values_Gira = wy
    # Скорости стадий
    q_all_gira = values_Gira[-1]
    zam_gira = values_Gira[0:len(values_Gira) - 1]

    w_gira = []
    with open(path_sdy + "W_izoterma.txt") as f:
        for line in f:
            w_gira.append(line[:-1])

    product_gira = w_gira[-1].split()
    w_gira = w_gira[0:len(w_gira) - 1]

    k_gira = []
    with open(path_sdy + "K_izoterma.txt") as f_kk:
        for line_k in f_kk:
            k_gira.append(float(line_k))

    for m in range(len(w_gira)):
        for n in range(len(product_gira)):
            w_gira[m] = w_gira[m].replace(product_gira[n] + '/', 'zamena[' + str(n) + ']/')
        for v in range(len(k_gira)):
            w_gira[m] = w_gira[m].replace('k' + str(v + 1) + '*', str(k_gira[v]) + '*')
        for v in range(len(k_gira)):
            w_gira[m] = w_gira[m].replace('Q', 'q')

    # print(w_gira, len(w_gira))

    return_w_all_gira = []
    for i in range(len(q_all_gira)):
        q = q_all_gira[i]
        return_w_gira = []
        zamena = zam_gira[:, i]
        for j in range(len(w_gira)):
            return_w_gira.append(eval(w_gira[j]))
        return_w_all_gira.append(return_w_gira)

    # print(return_w_all_gira)
    return_w_all_gira = np.array(return_w_all_gira).T
    # print(return_w_all_gira)

    list_of_stad = []
    for stad in range(len(return_w_all_gira)):
        list_of_stad.append('Стадия ' + str(stad + 1))

    # Добавление значений в список w
    for i in range(len(list_of_stad)):
        listbox_stad.insert(END, list_of_stad[i])

    # Добавление значений в список concentration
    for i in range(len(values_Gira) - 2):
        listbox_concentration.insert(END, him_el_list[i])

    times_RK45 = wt2
    values_RK45 = wy2

    # Скорости стадий
    q_all_rk45 = values_RK45[-1]
    zam_rk45 = values_RK45[0:len(values_RK45) - 1]

    w_rk45 = []
    with open(path_sdy + "W_izoterma.txt") as f:
        for line in f:
            w_rk45.append(line[:-1])

    product_rk45 = w_rk45[-1].split()
    w_rk45 = w_rk45[0:len(w_rk45) - 1]

    k_rk45 = []
    with open(path_sdy + "K_izoterma.txt") as f_kk:
        for line_k in f_kk:
            k_rk45.append(float(line_k))

    for m in range(len(w_rk45)):
        for n in range(len(product_rk45)):
            w_rk45[m] = w_rk45[m].replace(product_rk45[n] + '/', 'zamena[' + str(n) + ']/')
        for v in range(len(k_rk45)):
            w_rk45[m] = w_rk45[m].replace('k' + str(v + 1) + '*', str(k_rk45[v]) + '*')
        for v in range(len(k_rk45)):
            w_rk45[m] = w_rk45[m].replace('Q', 'q')

    # print(w_rk45, len(w_rk45))

    return_w_all_rk45 = []
    for i in range(len(q_all_rk45)):
        q = q_all_rk45[i]
        return_w_rk45 = []
        zamena = zam_rk45[:, i]
        for j in range(len(w_rk45)):
            return_w_rk45.append(eval(w_rk45[j]))
        return_w_all_rk45.append(return_w_rk45)

    # print(return_w_all_rk45)
    return_w_all_rk45 = np.array(return_w_all_rk45).T
    # print(return_w_all_rk45)

    list_of_stad = []
    for stad in range(len(return_w_all_rk45)):
        list_of_stad.append('Стадия ' + str(stad + 1))

    # Запуск интерфейса
    root.mainloop()
