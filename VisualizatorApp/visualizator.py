from __future__ import print_function
import random
from queue import Queue
import tkinter as tk
from PIL import Image, ImageTk
import sys
from GeneratorApp.generator import Generator


# Окно вывода изображения на экран
class ExampleApp(tk.Tk):

    # Отступ налево
    def _draw_image_left(self, event):
        if self.regime == 1:
            if self.counter_x > 0:
                self.counter_x -= 1
            self._draw_image()

    # Отступ вправо
    def _draw_image_right(self, event):
        if self.regime == 1:
            self.counter_x += 1
            self._draw_image()

    # Отступ наверх
    def _draw_image_up(self, event):
        if self.regime == 1:
            if self.counter_y > 0:
                self.counter_y -= 1
            self._draw_image()

    # Отступ вниз
    def _draw_image_down(self, event):
        if self.regime == 1:
            self.counter_y += 1
            self._draw_image()

    # Инициализация окна вывода
    def __init__(self, master):

        # master = looped root, к которому мы "привязались"

        # Указание наименований текстур, импортируемых в вывод *позиция имеет значение!!!*
        self.names = ['../ResourcesDirectory/Water_deep.png', '../ResourcesDirectory/Water_not_deep.png',
                      '../ResourcesDirectory/Plains.png',
                      '../ResourcesDirectory/Forests.png', '../ResourcesDirectory/Mountains.png',
                      '../ResourcesDirectory/Snowy_mountains.png']
        self.master = master

        self.counter_x = self.counter_y = 0

        self.regime = 0

        self.tk_im = []
        self.items = []
        self.images = []
        self.generator = Generator

        # Привязка нажатий на кнопки к соответствующим событиям

        self.master.bind("<Up>", self._draw_image_up)
        self.master.bind("<Down>", self._draw_image_down)
        self.master.bind("<Left>", self._draw_image_left)
        self.master.bind("<Right>", self._draw_image_right)

        self.frame = tk.Frame(self.master)
        self.frame.rowconfigure(1, weight=1)
        self.framework1 = tk.Frame(self.frame)

        self.sizemap_x_label = tk.Label(self.framework1, text="Введите длину карты: ")
        self.sizemap_y_label = tk.Label(self.framework1, text="Введите ширину карты: ")
        self.number_of_continents_label = tk.Label(self.framework1, text="Введите количество континентов: ")
        self.filename_label = tk.Label(self.framework1, text="Введите имя файла для записи карты: ")

        self.sizemap_x_label.grid(row=0, column=0, sticky="w")
        self.sizemap_y_label.grid(row=1, column=0, sticky="w")
        self.number_of_continents_label.grid(row=2, column=0, sticky="w")
        self.filename_label.grid(row=3, column=0, sticky="w")

        self.sizemap_x = tk.StringVar()
        self.sizemap_y = tk.StringVar()
        self.number_of_continents = tk.StringVar()
        self.filename = tk.StringVar()

        self.sizemap_x_entry = tk.Entry(self.framework1, textvariable=self.sizemap_x)
        self.sizemap_y_entry = tk.Entry(self.framework1, textvariable=self.sizemap_y)
        self.number_of_continents_entry = tk.Entry(self.framework1, textvariable=self.number_of_continents)
        self.filename_entry = tk.Entry(self.framework1, textvariable=self.filename)

        self.sizemap_x_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.sizemap_y_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.number_of_continents_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.filename_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.framework1.grid(row=0, column=0, sticky="n")

        self.framework2 = tk.Frame(self.frame)
        self.framework2.rowconfigure(0, weight=1)
        self.framework2.columnconfigure(0, weight=1)

        self.message_button = tk.Button(self.framework2, text="Сгенерировать Карту", bg="green")
        self.message_button.grid(row=0, column=0, sticky="nesw")
        self.message_button.bind("<Button-1>", self._map_generate)

        self.smallmap = Image.open("../ResultsDirectory/example.png")
        self.smallmap = self.smallmap.resize((350, 350), Image.Resampling.LANCZOS)
        self.smallmap = ImageTk.PhotoImage(self.smallmap)

        self.minimap = tk.Label(self.framework2, image=self.smallmap)
        self.minimap.grid(row=1, column=0, sticky="nw")

        self.framework2.grid(row=1, column=0, sticky="nesw")

        self.frame.grid(row=0, column=0, sticky="nesw")

        self.frame1 = tk.Frame(self.master)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.rowconfigure(0, weight=1)

        # Указание размеров canvas
        self.canvas = tk.Canvas(self.frame1, cursor="cross")
        self.canvas.grid(row=0, column=0, sticky="nesw")

        self.frame1.grid(row=0, column=1, sticky="nesw")

        # Создание массива текстур, для ускорения работы вывода изображений
        for name in self.names:
            self.im = Image.open(name)
            self.tk_im.append(ImageTk.PhotoImage(self.im))
            self.images.append(self.im)

    def _map_generate(self, event):

        self.regime = 0
        self.canvas.delete("all")

        try:
            if int(self.sizemap_x.get()) >= 7 and int(self.sizemap_y.get()) >= 7 and int(
                    self.number_of_continents.get()) >= 0 and not str(self.filename.get()) == "Example":
                self.canvas.create_text(30, 30, anchor="nw", text="Generating is on, please, wait",
                                        font="Times 20 italic bold", fill="darkblue")
                self.canvas.update()

                self.generator = Generator(int(self.sizemap_x.get()), int(self.sizemap_y.get()),
                                           int(self.number_of_continents.get()), str(self.filename.get()))

                self.regime = 1

                # Первичная отрисовка
                self._draw_image()

                self.smallmap = ImageTk.PhotoImage(
                    self.generator.image_out.resize((350, min(900, round(350 * (len(self.generator.array[0]) / len(self.generator.array))))),
                                          Image.Resampling.LANCZOS))
                self.minimap.configure(image=self.smallmap)
                self.minimap.image = self.smallmap
            else:
                self.canvas.create_text(30, 30, anchor="nw", text="The map is too small, please, try other size",
                                        font="Times 20 italic bold", fill="red")
                self.canvas.update()
        except:
            self.canvas.create_text(30, 30, anchor="nw", text="Invalid input", font="Times 20 italic bold", fill="red")
            self.canvas.update()

    # Вывод картинок на канвас
    def _draw_image(self):

        # Очистка старого вывода
        self.items.clear()
        self.canvas.delete("all")

        # Было подсчитано, что при расширении 1920х1080 на экран помещается прямоугольник размера 47х27 клеток
        SIZE_OF_SCREEN_X = 47
        SIZE_OF_SCREEN_Y = 27
        SIZE_OF_IMAGE = 41

        # Отрисовка подвинутого изображения
        for x_map in range(self.counter_x, min(len(self.generator.array), self.counter_x + SIZE_OF_SCREEN_X)):
            for y_map in range(self.counter_y, min(len(self.generator.array[0]), self.counter_y + SIZE_OF_SCREEN_Y)):
                self.items.append(self.canvas.create_image(SIZE_OF_IMAGE * (x_map - self.counter_x),
                                                           SIZE_OF_IMAGE * (y_map - self.counter_y), anchor="nw",
                                                           image=self.tk_im[self.generator.array[x_map][y_map]]))

if __name__ == '__main__':
    # Работаем с окном вывода программы
    root = tk.Tk()
    root.title("Генератор карт")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    app = ExampleApp(root)

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    root.mainloop()
