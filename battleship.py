"""

Игра "Морской бой"

Игрок играет с компьютером.
Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже сходил.
Для представления корабля опишите класс Ship с конструктором принимающим в себя набор точек (координат) на игровой доске.
Опишите класс доски. Доска должна принимать в конструкторе набор кораблей.
Корабли должны находится на расстоянии минимум одна клетка друг от друга.
На каждой доске (у ИИ и у игрока) должно находится следующее количество кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение.
В случае, если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения.
Буквой X помечаются подбитые корабли, буквой T — промахи.

Побеждает тот, кто быстрее всех разгромит корабли противника.





# 1. Сделать общий алгоритм игры

# 2. Сделать класс поля

# 3. Сделать класс корабля

# 4. Сделать условия победы
"""
import random


class BattleshipGame:
    players = []

    field_size = None

    winner = None
    game_end = False

    def __init__(self):
        self.__init_players__()

        self.__init_fields__()

    def play(self):

        self.__fill_fields__()

        player = self.players[0]
        waiting = self.players[1]

        while not self.game_end:

            shot = self.__player_move__(player, waiting.get_field())

            self.__register_shot__(player, waiting, shot)

            self.__check_game_end__(waiting.get_field())

            if self.__check_game_end__(waiting.get_field()):
                self.winner = player
                break

            temp = player
            player = waiting
            waiting = temp

        print(f'Игра окончена! Победил игрок {self.winner}')


    def __register_shot__(self, playing, waiting, shot):
        # 1. ждущий ставит себе попадание, возвращает результат (мимо\ранил\потопил)
        waiting.get
        # 2. играющий ставит результат попадания себе в поле
    

    def __fill_fields__(self):
        # 1.2 отрисовывается поле
        # 1.3 игрок 1 расставляет свои корабли
        # 1.4 отрисовывается поле
        # 1.5 игрок 2 расставляет корабли
        for player in self.players:
            self.__fill_field__(player)

    def __fill_field__(self, player):

        print(f'Игрок {player.name} расставляет корабли.')

        if self.field_size == 8:
            ships_available = [2, 1]

            for ship_size in ships_available:
                x = 1
                player.get_field().place_ship(ship_size)


    def __init_players__(self):
        self.players.append(Player('Паша'))
        self.players.append(Player('Лена'))

        return

        player_0 = None
        player_1 = None

        while not player_0 and not player_1:
            name_0 = input(f'Введите имя первого игрока: ')
            if not name_0:
                print('Нужно ввести имя хотя бы одного игрока!')
                continue
            player_0 = Player(name_0)

            name_1 = input('Введите имя второго игрока (или ничего, если играем с компьютером): ')
            player_1 = Player(name_1) if name_1 else Player('', True)

        return player_0, player_1

    def __init_fields__(self):

        self.field_size = 8
        for player in self.players:
            new_field = Field(self.field_size, player)
            player.set_field(new_field)
        return

        print('Создание поля. Выберите размер:\n',
              '\t1: 8х8, 1х 3-кл; 2 шт. 2-кл; 3 шт. 1кл.\n',
              '\t2: 10х10, 1х 4-кл; 2 шт. 3-кл; 3 шт. 2кл., 4 шт. 1-кл.\n')
        field_size_input = ''

        while not self.field_size:

            field_size_input = input()

            if field_size_input == '1':
                self.field_size = 8
            elif field_size_input == '2':
                self.field_size = 10
            else:
                print('Выберите один из двух вариантов!\n',
                      '\t1: 8х8, 1х 3-кл; 2 шт. 2-кл; 3 шт. 1кл.\n',
                      '\t2: 10х10, 1х 4-кл; 2 шт. 3-кл; 3 шт. 2кл., 4 шт. 1-кл.\n')

    def __player_move__(self, player, enemy_field):
        x = 1
        print(f'Ход игрока {player.name}')

        while True:
            shot = input('Введите координаты выстрела')
            enemy_field.print()
            
            try:
                enemy_field.__check_shot_coordinates_correct__(shot)
            except ValueError:
                print("Введены не числа. Введите координаты в двух чисел чисел через пробел.")
                continue
            except IndexError:
                print("Введено не два числа. Введите два числа.")
                continue
            except self.BadShipPositionError as error:
                print(str(error))
                continue
            else:
                return shot
        

    def __check_game_end__(self, field):
        """

        :param player: кого проверяем (!но поле надо смотреть другого игрока!)
        :return:
        """
        # todo Условия окончания игры: 1. все корабли какого-то игрока побиты
        return True


