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


"""
import random
import time


class BattleshipGame:
    def __init__(self):
        self.players = []

        self.winner = None
        self.game_end = False

        self.ships_available = None
        self.field_size = None

        self.__init_players__()

        self.__init_fields__()

    def play(self):
        self.__fill_fields__()

        player = self.players[0]
        waiting = self.players[1]

        while not self.game_end:
            shot = self.__player_move__(player, waiting.get_field())

            shot_res = self.__register_shot__(player, waiting, shot)

            if self.__check_game_end__(waiting.get_field()):
                self.winner = player
                print(f'Игра окончена! Победил игрок {player.name}')
                print('Расклад кораблей:')
                player.get_field().print_both_fields()
                break

            if shot_res == 2:   # Ход переходит только если играющий промахнулся
                temp = player
                player = waiting
                waiting = temp

            time.sleep(1)

    def __register_shot__(self, player, waiting, shot):
        shot_res, ship_coords = waiting.get_field().register_enemy_shot(shot)
        if shot_res == 0:
            print(f'\n{"Потопил!": ^50}')
        elif shot_res == 1:
            print(f'\n{"Ранил!": ^50}')
        else:
            print(f'\n{"Мимо!": ^50}')
        player.get_field().register_shot(shot_res, shot, ship_coords)

        return shot_res


    def __generate_random_shot__(self, field):
        cells = []
        for y, line in enumerate(field):
            for x, cell in enumerate(line):
                if Field.miss_symbol not in cell:
                    cells.append([x, y])
                else:
                    continue

        shot_cell = random.randint(0, len(cells))
        return cells[shot_cell]

    def __fill_fields__(self):
        for player in self.players:
            self.__fill_field__(player)

    def __fill_field__(self, player):
        print(f'Игрок {player.name} расставляет корабли.')
        for ship_id, ship in player.get_field().get_ships().items():
            player.get_field().place_ship(ship_id, ship)

    def __init_players__(self):
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

        self.players.append(player_0)
        self.players.append(player_1)

    def __init_fields__(self):
        while True:
            print(f'Выберите вариант игры. На данный момент доступно два размера поля:')
            var_1 = '\t1: 5х5, корабли: \n\t\t1 2-клеточный;\n\t\t2 1-клеточных.\n'
            var_2 = '\t1: 8х8, корабли: \n\t\t1 3-клеточный;\n\t\t2 2-клеточных;\n\t\t3 1клеточных.\n'
            var_3 = '\t2: 10х10, корабли:\n\t\t1 4-клеточный;\n\t\t2 3-клеточных;\n\t\t3 2клеточных;\n\t\t4 1-клеточных.\n'
            field_size_input = input(var_1 + var_2 + var_3)

            if not isinstance(int(field_size_input), int):
                print('Введите число!')
                continue
            elif field_size_input == '1':
                self.field_size = 5
                self.ships_available = [2, 1, 1]
                break
            elif field_size_input == '2':
                self.field_size = 8
                self.ships_available = [3, 2, 2, 1, 1, 1]
                break
            elif field_size_input == '3':
                self.field_size = 10
                self.ships_available = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
                break
            else:
                print('Выберите один из вариантов!')
                continue

        for player in self.players:
            new_field = Field(self.field_size, player, self.ships_available)
            player.set_field(new_field)

    def __player_move__(self, player, enemy_field):
        help_messages = [f'{Field.ship_symbol_y} - корабль', f'{Field.ship_wounded_symbol_y} - раненый', f'{Field.ship_killed_symbol_y} - потопленный']
        print('\n')
        print(f'{"-" * 40} Ход игрока {player.name} {"-" * 40}')
        for help_msg in help_messages:
            print(help_msg)
        print('\n')

        while True:
            player.get_field().print_both_fields()

            while True:
                rand_coords = self.__generate_random_shot__(player.get_field().enemy_field)
                if not player.get_field().__check_cell_hit__(rand_coords):
                    break

            if player.ai:
                shot = f'{rand_coords[0]} {rand_coords[1]}'
                print(f'Компьютер стреляет по {rand_coords}')
            else:
                shot = input(f'{player.name}, введите координаты выстрела по вражескому полю (справа)')

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
        # Если остался хотя бы один корабль, статус которого не "потоплен" - игра не окончена
        for ship in field.ships.values():
            if ship.status != 0:
                return False
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
    # ship_symbol_x = '\u2593' * 5  # ▓
    # ship_symbol_y = '\u2593' * 3

    ship_symbol_x = '|' * 5
    ship_symbol_y = '|' * 3

    # ship_wounded_symbol_x = '\u2592' * 5  # ▒
    # ship_wounded_symbol_y = '\u2592' * 3

    ship_wounded_symbol_x = '+' * 5
    ship_wounded_symbol_y = '+' * 3

    # ship_killed_symbol_x = '\u2591' * 5  # ░
    # ship_killed_symbol_y = '\u2591' * 3

    ship_killed_symbol_x = '*' * 5
    ship_killed_symbol_y = '*' * 3

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
        self.ships_by_coordinates = {}
        self.field_size = field_size
        self.player = player

        self.field = []
        self.enemy_field = self.field.copy()

        self.__create_field__()

    def set_symbol_to_field_cell(self, coords, symbol):
        self.field[coords[1]][coords[0]] = symbol

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


    def __check_cell_hit__(self, coords):
        if self.miss_symbol not in self.enemy_field[coords[1]][coords[0]]:
            return False
        else:
            return True


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
        if len(ship_coords) == 1:
            self.set_symbol_to_field_cell(*ship_coords, f'{self.ship_symbol_x: ^5}')
            return

        if ship_coords[0][0] == ship_coords[1][0]:
            symbol = self.ship_symbol_y
        else:
            symbol = self.ship_symbol_x

        for cell_coords in ship_coords:
            self.set_symbol_to_field_cell(cell_coords, f'{symbol: ^5}')

    @staticmethod
    def print_field(field):
        print('\n')
        for line in field:
            print(line)
        print('\n')

    def print_both_fields(self):
        my_field = self.get_field()
        enemy_field = self.get_enemy_field()

        field_width = len(my_field[0])  # (60 - 10) / 2
        my_header = ' ' * int((field_width - 10) / 2) + ' Моё поле ' + ' ' * int((field_width - 10) / 2)
        enemy_header = ' ' * int((field_width - 16) / 2) + ' Вражеское поле ' + ' ' * int((field_width - 16) / 2)


        space_between_fields_size = 50



        common_header = f'{my_header}{" " * space_between_fields_size}{enemy_header}'
        print(common_header)
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
        if shot_result == 0:
            if len(ship_coords) != 1:
                if ship_coords[0][0] != ship_coords[1][0]:
                    for coord in ship_coords:
                        self.enemy_field[coord[1]][coord[0]] = f'{self.ship_killed_symbol_x: ^5}'
                else:
                    for coord in ship_coords:
                        self.enemy_field[coord[1]][coord[0]] = f'{self.ship_killed_symbol_y: ^5}'
            else:
                self.enemy_field[ship_coords[0][1]][ship_coords[0][0]] = f'{self.ship_killed_symbol_x: ^5}'
        elif shot_result == 1:
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
            if ship.get_size() == 1:
                msg = f"{self.player.name}, введите координаты корабля размера {ship.get_size()} в формате х y: "
            else:
                msg = f"{self.player.name}, введите координаты корабля размера {ship.get_size()} в формате х1 у1 x2 y2: "

            input_coords = input(msg)

            try:
                coordinates = self.__check_coordinates__(input_coords, ship.get_size())

                # 2. координаты павильные, создаём корабль

            except ValueError:
                print("Введены не числа. Введите координаты числами через пробел.")
                continue
            except IndexError:
                if ship.get_size() == 1:
                    print(f"Введено неверное число координат ({len(input_coords)}). Нужно 2.")
                else:
                    print(f"Введено неверное число координат({len(input_coords)}). Нужно 4.")
                continue
            except self.BadShipPositionError as error:
                print(str(error))
                continue
            else:
                ship.set_coords(coordinates)
                self.__insert_ship_to_field__(coordinates)
                for coordinate in coordinates:
                    self.ships_by_coordinates[coordinate] = ship_id
                break

    def __check_shot_coordinates_correct__(self, shot_input):
        """
        :return: status: 0 - потопил 1 - ранил 2 - мимо
        """
        # print(f'Введены значения выстрела: {shot_input.split()} (длина {len(shot_input.split())})')

        # проверка числа введенных аргументов

        if len(shot_input.split()) != 2:
            raise self.BadShipPositionError(
                f'Неверное количество аргументов. Нужно 2, а введено {len(shot_input.split())}.')

        # 1. проверка что координаты - цифры
        try:
            int(shot_input.split()[0])
            int(shot_input.split()[1])
        except ValueError:
            raise
        except IndexError:
            raise

        # 2. проверка, что не вылезаем за пределы поля
        if any(coord for coord in shot_input.split() if int(coord) >= self.field_size or int(coord) < 0):
            raise self.BadShipPositionError(
                f'ОШИБКА! Координаты выходят за пределы поля. Максимум {self.field_size - 1}, минимум 0')

        # 3. проверка, что в это поле ещё не стреляли
        if self.miss_symbol in self.field[int(shot_input.split()[1])][int(shot_input.split()[0])]:
            raise self.BadShipPositionError(f'ОШИБКА! По данным координатам уже стреляли! Введите другие координаты. {self.hit_fields}')

    def __check_coordinates__(self, input_coordinates, ship_size):
        """

        :param input_coordinates: строка, где через пробел записаны цифры координат
        :return: разные исключения
        """
        res_coordinates = []

        # print(f'Введены значения: {input_coordinates.split()} (длина {len(input_coordinates.split())})')

        # 0. проверка числа введённых аргументов
        if ship_size != 1:
            if len(input_coordinates.split()) != 4:
                raise self.BadShipPositionError(
                    f'ОШИБКА! Неверное количество аргументов. Нужно 4, а введено {len(input_coordinates.split())}.')
        else:
            if len(input_coordinates.split()) != 2:
                raise self.BadShipPositionError(f'ОШИБКА! Неверное количество аргументов. Нужно 2, а введено {len(input_coordinates.split())}.')

        # 1. проверка, что все координаты - цифры
        try:
            if ship_size == 1:
                res_coordinates.append(int(input_coordinates.split()[0]))
                res_coordinates.append(int(input_coordinates.split()[1]))
            else:
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
            raise self.BadShipPositionError(
                f'ОШИБКА! Координаты выходят за пределы поля. Максимум {self.field_size - 1}, минимум 0')

        # координаты (цифры) введены корректно с точки зрения типов данных. сейчас будем проверять с точки зрения игры.
        if ship_size != 1:
            start = (res_coordinates[0], res_coordinates[1])
            end = (res_coordinates[2], res_coordinates[3])
            ship_horizontal = start[0] == end[0]
            ship_vertical = start[1] == end[1]

            # 3. Проверка, что корабль прямой
            if not ship_horizontal and not ship_vertical:
                raise self.BadShipPositionError(
                    'ОШИБКА! Корабль должен располагаться по вертикали или по горизонтали. Введён зигзаг.')

            if ship_horizontal:
                ship_cells_coords = set([(res_coordinates[0], res_coordinates[1] + i) for i in range(end[1] - start[1] + 1)])
            else:
                ship_cells_coords = set([(res_coordinates[0] + i, res_coordinates[1]) for i in range(end[0] - start[0] + 1)])
        else:
            ship_cells_coords = {(res_coordinates[0], res_coordinates[1])}  # x = {...} - множество

        # 4. Проверка, что координаты соответствуют длине корабля
        if len(ship_cells_coords) != ship_size:
            raise self.BadShipPositionError(
                f'ОШИБКА! Координаты корабля не совпадают с его размерами. Нужная длина {ship_size}, '
                f'а по введённым координатам получается {len(ship_cells_coords)}')

        around_cells = set()
        occupied_cells = set()

        for other_ship in self.get_ships().values():
            around_cells = around_cells.union(other_ship.get_around_coords())
            occupied_cells = occupied_cells.union(other_ship.get_coords())

        # 5. смотрим, не попадаем ли на корабль
        if ship_cells_coords.intersection(occupied_cells):
            raise self.BadShipPositionError('ОШИБКА! На указанных координатах расположен другой корабль.')

        # 6. смотрим, не попадаем ли на окружность корабля
        if ship_cells_coords.intersection(around_cells):
            raise self.BadShipPositionError('ОШИБКА! Нельзя ставить корабли впритирку.')

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


    def set_coords(self, coords):
        self.cells = {}

        if len(coords) == 1:
            self.cells[coords[0]] = False
            return

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
