import tkinter as tk
from time import sleep


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


root = tk.Tk()


window_width = 1000
window_height = 300

# Получение размеров экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Вычисление координат для центрирования окна
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Установка размеров и позиции окна
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Создание текстового виджета
label1 = tk.Label(root, text="Моделирование кинетических закономерностей", font=("Arial", 33))
label1.pack()  # Размещение виджета в окне
label1.place(relx=0.5, rely=0.40, anchor="center")
label2 = tk.Label(root, text="химических процессов", font=("Arial", 33))
label2.pack()  # Размещение виджета в окне
label2.place(relx=0.5, rely=0.60, anchor="center")
fade_in(root)
fade_out(root)