class Player:
    field = None

    def __init__(self, name, ai=False):
        if ai:
            self.ai = True
            self.player_name = 'Компьютер'
        else:
            self.player_name = name
            self.ai = False

    def set_field(self, field):
        self.field = field

    def get_field(self):
        return self.field

    @property
    def name(self):
        return self.player_name

    @property
    def player_type(self):
        return self.ai


class Field:

    class BadShipPositionError(Exception):
        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None

        def __str__(self):
            if self.message:
                return self.message
            else:
                return 'BadShipPositionError has been raised'

    def __init__(self, field_size, player):
        
        self.ships = []
        self.field_size = field_size
        self.player = player

        self.field = []

        self.__create_field__()


    def __create_header__(self):
        self.field_header = []

        for i in range(self.field_size):
            self.field_header.append(f'{i: ^5}')


    def __create_field__(self):
        """
        Поле вида 
        [
            [ячейка0, ячейка1, ...],
            [...],
            ...
        ]
        """
        self.__create_header__()

        for i in range(self.field_size):
            line = []
            for cell in range(self.field_size):
                # print(f'Строка {line}: ячейка {cell}')
                line.append(f'{"-": ^5}')
            # print(f'Сформирована строка {res_line}')
            self.field.append(line)



    def __add_ships_to_field__(self):
        x = 1

    
    def __insert_ship_to_field__(self, ship_coords):
        for cell_coords in ship_coords:
            x = cell_coords[0]
            y = cell_coords[1]
            z = 1
            self.field[y][x] = f'{"|||||": ^5}'
            z = 1
            """
            Ship([(4, 3), (5, 3), (6, 3)])
            Ship([(0, 0), (1, 0)])
            Ship([(1, 4), (1, 5)])
            """


    def print(self):
        print('\n--- Моё поле ---\n')
        start_of_coordinates = f'{"O": ^5}'

        for ship in self.ships:
            coords = ship.get_coords()
            self.__insert_ship_to_field__(ship.get_coords())

        
        print(start_of_coordinates + ''.join(self.field_header))
        for i in range(self.field_size):
            line_to_print = self.field_header[i] + ''.join(self.field[i])
            print(line_to_print)


    def place_ship(self, ship_size):
        """
        Я решила передавать корабли не в конструктор, а создавать их отдельно.
        Во время игры я смотрю на поле и выбираю, в какую клетку надо поставить корабль.
        Следовательно, создавать корабль надо в классе "Поле"

        :param ship_size:
        :return:
        """
        # 0. нарисовать текущее состояние поля


        # 1. попросить ввести координаты

        while True:
            self.print()
            input_coords = input(f"Введите координаты корабля размера {ship_size} в формате х1 у1 x2 y2: ")

            try:
                coordinates = self.__check_coordinates__(input_coords, ship_size)

                # 2. координаты павильные, создаём корабль

            except ValueError:
                print("Введены не числа. Введите координаты в четырех чисел чисел через пробел.")
                continue
            except IndexError:
                print("Введено не четыре числа. Введите четыре числа.")
                continue
            except self.BadShipPositionError as error:
                print(str(error))
                continue
            else:
                self.ships.append(Ship(coordinates))
                break



    def __check_shot_coordinates_correct__(self, shot_input):
        """
        :return: status: 0 - потопил 1 - ранил 2 - мимо
        """
        print(f'Введены значения выстрела: {shot_input.split()} (длина {len(shot_input.split())})')

        # проверка числа введенных аргументов
        
        if len(shot_input.split()) != 2:
            raise self.BadShipPositionError(f'Неверное количество аргументов. Нужно 2, а введено {len(shot_input.split())}.')


        # 1. проверка что координаты - цифры
        try:
            int(shot_input.split()[0])
            int(shot_input.split()[1])
        except ValueError:
            raise
        except IndexError:
            raise

        # 2. проверка, что не вылезаем за пределы поля
        if any(coord for coord in shot_input if coord >= self.field_size or coord < 0):
            raise self.BadShipPositionError(f'Координаты выходят за пределы поля. Максимум {self.field_size - 1}, минимум 0')




    def __check_coordinates__(self, input_coordinates, ship_size):
        """

        :param input_coordinates: строка, где через пробел записаны цифры координат
        :return: разные исключения
        """
        res_coordinates = []

        print(f'Введены значения: {input_coordinates.split()} (длина {len(input_coordinates.split())})')

        # 0. проверка числа введённых аргументов
        if len(input_coordinates.split()) != 4:
            raise self.BadShipPositionError(f'Неверное количество аргументов. Нужно 4, а введено {len(input_coordinates.split())}.')


        # 1. проверка, что все координаты - цифры
        try:
            res_coordinates.append(int(input_coordinates.split()[0]))
            res_coordinates.append(int(input_coordinates.split()[1]))
            res_coordinates.append(int(input_coordinates.split()[2]))
            res_coordinates.append(int(input_coordinates.split()[3]))
        except ValueError:
            raise
        except IndexError:
            raise


        # 2. Проверка, что не вылезаем за границы поля
        if any(coord for coord in res_coordinates if coord >= self.field_size or coord < 0):
            raise self.BadShipPositionError(f'Координаты выходят за пределы поля. Максимум {self.field_size - 1}, минимум 0')




        # координаты (цифры) введены корректно с точки зрения типов данных. сейчас будем проверять с точки зрения игры.
        start = (res_coordinates[0], res_coordinates[1])
        end = (res_coordinates[2], res_coordinates[3])
        ship_horizontal = start[0] == end[0]
        ship_vertical = start[1] == end[1]

        # 3. Проверка, что корабль прямой
        if not ship_horizontal and not ship_vertical:
            raise self.BadShipPositionError('Корабль должен располагаться по вертикали или по горизонтали. Введён зигзаг.')



        if ship_horizontal:
            ship_cells_coords = set([(res_coordinates[0], res_coordinates[1] + i) for i in range(end[1] - start[1] + 1)])
        else:
            ship_cells_coords = set([(res_coordinates[0] + i, res_coordinates[1]) for i in range(end[0] - start[0] + 1)])

        # 4. Проверка, что координаты соответствуют длине корабля
        print(len(ship_cells_coords))
        if len(ship_cells_coords) != ship_size:
            raise self.BadShipPositionError(f'Координаты корабля не совпадают с его размерами. Нужная длина {ship_size}, '
                                            f'а по введённым координатам получается {len(ship_cells_coords)}')

        # todo проверка что координата не занята или не находится слишком близко к другому кораблю
        # ship_test_0 = Ship([(4, 3), (5, 3), (6, 3)])

        # ship_test_1 = Ship([(0, 0), (1, 0)])

        # ship_test_2 = Ship([(1, 4), (1, 5)])

        # self.ships.append(ship_test_0)
        # self.ships.append(ship_test_1)
        # self.ships.append(ship_test_2)


        around_cells = set()
        occupied_cells = set()

        for other_ship in self.ships:
            around_cells = around_cells.union(other_ship.get_around_coords())
            occupied_cells = occupied_cells.union(other_ship.get_coords())

        # 5. смотрим, не попадаем ли на корабль
        if ship_cells_coords.intersection(occupied_cells):
            raise self.BadShipPositionError('На указанных координатах расположен другой корабль.')

        # 6. смотрим, не попадаем ли на окружность корабля
        if ship_cells_coords.intersection(around_cells):
            raise self.BadShipPositionError('Нельзя ставить корабли впритирку.')

        x = 1
        return ship_cells_coords


