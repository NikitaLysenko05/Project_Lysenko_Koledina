import tkinter as tk


class Interface1:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.root.title("1")

        self.button = tk.Button(self.frame, text="Go to Interface 2", command=self.goto_interface2)
        self.button.pack()

    def goto_interface2(self):
        self.frame.destroy()  # Удаление текущего интерфейса
        interface2 = Interface2(self.root)


class Interface2:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Interface 2")
        self.label.pack()

        self.button1 = tk.Button(self.frame, text="Go to Interface 1", command=self.goto_interface1)
        self.button1.pack()

        self.button2 = tk.Button(self.frame, text="Go to Interface 3", command=self.goto_interface3)
        self.button2.pack()

    def goto_interface1(self):
        self.frame.destroy()  # Удаление текущего интерфейса
        interface1 = Interface1(self.root)

    def goto_interface3(self):
        self.frame.destroy()  # Удаление текущего интерфейса
        interface3 = Interface3(self.root)


class Interface3:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Interface 3")
        self.label.pack()

        self.button = tk.Button(self.frame, text="Go to Interface 2", command=self.goto_interface2)
        self.button.pack()

    def goto_interface2(self):
        self.frame.destroy()  # Удаление текущего интерфейса
        interface2 = Interface2(self.root)


root = tk.Tk()
root.geometry("1024x720")
interface1 = Interface1(root)
root.mainloop()
