from __future__ import print_function
import random
from queue import Queue
import tkinter as tk
from PIL import Image, ImageTk
import sys


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
        self.names = ['Water_deep.png', 'Water_not_deep.png', 'Plains.png', 'Forests.png', 'Mountains.png',
                      'Snowy_mountains.png']
        self.master = master

        self.counter_x = self.counter_y = 0
        # Разброс скорости генераци
        self.t = 11
        # Размер Континента
        self.size_continent = 20

        self.regime = 0

        # Высоты биомов
        self.heights = [15, 59, 71, 96]
        self.array = []
        self.tk_im = []
        self.items = []
        self.images = []

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
        self.number_of_continents_label = tk.Label(self.framework1, text="Введите количество конинентов: ")
        self.filename_label = tk.Label(self.framework1, text="Введите имя файла, для записи карты: ")

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

        self.smallmap = Image.open("Example.png")
        self.smallmap = self.smallmap.resize((350, 350), Image.ANTIALIAS)
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

                self.array = map_generator(int(self.sizemap_x.get()), int(self.sizemap_y.get()),
                                           int(self.number_of_continents.get()), str(self.filename.get()), self.heights,
                                           self.t, self.size_continent)

                self.regime = 1

                # Первичная отрисовка
                self._draw_image()
                self.image_out = Image.new(self.im.mode, (len(self.array) * 41, len(self.array[0]) * 41))
                for x in range(len(self.array)):
                    for y in range(len(self.array[0])):
                        self.image_out.paste(self.images[self.array[x][y]], (x * 41, y * 41))
                self.image_out.save(str(self.filename.get()) + ".png")
                self.smallmap = ImageTk.PhotoImage(
                    self.image_out.resize((350, min(900, round(350 * (len(self.array[0]) / len(self.array))))),
                                          Image.ANTIALIAS))
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

        # Было подсчитано, что при расширении 1920х1080 на экран помещается прямогугольник размера 47х27 клеток
        SIZE_OF_SCREEN_X = 47
        SIZE_OF_SCREEN_Y = 27
        SIZE_OF_IMAGE = 41

        # Отрисовка подвинутого изображения
        for x_map in range(self.counter_x, min(len(self.array), self.counter_x + SIZE_OF_SCREEN_X)):
            for y_map in range(self.counter_y, min(len(self.array[0]), self.counter_y + SIZE_OF_SCREEN_Y)):
                self.items.append(self.canvas.create_image(SIZE_OF_IMAGE * (x_map - self.counter_x),
                                                           SIZE_OF_IMAGE * (y_map - self.counter_y), anchor="nw",
                                                           image=self.tk_im[self.array[x_map][y_map]]))


# -----------------------------------------------------------------------------Классы--------------------------------------------------------------------------

class square:
    def __init__(self):
        # Скорость "роста высоты" клетки
        self.speed = int()
        # Высота клетки в каком-то определённом чанке
        self.main = int()
        # Количество "посещений" клетки
        self.count = int()
        # Тип поверхнсти, которая будет располагаться на клетке
        self.id = int()
        # Итоговая (средняя) высота клетки по всем чанкам, с учётом близости от центров генераций
        self.heigth = int()
        # Лопнула ли ещё эта клетка при генерации конкретного чанка?
        self.turn = int()
        # "Вес", на который нужно делить self.heigth, для получения средней высоты
        self.delta = int()
        # Является ли генерируемый чанк - чанком суши?
        self.type = int()
        # Тип "биома", по которому бедет генерироваться чанк
        self.typeres = int()