class Ship:

    """
    Координата Х, Координата У, Поражённость
    {
        (0, 0): False,
        (0, 1): False,
        (0, 2): True,
    }
    """
    def __init__(self, coords):
        # 0 - потоплен
        # 1 - ранен
        # 2 - цел
        self.status = None
        self.cells = {}
        for cell_coord in coords:
            self.cells[cell_coord] = False


    def __refresh_status__(self):
        if all(self.get_cell_statuses()):
            self.status = 0
        elif any(self.get_cell_statuses()):
            self.status = 1
        else:
            self.status = 2


    def set_coords(self, coords):
        self.cells = {}
        for cell_coord in coords:
            self.cells[cell_coord] = False


    def get_size(self):
        return len(self.cells)

    def get_coords(self):
        return set(self.cells.keys())

    def get_cell_statuses(self):
        return self.cells.values()

    def get_cells(self):
        return self.cells




    def get_around_coords(self):
        res = set()
        for cell_coords in self.get_coords():
            # 1. x - 1
            res.add((cell_coords[0] - 1, cell_coords[1] - 1))
            res.add((cell_coords[0] - 1, cell_coords[1]))
            res.add((cell_coords[0] - 1, cell_coords[1] + 1))

            # 2. x
            res.add((cell_coords[0], cell_coords[1] - 1))
            res.add((cell_coords[0], cell_coords[1] + 1))

            # 3. x + 1
            res.add((cell_coords[0] + 1, cell_coords[1] - 1))
            res.add((cell_coords[0] + 1, cell_coords[1]))
            res.add((cell_coords[0] + 1, cell_coords[1] + 1))

        x = 1

        return res.difference(self.get_coords())



def __main__():
    print('Это игра "Морской бой!"')

    game = BattleshipGame()

    game.play()

__main__()
