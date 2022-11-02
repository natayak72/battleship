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
import os
import random


class BattleshipGame:
    def __init__(self):
        self.players = []

        self.winner = None
        self.game_end = False

        self.ships_available = [2]
        self.field_size = 8

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


    def __register_shot__(self, player, waiting, shot):
        # 0. ждущий ставит себе попадание, возвращает результат (мимо\ранил\потопил)
        x = 1
        shot_res, ship_coords = waiting.get_field().register_enemy_shot(shot)
        # 1. все ставит результат попадания себе в поле
        x = 1
        player.get_field().register_shot(shot_res, shot, ship_coords)
        x = 1



    def __fill_fields__(self):
        for player in self.players:
            self.__fill_field__(player)


    def __fill_field__(self, player):
        print(f'Игрок {player.name} расставляет корабли.')

        for ship_id, ship in player.get_field().get_ships().items():
            player.get_field().place_ship(ship_id, ship)



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

        for player in self.players:
            new_field = Field(self.field_size, player, self.ships_available)
            player.set_field(new_field)

        x = 1
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
        print('---------------------------\n')
        print(f'Ход игрока {player.name}')

        while True:
            player.get_field().print_both_fields()
            shot = input('Введите координаты выстрела по вражескому полю (справа)')

            try:
                enemy_field.__check_shot_coordinates_correct__(shot)
            except ValueError:
                print("Введены не числа. Введите координаты в двух чисел чисел через пробел.")
                continue
            except IndexError:
                print("Введено не два числа. Введите два числа.")
                continue
            except Field.BadShipPositionError as error:
                print(str(error))
                continue
            else:
                return [int(coordinate) for coordinate in shot.split()]


    def __check_game_end__(self, field):
        """

        :param player: кого проверяем (!но поле надо смотреть другого игрока!)
        :return:
        """
        # todo Условия окончания игры: 1. все корабли какого-то игрока побиты
        return False



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

    ship_symbol_x = '\u2593' * 5  # ▓
    ship_symbol_y = '\u2593' * 3

    ship_wounded_symbol_x = '\u2592' * 5  # ▒
    ship_wounded_symbol_y = '\u2592' * 3

    ship_killed_symbol_x = '\u2591' * 5   # ░
    ship_killed_symbol_y = '\u2591' * 3

    empty_cell_symbol = '-'
    start_of_coordinates_symbol = '\u25e4'  # ◤
    miss_symbol = 'X'


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

    def __init__(self, field_size, player, ships_available):

        self.ships = {ship_id: Ship(ship_size) for ship_id, ship_size in enumerate(ships_available)}
        self.ships_by_coordinates = {}  # { (1,1): ship_id в self.ships, (1,2): 1, (3,3): 2, (3,4): 2 }
        self.field_size = field_size
        self.player = player

        self.field = []
        self.enemy_field = self.field.copy()

        self.__create_field__()


    def set_symbol_to_field_cell(self, coords, symbol):
        x = 1
        self.field[coords[1]][coords[0]] = symbol
        x = 1


    def set_symbol_to_enemy_field_cell(self, coords, symbol):
        self.enemy_field[coords[1][coords[0]]] = symbol


    def get_field_size(self):
        return self.field_size


    def get_ship_id_by_coords(self, coords):
        try:
            return self.ships_by_coordinates[coords]
        except KeyError:
            return None


    def get_ship_by_id(self, ship_id):
        return self.ships[ship_id]


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
        lines = []
        enemy_lines = lines.copy()

        for i in range(self.field_size):
            line = []
            for cell in range(self.field_size):
                line.append(f'{self.empty_cell_symbol: ^5}')
            lines.append(line)


        for i in range(self.field_size):
            enemy_line = []
            for cell in range(self.field_size):
                enemy_line.append(f'{self.empty_cell_symbol: ^5}')
            enemy_lines.append(enemy_line)


        self.field = lines
        self.enemy_field = enemy_lines


    def __insert_ship_to_field__(self, ship_coords):
        # узнать, по горизонтали корабль или по вертикали
        if ship_coords[0][0] == ship_coords[1][0]:
            symbol = self.ship_symbol_y
        else:
            symbol = self.ship_symbol_x

        for cell_coords in ship_coords:
            x = 1
            self.set_symbol_to_field_cell(cell_coords, f'{symbol: ^5}')
            x = 1
            # self.field[y][x] = f'{symbol: ^5}'

    @staticmethod
    def print_field(field):
        print('\n')
        for line in field:
            print(line)
        print('\n')


    def print_both_fields(self):
        my_field = self.get_field()
        enemy_field = self.get_enemy_field()

        my_header = f'{"Моё поле": ^60}'
        enemy_header = f'{"Вражеское поле": ^60}'
        field_width = len(my_field[0])

        try:
            terminal_size = os.get_terminal_size()
        except OSError as error:
            terminal_size = 120  # примерно чуть больше половины
            my_header = f'{"Моё поле": ^50}'
            enemy_header = f'{"Вражеское поле": ^50}'
            pass

        if self.get_field_size() == 8:

            my_header = f'{"Моё поле": ^45}'
            enemy_header = f'{"Вражеское поле": ^45}'

        space_between_fields_size = terminal_size - field_width * 2

        lines = []

        common_header = f'{my_header}{" " * space_between_fields_size}{enemy_header}'
        print(common_header)
        x = 1
        for my_line, enemy_line in zip(my_field, enemy_field):
            line = f'{my_line}{" " * space_between_fields_size}{enemy_line}'
            print(line)

        print('\n')


    def get_enemy_field(self):
        lines = []
        start_of_coordinates = f'{self.start_of_coordinates_symbol: ^5}'
        lines.append(start_of_coordinates + ''.join(self.field_header))
        for i, line in enumerate(self.enemy_field):

            line = self.field_header[i] + ''.join(line)
            lines.append(line)
        return lines


    def get_field(self):
        lines = []
        start_of_coordinates = f'{self.start_of_coordinates_symbol: ^5}'
        lines.append(start_of_coordinates + ''.join(self.field_header))
        for i in range(self.field_size):
            line_to_print = self.field_header[i] + ''.join(self.field[i])
            lines.append(line_to_print)
        return lines


    def get_shot_res(self, shot_coords):
        """

        :param shot_coords:
        :return: 0 - потопил 1 - ранил 2 - мимо
        """
        x = 1
        ship_id = self.get_ship_id_by_coords(tuple(shot_coords))
        x = 1
        status = self.get_ship_by_id(ship_id).get_ship_status()
        x = 1


    def register_enemy_shot(self, shot_coords):
        """

        :param shot_coords:
        :return: status, ship_coords - возвращаются координаты потопленного корабля, если такое случилось,
                                        чтобы стреляющий смог отметить его у себя.
        """
        x = shot_coords[0]
        y = shot_coords[1]
        ship_id = self.get_ship_id_by_coords(tuple(shot_coords))

        if ship_id is not None:
            ship = self.get_ship_by_id(ship_id)
            ship.cells[tuple(shot_coords)] = True
            status = ship.get_ship_status()

            if status == 1:
                if ship.direction == 0:
                    self.field[y][x] = f'{self.ship_wounded_symbol_x: ^5}'
                else:
                    self.field[y][x] = f'{self.ship_wounded_symbol_y: ^5}'
                return 1, None
            elif status == 0:
                ship_coords = ship.get_coords()
                # пометить потопленным весь корабль
                if ship.direction == 0:
                    for coord in ship_coords:
                        self.field[coord[1]][coord[0]] = f'{self.ship_killed_symbol_x: ^5}'
                else:
                    for coord in ship_coords:
                        self.field[coord[1]][coord[0]] = f'{self.ship_killed_symbol_y: ^5}'

                return 0, ship_coords
        else:
            self.field[y][x] = f'{self.miss_symbol: ^5}'
            return 2, None


    def register_shot(self, shot_result, shot_coords, ship_coords):
        """

        :param shot_result: 0 - потопил, 1 - ранил, 2 - мимо
        :param shot_coords: - координаты выстрела
        :param ship_coords: - координаты потопленного корабля, если это случилось
        :return:
        """
        x = 1
        if shot_result == 0:
            x = 1
            if ship_coords[0][0] != ship_coords[1][0]:
                for coord in ship_coords:
                    self.enemy_field[coord[1]][coord[0]] = f'{self.ship_killed_symbol_x: ^5}'
            else:
                for coord in ship_coords:
                    self.enemy_field[coord[1]][coord[0]] = f'{self.ship_killed_symbol_y: ^5}'
        elif shot_result == 1:
            x = 1
            self.enemy_field[shot_coords[1]][shot_coords[0]] = f'{self.ship_wounded_symbol_x: ^5}'
        else:
            self.enemy_field[shot_coords[1]][shot_coords[0]] = f'{self.miss_symbol: ^5}'


    def place_ship(self, ship_id, ship):
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
            self.print_field(self.get_field())
            input_coords = input(f"Введите координаты корабля размера {ship.get_size()} в формате х1 у1 x2 y2: ")

            try:
                coordinates = self.__check_coordinates__(input_coords, ship.get_size())

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
                x = 1
                ship.set_coords(coordinates)
                x = 1
                self.__insert_ship_to_field__(coordinates)
                for coordinate in coordinates:
                    self.ships_by_coordinates[coordinate] = ship_id
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
        x = 1
        if any(coord for coord in shot_input.split() if int(coord) >= self.field_size or int(coord) < 0):
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

        for other_ship in self.get_ships().values():
            around_cells = around_cells.union(other_ship.get_around_coords())
            occupied_cells = occupied_cells.union(other_ship.get_coords())

        # 5. смотрим, не попадаем ли на корабль
        if ship_cells_coords.intersection(occupied_cells):
            raise self.BadShipPositionError('На указанных координатах расположен другой корабль.')

        # 6. смотрим, не попадаем ли на окружность корабля
        if ship_cells_coords.intersection(around_cells):
            raise self.BadShipPositionError('Нельзя ставить корабли впритирку.')

        x = 1
        return list(ship_cells_coords)


    def get_ship(self, ship_id):
        return self.ships[ship_id]


    def get_ships(self):
        return self.ships