class square_map:

    # Инициалиация карты клеток
    def __init__(self, length, heigth, sizemap_x, sizemap_y):
        self.stock = []

        # Указание размера первичной карты
        for i in range(length + 2):
            useless = [square() for i in range(heigth + 2)]
            self.stock.append(useless)
        self.under_development = Queue()
        self.turn_cleaning = []
        self.interpolated_map = []

        # Указание размера аппроксимированной карты
        for i in range(sizemap_x):
            useless = [int() for j in range(sizemap_y)]
            self.interpolated_map.append(useless)

    # Поиск соседей клетки с координатами x, y
    def neighbours(self, x, y, step_x=1, step_y=1):
        res = []
        # Если сосед по х слева находится не на "противоположной" стороне карты, то:
        if (x - 1) * step_x > 0:
            # Проверка на диагональных соседей слева
            if (y - 1) * step_y > 0:
                res.append(((x - 1) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append(((x - 1) * step_x, (y + 1) * step_y))
            # Добавляем соседа слева
            res.append(((x - 1) * step_x, y * step_y))
        # А иначе:
        else:
            # Добавляем соседа слева
            res.append((((len(self.stock) - 2) // step_x) * step_x, y * step_y))
            # Проверка на диагональных соседей слева
            if (y - 1) * step_y > 0:
                res.append((((len(self.stock) - 2) // step_x) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append((((len(self.stock) - 2) // step_x) * step_x, (y + 1) * step_y))

        # Если сосед по х справа находится не на "противоположной" стороне карты, то:
        if (x + 1) * step_x < len(self.stock):
            # Проверка на диагональных соседей справа
            if (y - 1) * step_y > 0:
                res.append(((x + 1) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append(((x + 1) * step_x, (y + 1) * step_y))
            # Добавляем соседа справа
            res.append(((x + 1) * step_x, y * step_y))
        # А иначе:
        else:
            # Добавляем соседа справа
            res.append((step_x, y * step_y))
            # Проверка на диагональных соседей справа
            if (y - 1) * step_y > 0:
                res.append((step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append((step_x, (y + 1) * step_y))

        # Если сверху есть сосед, то добавим его
        if (y - 1) * step_y > 0:
            res.append((x * step_x, (y - 1) * step_y))
        # Если снизу есть сосед, то добавим его
        if (y + 1) * step_y < len(self.stock[0]):
            res.append((x * step_x, (y + 1) * step_y))
        return res

    # "Лопание" клетки с координатами x, y
    def pop(self, x, y, mode=1, delta_x=1, delta_y=1):
        # Узнаём наших соседей
        mates = self.neighbours(x, y, delta_x, delta_y)
        # Увеличиваем кол-во их посещений на 1 у каждого
        for coords in mates:
            if self.stock[coords[0]][coords[1]].count < 3:
                self.stock[coords[0]][coords[1]].count += mode
        return mates

    # Очистка клеток от "мусора"
    def clear(self, step_x=1, step_y=1):
        for i in range(1, ((len(self.stock) - 1) // step_x) + 1):
            for j in range(1, ((len(self.stock[0]) - 1) // step_y) + 1):
                self.stock[step_x * i][step_y * j].type = 0
                self.stock[step_x * i][step_y * j].count = 0
                self.stock[step_x * i][step_y * j].turn = 0

    # Вывод образов континента в консоль
    def show_continent(self, step_x=1, step_y=1):
        for i in range(1, ((len(self.stock) - 1) // step_x) + 1):
            for j in range(1, ((len(self.stock[0]) - 1) // step_y) + 1):
                print(self.stock[step_x * i][step_y * j].typeres, end=' ')
            print()
        print()

    # Отправка скорости взрывающейся клетки её соседям
    def send_speed(self, _from, _to, t, ground_level, speed_cut):
        to = self.stock[_to[0]][_to[1]]
        father = self.stock[_from[0]][_from[1]]
        # Считаем знак нащей функии
        value = sign(to.speed + father.speed + custom_rand(t) + (ground_level - father.main))

        # Изменяем скорость роста высот в клетке-соседе по формуле ниже (игнорируя знак)
        to.speed = ((value * (
                    to.speed + father.speed + custom_rand(t) + (ground_level - father.main))) % speed_cut) * value

    # Аппроксимация высот карты
    def approximation(self):

        # Указываем размеры апрроксимируемых областей
        interpolation_x = len(self.stock) // (2 * len(self.interpolated_map))
        interpolation_y = len(self.stock[0]) // (2 * len(self.interpolated_map[0]))

        # Заполняем аппроксимированную карту высот
        for map_x in range(1, len(self.interpolated_map) + 1):
            for map_y in range(1, len(self.interpolated_map[0]) + 1):

                # Создаём счётчики клеток, встречающихся в каждой "области"
                counters = [0] * 6
                for x in range((2 * map_x - 2) * interpolation_x, (2 * map_x) * interpolation_x):
                    for y in range((2 * map_y - 2) * interpolation_y, (2 * map_y) * interpolation_y):
                        # Считаем, сколько клеток каждого типа встретилось на каждой из областей
                        counters[self.stock[x][y].id] += 1
                # Пишем id самой часто встречающейся клетки в соотвествующую клетку аппроксимированной карты высот
                self.interpolated_map[map_x - 1][map_y - 1] = counters.index(max(counters))

    # "Усредняем" высоту каждой из клеток
    def heigths_approximation(self):

        borders = [40, 48, 65, 77, 94]

        # Проходимся по всем клеткам карты
        for array in self.stock:
            for item in array:
                # Усредняем высоту по всем принятым значениям
                if item.delta > 0: item.heigth = item.heigth // item.delta

                counter = 0
                ckecker = True

                # В зав-ти от высоты клетки, присваиваем ей свой "биом"
                while counter < len(borders) and ckecker:
                    if item.heigth <= borders[counter]:
                        item.id = counter
                        ckecker = False
                    else:
                        counter += 1
                if counter == 5:
                    item.id = counter

    # Убираем промежуточные значения из карты высот
    def clean_buffer(self):
        for guy in self.turn_cleaning:
            guy.turn = 0
            guy.count = 0
            guy.main = 0
            guy.speed = 0
        while not self.under_development.empty():
            self.under_development.get()
        self.turn_cleaning.clear()

    # ----------------------------------------Смысловые функции--------------------------------------------

    def initialize_center(self, x, y):
        self.stock[x][y].count = 3
        self.stock[x][y].type = 1
        self.stock[x][y].typeres = random.randint(1, 2)
        self.stock[x][y].turn = 1

    def continent_tipisation(self, x, y):
        self.stock[x][y].type = 1
        if self.stock[x][y].typeres == 0:
            self.stock[x][y].typeres = random.randint(1, 2)
        else:
            self.stock[x][y].typeres = 3

    def popping_initialisation(self, coords, radius, counter):
        cur_stock = self.stock[coords[0]][coords[1]]
        cur_stock.main = (cur_stock.main + cur_stock.speed) // cur_stock.count
        cur_stock.speed = cur_stock.speed // cur_stock.count
        cur_stock.delta += (radius - counter)
        cur_stock.heigth += cur_stock.main * (radius - counter)

    def biome_initialisation(self, center_x, center_y, normal, radius, t):
        center = self.stock[center_x][center_y]
        center.main = normal[center.typeres]
        center.turn = 1

        # Изменение итоговой высоты на значение, пропорциональное близости к центру генерации
        center.heigth = center.main * radius
        center.delta += radius
        mates = self.pop(center_x, center_y, 3)
        for mate in mates:
            square_mate = self.stock[mate[0]][mate[1]]
            self.send_speed((center_x, center_y), mate, t, normal[center.typeres], 20)
            square_mate.main = center.main * 3
            square_mate.speed *= 3
            square_mate.turn = 1
            self.under_development.put(mate)
            self.turn_cleaning.append(square_mate)

        center.count = 4
        center.main = 0
        center.speed = 0

    def add_to_development(self, mate):
        self.stock[mate[0]][mate[1]].turn = 1
        self.under_development.put(mate)
        self.turn_cleaning.append(self.stock[mate[0]][mate[1]])

    def speed_parameters_choosing(self, center_x, center_y, coords, mate, t, normal):
        center = self.stock[center_x][center_y]
        father = self.stock[coords[0]][coords[1]]

        # 0 - Вода
        # 1 - Равнина
        # 2 - Лес
        # 3 - Горы

        borders = [[40, 48],
                   [49, 66],
                   [54, 86],
                   []]
        middle_heights = [[normal[0], 45, normal[1]],
                          [43, normal[1], normal[2]],
                          [45, normal[2], normal[3]],
                          [normal[3]]]

        speed_limit_borders = [[20, 20, 1000],
                               [20, 20, 20],
                               [20, 20, 20],
                               [30]]

        counter = 0
        ckecker = True

        # В зав-ти от высоты клетки, присваиваем ей свой "биом"
        while counter < len(borders[center.typeres]) and ckecker:
            if father.main < borders[center.typeres][counter]:
                self.send_speed(coords, mate, t, middle_heights[center.typeres][counter],
                                speed_limit_borders[center.typeres][counter])
                ckecker = False
            else:
                counter += 1
        if ckecker:
            self.send_speed(coords, mate, t, middle_heights[center.typeres][counter],
                            speed_limit_borders[center.typeres][counter])


# --------------------------------------------------------------------------------Функции----------------------------------------------------------------------

def custom_rand(t):
    return random.randint(0, t - 1) - random.randint(0, t - 1)


def sign(num):
    return -1 if num < 0 else 1


# Генерация одного континента
def continent_generate(map, center_x, center_y, size_of_chunks_x, size_of_chunks_y, continent_size):
    # Инициализация очереди обработки
    under_development = Queue()
    under_development.put((size_of_chunks_x * center_x, size_of_chunks_y * center_y))

    # Инициализация счётчиков
    size_of_generated_continent = 0
    number_of_targets = 0

    # Генерируем континент
    while size_of_generated_continent < continent_size:
        size_of_queue = under_development.qsize()

        # Идём по всем обрабатываемым центрам генерации суши
        for i in range(size_of_queue):

            # Инициализация данных, используемых далее, и счётчиков
            number_of_targets += 1
            rand = random.randint(0, 100)
            counter = 0

            # Работаем с "лопающейся" клеткой
            coords = under_development.get()
            mates = map.pop(coords[0] // size_of_chunks_x, coords[1] // size_of_chunks_y, 1, size_of_chunks_x,
                            size_of_chunks_y)

            # Работа с соседями лопающейся клетки
            for mate in mates:
                square_mate = map.stock[mate[0]][mate[1]]
                if square_mate.type == 1:
                    counter += 1
                if square_mate.turn == 0 and square_mate.count >= 3:
                    under_development.put(mate)
                    square_mate.turn = 1

            # Работа непосредственно с лопающейся клуткой
            if map.stock[coords[0]][coords[1]].type == 0:
                if rand < counter * 28:
                    map.continent_tipisation(coords[0], coords[1])

        # Увеличиваем счётчик размера континента
        size_of_generated_continent += 1


# Генерация всех образов континентов
def generate_map_of_continents(map, size_of_chunks_x, size_of_chunks_y, number_of_chunks_x, number_of_chunks_y,
                               number_of_continents, size):
    numof_generated_ccntinents = 0
    while numof_generated_ccntinents < number_of_continents:

        # Ищем центр генерируемого континента
        rand_x = random.randint(1, number_of_chunks_x)
        rand_y = random.randint(1, number_of_chunks_y)
        if map.stock[size_of_chunks_x * rand_x][size_of_chunks_y * rand_y].typeres == 0:

            # Инициализируем центр континента
            map.initialize_center(size_of_chunks_x * rand_x, size_of_chunks_y * rand_y)

            # Собираем прямых соседей выбранного центра генерации
            mates = map.pop(rand_x, rand_y, 2, size_of_chunks_x, size_of_chunks_y)

            # Работа с прямыми соседями
            for mate in mates:
                rand = random.randint(1, 50) + random.randint(1, 50)
                # Заполняем соседей данными о посещаемости и типе биома
                if rand < 85:
                    map.continent_tipisation(mate[0], mate[1])

            # Генерируем континент
            continent_generate(map, rand_x, rand_y, size_of_chunks_x, size_of_chunks_y, size)

            # Обнуляем все поля генерации для их дальнейшего заполнения
            map.clear(size_of_chunks_x, size_of_chunks_y)

            # Увеличиваем количество континентов
            numof_generated_ccntinents += 1


# Генерация рельефа в конкретном биоме
def generate_chunk(map, center_x, center_y, radius, normal, t):
    counter = 0
    while counter < radius:
        size_of_queue = map.under_development.qsize()

        # Идём по "радиусу" лопнутых клеток
        for n in range(size_of_queue):
            # Узнаём, какую клетку сейчас нужно "лопнуть"
            coords = map.under_development.get()
            father = map.stock[coords[0]][coords[1]]

            # Заполнение "лопающейся" клетки
            map.popping_initialisation(coords, radius, counter)

            # Лопаем клетку
            mates = map.pop(coords[0], coords[1])

            # Идём по соседям лопающейся клетки
            for mate in mates:

                square_mate = map.stock[mate[0]][mate[1]]

                # Проверяем, не "лопнул" ли сосед клетки раньше?
                if square_mate.turn == 0:

                    # Увеличиваем высоту соседа "лопающейся" клетки
                    square_mate.main += father.main

                    # Если клетка получила данные с как минимум трёх соседей, то на "лопается" (добавляется к обрабатываемым)
                    if square_mate.count >= 3:
                        map.add_to_development(mate)

                    # В зависимости от типа местности, передаём сосседям разную скорость изменения высоты
                    map.speed_parameters_choosing(center_x, center_y, coords, mate, t, normal)

            # Чистим "лопнутого" соседа
            father.main = 0
            father.speed = 0
        counter += 1
    # Чистим все системные значения, для следующих итераций.
    map.clean_buffer()


# Генерация рельефа на всей карте
def generate_landscape(map, number_of_chunks_x, number_of_chunks_y, size_of_chunks_x, size_of_chunks_y, normal, t):
    # Идём по всем чанкам
    for i in range(1, number_of_chunks_x + 1):
        for j in range(1, number_of_chunks_y + 1):
            # Считаем расстояние, до которого будут генерироваться очаги генерации
            radius = max((2 * (len(map.stock) // (number_of_chunks_x + 1)) + 8),
                         (2 * (len(map.stock[0]) // (number_of_chunks_y + 1)) + 8))

            center_x = i * size_of_chunks_x
            center_y = j * size_of_chunks_y

            # Игнициализируем центр чанка
            map.biome_initialisation(center_x, center_y, normal, radius, t)

            # Генерируем "чанк"
            generate_chunk(map, center_x, center_y, radius, normal, t)


# Cохранение массива высот в txt файле filename
def write_map_array(stock, filename):
    # Создаём отдельный файл filename.txt
    file = open(filename + '.txt', 'w')

    # Пишем размер карты первыми 2 цифрами в файл
    file.write(str(len(stock)) + ' ' + str(len(stock[0])) + '\n')

    output = ""
    # Записываем каждую высоту в filename.txt
    for x in range(len(stock)):
        for y in range(len(stock[0])):
            output += str(stock[x][y]) + " "
        file.write(output + '\n')
        output = ""


# Генерация карты
def map_generator(sizemap_x, sizemap_y, number_of_continents, filename, normal, t, size):
    # Длина карты до аппроксимации
    length = sizemap_x * 4
    # Высота карты до аппроксимации
    heigth = sizemap_y * 4
    number_of_chunks_x = length // 25
    number_of_chunks_y = heigth // 25

    # Задаём необходимый размер карты
    map = square_map(length, heigth, sizemap_x, sizemap_y)

    size_of_chunks_x = length // (number_of_chunks_x + 1)
    size_of_chunks_y = heigth // (number_of_chunks_y + 1)
    numof_generated_ccntinents = 0

    # Генерируем карту континентов
    generate_map_of_continents(map, size_of_chunks_x, size_of_chunks_y, number_of_chunks_x, number_of_chunks_y,
                               number_of_continents, size)

    # Уведомляем об успешном размещении материков на образе карты
    print("Generating_started")

    # Генерируем высоты континента
    generate_landscape(map, number_of_chunks_x, number_of_chunks_y, size_of_chunks_x, size_of_chunks_y, normal, t)

    # Аппроксимация высот карты
    map.heigths_approximation()

    # Аппроксимация клеток карты
    map.approximation()

    write_map_array(map.interpolated_map, filename)

    return map.interpolated_map


# ----------------------------------------------------------------------------Тело программы----------------------------------------------------------------------

if __name__ == '__main__':
    # Работаем с окном вывода программы
    root = tk.Tk()
    root.title("Генератор карт")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    app = ExampleApp(root)
    if sys.platform != 'linux':
        root.wm_state('zoomed')
    else:
        root.wm_attributes('-zoomed', True)
    root.mainloop()
