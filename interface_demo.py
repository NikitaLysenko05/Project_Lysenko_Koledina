import matplotlib.pyplot as plt
import tkinter
from tkinter import Tk, Listbox, Button, Scrollbar, MULTIPLE, END, RIGHT, Y, filedialog, messagebox, ttk
from tkinter import *
import numpy as np
import sdy_form
import sdy_form_izoterma
import os
import subprocess
import katal_riforming
import katal_pay
from time import sleep
import time
import threading
from threading import Thread

# библиотеки для интерфейса
from tkinter import Tk, Listbox, Button, Scrollbar, MULTIPLE, END, RIGHT, Y


def fade_in(window):
    alpha = 0.0
    while alpha < 1:
        window.attributes("-alpha", alpha)
        window.update()
        sleep(0.03)  # задержка для плавности эффекта
        alpha += 0.01


def fade_out(window):
    alpha = 1.0
    while alpha > 0:
        window.attributes("-alpha", alpha)
        window.update()
        sleep(0.03)  # задержка для плавности эффекта
        alpha -= 0.01
    window.destroy()


def open_interface_1_pay():
    # Функция, которая предоставляет выбор файла со стехиометрической матрицей в формате электронной таблицы
    def choose_file():
        global filename
        filename = filedialog.askopenfilename(title="Select a File")
        if filename != '':
            file_label.config(text="Файл успешно выбран:\n {}".format(filename))
            button_form_sdy.config(state=tkinter.NORMAL)

    # Функция для формирования СДУ
    def activate_function_choose_file():
        global path_sdy
        path_sdy = filename[0:filename.rfind('/') + 1]
        sdy_form_izoterma.stex_matrix_to_sdy(filename, path_sdy)
        message_label.config(text="Система СДУ создана в файле sdy_izoterma.txt по пути:\n {}".
                             format(path_sdy + 'sdy_izoterma.txt'))
        button_graphics.config(state=tkinter.NORMAL)

    # Создание GUI-интерфейса
    global interface_1_pay
    interface_1_pay = Tk()
    interface_1_pay.title("Формирование СДУ")
    interface_1_pay.geometry("1024x720")  # устанавливаем размеры окна
    # interface_main.destroy()
    fr1 = Frame()
    fr2 = Frame()

    # Создаем и размещаем кнопки
    # button_previous = Button(interface_1, text="Предыдущее окно", command=previous_window)
    # button_previous.pack()
    # Кнопка выбора файла
    button_select_file = Button(interface_1_pay, text="Выбор файла со стехиометрической матрицей", command=choose_file,
                                width=40)
    button_select_file.config(font=("Helvetica", 20))
    button_select_file.pack(side=TOP)
    # Кнопка Формирования СДУ
    button_form_sdy = Button(interface_1_pay, text="Сформировать математическую модель",
                             command=activate_function_choose_file,
                             state=tkinter.DISABLED, width=40)
    button_form_sdy.config(font=("Helvetica", 20))
    button_form_sdy.pack(side=TOP)
    # Кнопка перехода на второй интерфейс
    button_graphics = Button(interface_1_pay, text="Перейти к построению кривых концентраций",
                             command=open_interface_2_pay, state=tkinter.DISABLED, width=40)
    button_graphics.config(font=("Helvetica", 20))
    button_graphics.pack(side=TOP)

    # Создаем и размещаем метки для отображения статуса и сообщений
    file_label = Label(interface_1_pay, text="")
    file_label.config(font=("Helvetica", 14))
    file_label.pack()

    message_label = Label(interface_1_pay, text="", compound="right")
    message_label.config(font=("Helvetica", 14))
    message_label.pack()

    # Запуск интерфейса
    interface_1_pay.mainloop()