class Ship:

    """
    Координата Х, Координата У, Поражённость
    {
        (0, 0): False,
        (0, 1): False,
        (0, 2): True,
    }
    """
    def __init__(self, size):
        self.size = size

        # 0 - потоплен
        # 1 - ранен
        # 2 - цел
        self.status = None

        self.cells = {}

        # 0 - горизонтально
        # 1 - вертикально
        self.direction = 0


    def __refresh_status__(self):
        if all(self.get_cell_statuses()):
            self.status = 0
        elif any(self.get_cell_statuses()):
            self.status = 1
        else:
            self.status = 2

    def set_coords(self, coords):
        self.cells = {}
        x1 = coords[0][0]
        x2 = coords[1][0]

        y1 = coords[0][1]
        y2 = coords[1][1]
        if x1 != x2 and y1 == y2:
            self.direction = 0
        else:
            self.direction = 1

        for cell_coord in coords:
            self.cells[cell_coord] = False

    def get_size(self):
        return self.size

    def get_coords(self):
        return list(self.cells.keys())

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

    def get_ship_status(self):
        """

        :return: 0 - потомлен 1 - ранен 2 - целый
        """
        if all(self.get_cell_statuses()):
            self.status = 0
        elif any(self.get_cell_statuses()):
            self.status = 1
        else:
            self.status = 2

        return self.status



def __main__():
    print('Это игра "Морской бой!"')

    game = BattleshipGame()

    game.play()


__main__()