def open_interface_2_pay():
    # Функция для выбора файла
    def choose_parametr_C0():
        global file_param_C0
        file_param_C0 = filedialog.askopenfilename(title="Select a File")
        if file_param_C0 != '':
            file_label_C0.config(text="Файл начальных концентраций успешно выбран:\n {}".format(file_param_C0))
            button_select_T0.config(state=tkinter.NORMAL)
            with open(file_param_C0, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def choose_parametr_T0():
        global file_param_T0
        file_param_T0 = filedialog.askopenfilename(title="Select a File")
        if file_param_T0 != '':
            file_label_T0.config(text="Файл начальной температуры успешно выбран:\n {}".format(file_param_T0))
            button_select_E.config(state=tkinter.NORMAL)
            with open(file_param_T0, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def choose_parametr_E():
        global file_param_E
        file_param_E = filedialog.askopenfilename(title="Select a File")
        if file_param_E != '':
            file_label_E.config(text="Файл начальных энергий активации успешно выбран:\n {}".format(file_param_E))
            button_select_k0.config(state=tkinter.NORMAL)
            with open(file_param_E, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def choose_parametr_k0():
        global file_param_k0
        file_param_k0 = filedialog.askopenfilename(title="Select a File")
        if file_param_k0 != '':
            file_label_k0.config(text="Файл начальных предэкспоненциальных множителей успешно выбран:\n {}".
                                 format(file_param_k0))
            button2.config(state=tkinter.NORMAL)
            with open(file_param_k0, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def clear_text():
        text_box.delete("1.0", tkinter.END)

    # Функция для запуска файла sdy.py
    def run_interface():
        katal_pay.interface_of_graphics(file_param_E, file_param_k0, file_param_T0, file_param_C0, path_sdy)

    global interface_2_pay
    interface_2_pay = Tk()
    interface_2_pay.title("Выбор файла для расчёта")
    interface_2_pay.geometry("1024x720")
    # interface_1_pay.destroy()

    # Создаем две рамки для разделения окна
    frame1 = tkinter.Frame(interface_2_pay, width=200, height=400)
    frame2 = tkinter.Frame(interface_2_pay, width=200, height=400)

    # Устанавливаем расположение рамок на окне
    frame1.pack(side=tkinter.LEFT)
    frame2.pack(side=tkinter.RIGHT)

    # Кнопки и сообщения выбора файлов
    button_select_C0 = Button(frame1, text="Начальные значения концентраций компонент",
                              command=choose_parametr_C0, width=40)
    button_select_C0.config(font=("Helvetica", 18))
    button_select_C0.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_C0 = Label(frame1, text="")
    file_label_C0.config(font=("Helvetica", 12))
    file_label_C0.pack()

    button_select_T0 = Button(frame1, text="Входные температуры смеси в реакторах",
                              command=choose_parametr_T0, state=tkinter.DISABLED, width=40)
    button_select_T0.config(font=("Helvetica", 18))
    button_select_T0.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_T0 = Label(frame1, text="")
    file_label_T0.config(font=("Helvetica", 12))
    file_label_T0.pack()

    button_select_E = Button(frame1, text="Энергии активаций стадий",
                             command=choose_parametr_E, state=tkinter.DISABLED, width=40)
    button_select_E.config(font=("Helvetica", 18))
    button_select_E.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_E = Label(frame1, text="")
    file_label_E.config(font=("Helvetica", 12))
    file_label_E.pack()

    button_select_k0 = Button(frame1, text="Предэкспоненциальные множители стадий",
                              command=choose_parametr_k0, state=tkinter.DISABLED, width=40)
    button_select_k0.config(font=("Helvetica", 18))
    button_select_k0.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_k0 = Label(frame1, text="")
    file_label_k0.config(font=("Helvetica", 12))
    file_label_k0.pack()

    # Создание кнопки 2 в интерфейсе 2
    button2 = Button(frame1, text="Запуск расчета концентрационных профилей",
                     command=run_interface, state=tkinter.DISABLED, bg='darkolivegreen1', width=40)
    button2.config(font=("Helvetica", 18))
    button2.pack(anchor=tkinter.W, padx=20, pady=20)

    process_label = Label(frame1, text="")
    process_label.pack()
    process_label.config(text="После нажатия на кнопку, пожалуйста, дождитесь процесса вычисления.",
                         font=("Helvetica", 12))

    # Создаем окошко для отображения содержимого файла
    text_box = tkinter.Text(frame2)
    text_box.pack(anchor=tkinter.E, padx=20, pady=20)

    # Кнопка для очистки текстового поля
    clear_btn = Button(frame2, text="Очистить", command=clear_text)
    clear_btn.pack(anchor=tkinter.S, padx=20, pady=20)


def open_interface_1():
    # Функция, которая предоставляет выбор файла со стехиометрической матрицей в формате электронной таблицы
    def choose_file():
        global filename
        filename = filedialog.askopenfilename(title="Select a File")
        if filename != '':
            file_label.config(text="Файл успешно выбран:\n {}".format(filename))
            button_form_sdy.config(state=tkinter.NORMAL)

    # Функция для формирования СДУ
    def activate_function_choose_file():
        global path_sdy
        path_sdy = filename[0:filename.rfind('/') + 1]
        sdy_form.stex_matrix_to_sdy(filename, path_sdy)
        message_label.config(text="Система СДУ создана в файле sdy.txt по пути:\n {}".
                             format(path_sdy + 'sdy.txt'))
        button_graphics.config(state=tkinter.NORMAL)

    # Создание GUI-интерфейса
    global interface_1
    interface_1 = Tk()
    interface_1.title("Формирование СДУ")
    interface_1.geometry("1024x720")  # устанавливаем размеры окна
    # interface_main.destroy()
    fr1 = Frame()
    fr2 = Frame()

    # Создаем и размещаем кнопки
    # button_previous = Button(interface_1, text="Предыдущее окно", command=previous_window)
    # button_previous.pack()
    # Кнопка выбора файла
    button_select_file = Button(interface_1, text="Выбор файла со стехиометрической матрицей", command=choose_file,
                                width=40)
    button_select_file.config(font=("Helvetica", 20))
    button_select_file.pack(side=TOP)
    # Кнопка Формирования СДУ
    button_form_sdy = Button(interface_1, text="Сформировать математическую модель",
                             command=activate_function_choose_file,
                             state=tkinter.DISABLED, width=40)
    button_form_sdy.config(font=("Helvetica", 20))
    button_form_sdy.pack(side=TOP)
    # Кнопка перехода на второй интерфейс
    button_graphics = Button(interface_1, text="Перейти к построению кривых концентраций", command=open_interface_2,
                             state=tkinter.DISABLED, width=40)
    button_graphics.config(font=("Helvetica", 20))
    button_graphics.pack(side=TOP)

    # Создаем и размещаем метки для отображения статуса и сообщений
    file_label = Label(interface_1, text="")
    file_label.config(font=("Helvetica", 14))
    file_label.pack()

    message_label = Label(interface_1, text="", compound="right")
    message_label.config(font=("Helvetica", 14))
    message_label.pack()

    # Запуск интерфейса
    interface_1.mainloop()


# Обработчик события нажатия кнопки 1
def open_interface_2():
    # Функция для выбора файла
    def choose_parametr_C0():
        global file_param_C0
        file_param_C0 = filedialog.askopenfilename(title="Select a File")
        if file_param_C0 != '':
            file_label_C0.config(text="Файл начальных концентраций успешно выбран:\n {}".format(file_param_C0))
            button_select_T0.config(state=tkinter.NORMAL)
            with open(file_param_C0, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def choose_parametr_T0():
        global file_param_T0
        file_param_T0 = filedialog.askopenfilename(title="Select a File")
        if file_param_T0 != '':
            file_label_T0.config(text="Файл начальной температуры успешно выбран:\n {}".format(file_param_T0))
            button_select_E.config(state=tkinter.NORMAL)
            with open(file_param_T0, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def choose_parametr_E():
        global file_param_E
        file_param_E = filedialog.askopenfilename(title="Select a File")
        if file_param_E != '':
            file_label_E.config(text="Файл начальных энергий активации успешно выбран:\n {}".format(file_param_E))
            button_select_k0.config(state=tkinter.NORMAL)
            with open(file_param_E, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def choose_parametr_k0():
        global file_param_k0
        file_param_k0 = filedialog.askopenfilename(title="Select a File")
        if file_param_k0 != '':
            file_label_k0.config(text="Файл начальных предэкспоненциальных множителей успешно выбран:\n {}".
                                 format(file_param_k0))
            button2.config(state=tkinter.NORMAL)
            with open(file_param_k0, 'r') as file:
                file_content = file.read()
                text_box.delete("1.0", tkinter.END)
                text_box.insert(tkinter.END, file_content)

    def clear_text():
        text_box.delete("1.0", tkinter.END)

    # Функция для запуска файла sdy.py
    def run_interface():
        katal_riforming.interface_of_graphics(file_param_E, file_param_k0, file_param_T0, file_param_C0, path_sdy)
        # try:
        #     katal_riforming.interface_of_graphics(file_param_E, file_param_k0, file_param_T0, file_param_C0)
        # except:
        #     messagebox.showerror("Error", "Failed to run katal_riforming.py")

    # def command1():
    #     global progress_window, progress_bar
    #     progress_window = Tk()
    #     progress_window.title("Progress Bar")
    #     progress_window.geometry("200x100")
    #
    #     progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
    #     progress_bar.pack(pady=20)
    #
    #     progress_bar.start()
    #     progress_window.mainloop()
    #
    # def execute_commands():
    #     thread1 = threading.Thread(target=command1)
    #     thread2 = threading.Thread(target=run_interface)
    #     thread1.start()
    #     thread2.start()
    global interface_2
    interface_2 = Tk()
    interface_2.title("Выбор файла для расчёта")
    interface_2.geometry("1024x720")
    # interface_1.destroy()

    # Создаем две рамки для разделения окна
    frame1 = tkinter.Frame(interface_2, width=200, height=400)
    frame2 = tkinter.Frame(interface_2, width=200, height=400)

    # Устанавливаем расположение рамок на окне
    frame1.pack(side=tkinter.LEFT)
    frame2.pack(side=tkinter.RIGHT)

    # Кнопки и сообщения выбора файлов
    button_select_C0 = Button(frame1, text="Начальные значения концентраций компонент",
                              command=choose_parametr_C0, width=40)
    button_select_C0.config(font=("Helvetica", 18))
    button_select_C0.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_C0 = Label(frame1, text="")
    file_label_C0.config(font=("Helvetica", 12))
    file_label_C0.pack(anchor=tkinter.W)

    button_select_T0 = Button(frame1, text="Входные температуры смеси в реакторах",
                              command=choose_parametr_T0, state=tkinter.DISABLED, width=40)
    button_select_T0.config(font=("Helvetica", 18))
    button_select_T0.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_T0 = Label(frame1, text="")
    file_label_T0.config(font=("Helvetica", 12))
    file_label_T0.pack(anchor=tkinter.W)

    button_select_E = Button(frame1, text="Энергии активаций стадий",
                             command=choose_parametr_E, state=tkinter.DISABLED, width=40)
    button_select_E.config(font=("Helvetica", 18))
    button_select_E.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_E = Label(frame1, text="")
    file_label_E.config(font=("Helvetica", 12))
    file_label_E.pack(anchor=tkinter.W)

    button_select_k0 = Button(frame1, text="Предэкспоненциальные множители стадий",
                              command=choose_parametr_k0, state=tkinter.DISABLED, width=40)
    button_select_k0.config(font=("Helvetica", 18))
    button_select_k0.pack(anchor=tkinter.W, padx=20, pady=20)

    file_label_k0 = Label(frame1, text="")
    file_label_k0.config(font=("Helvetica", 12))
    file_label_k0.pack(anchor=tkinter.W)

    # Создание кнопки 2 в интерфейсе 2
    button2 = Button(frame1, text="Запуск расчета концентрационных профилей",
                     command=run_interface, state=tkinter.DISABLED, bg='darkolivegreen1', width=40)
    button2.config(font=("Helvetica", 18))
    button2.pack(anchor=tkinter.W, padx=20, pady=20)

    process_label = Label(frame1, text="")
    process_label.pack()
    process_label.config(text="После нажатия на кнопку, пожалуйста, дождитесь процесса вычисления.",
                         font=("Helvetica", 12))

    # Создаем окошко для отображения содержимого файла
    text_box = tkinter.Text(frame2)
    text_box.pack(anchor=tkinter.E, padx=20, pady=20)

    # Кнопка для очистки текстового поля
    clear_btn = Button(frame2, text="Очистить", command=clear_text)
    clear_btn.pack(anchor=tkinter.S, padx=20, pady=20)


# root = Tk()
# root.geometry("1024x720")  # устанавливаем размеры окна

root_vanish = Tk()


window_width = 1000
window_height = 300

# Получение размеров экрана
screen_width = root_vanish.winfo_screenwidth()
screen_height = root_vanish.winfo_screenheight()

# Вычисление координат для центрирования окна
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Установка размеров и позиции окна
root_vanish.geometry(f'{window_width}x{window_height}+{x}+{y}')
# Создание текстового виджета
label1_van = Label(root_vanish, text="Моделирование кинетических закономерностей \n химических процессов",
                   font=("Arial", 33))
label1_van.pack()  # Размещение виджета в окне
label1_van.place(relx=0.5, rely=0.5, anchor="center")
fade_in(root_vanish)
fade_out(root_vanish)

# Создание GUI-интерфейса
interface_main = Tk()
interface_main.title("Выбор реакции")
interface_main.geometry("1024x720")  # устанавливаем размеры окна

# Создаем и размещаем кнопки
# Кнопка выбора файла
button_katal_rif_oil = Button(interface_main, text="Каталитический риформинг бензина", width=40,
                              command=open_interface_1)
button_katal_rif_oil.config(font=("Helvetica", 20))
button_katal_rif_oil.pack()
# Кнопка Формирования СДУ
button_form_sdy = Button(interface_main, text="Каталитическое гидрирование полициклических \n"
                                              " ароматических углеводородов", width=40,
                         command=open_interface_1_pay)
button_form_sdy.config(font=("Helvetica", 20))
button_form_sdy.pack()
# Кнопка перехода на второй интерфейс
button_graphics = Button(interface_main, text="Другие реакции", width=40)
button_graphics.config(font=("Helvetica", 20))
button_graphics.pack()

# Запуск интерфейса
interface_main.mainloop()
