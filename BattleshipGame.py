import os
import random
import time

from Field import Field
from Player import Player


def __check_game_end__(field):
    """

    :param field: кого проверяем (!но поле надо смотреть другого игрока!)
    :return:
    """
    # Если остался хотя бы один корабль, статус которого не "потоплен" - игра не окончена
    for ship in field.ships.values():
        if ship.status != 0:
            return False
    return True


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def __fill_field__(player):
    print(f'Игрок {player.name} расставляет корабли.')
    for ship_id, ship in player.get_field().get_ships().items():
        player.get_field().place_ship(ship_id, ship)


def __generate_random_shot__(field):
    cells = []
    for y, line in enumerate(field):
        for x, cell in enumerate(line):
            if Field.miss_symbol not in cell:
                cells.append([x, y])
            else:
                continue

    shot_cell = random.randint(0, len(cells))
    return cells[shot_cell]


def __register_shot__(player, waiting, shot):
    shot_res, ship_coords = waiting.get_field().register_enemy_shot(shot)
    if shot_res == 0:
        print(f'\n{"Потопил!": ^50}')
    elif shot_res == 1:
        print(f'\n{"Ранил!": ^50}')
    else:
        print(f'\n{"Мимо!": ^50}')
    player.get_field().register_shot(shot_res, shot, ship_coords)

    return shot_res


def __player_move__(player, enemy_field):



    help_messages = [f'{Field.ship_symbol_y} - корабль', f'{Field.ship_wounded_symbol_y} - раненый', f'{Field.ship_killed_symbol_y} - потопленный']
    print('\n')
    print(f'{"-" * 40} Ход игрока {player.name} {"-" * 40}')
    for help_msg in help_messages:
        print(help_msg)
    print('\n')

    while True:
        player.get_field().print_both_fields()

        while True:
            rand_coords = __generate_random_shot__(player.get_field().enemy_field)
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
            shot = __player_move__(player, waiting.get_field())

            shot_res = __register_shot__(player, waiting, shot)

            if __check_game_end__(waiting.get_field()):
                self.winner = player
                print(f'Игра окончена! Победил игрок {player.name}')
                print('Расклад кораблей:')
                player.get_field().print_both_fields()
                break

            if shot_res == 2:   # Ход переходит только если играющий промахнулся
                temp = player
                player = waiting
                waiting = temp
                clear_screen()

            time.sleep(1)

    def __fill_fields__(self):
        for player in self.players:
            __fill_field__(player)

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
            print(f'Выберите вариант игры. На данный момент доступны следующие варианты:')
            var_4 = '\t2: 4х4, корабли:\n\t\t1 1-клеточный.\n'
            var_1 = '\t1: 5х5, корабли: \n\t\t1 2-клеточный;\n\t\t2 1-клеточных.\n'
            var_2 = '\t1: 8х8, корабли: \n\t\t1 3-клеточный;\n\t\t2 2-клеточных;\n\t\t3 1клеточных.\n'
            var_3 = '\t2: 10х10, корабли:\n\t\t1 4-клеточный;\n\t\t2 3-клеточных;\n\t\t3 2клеточных;\n\t\t4 1-клеточных.\n'
            field_size_input = input(var_1 + var_2 + var_3 + var_4)

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
            elif field_size_input == '4':
                self.field_size = 4
                self.ships_available = [1]
                break
            else:
                print('Выберите один из вариантов!')
                continue

        for player in self.players:
            new_field = Field(self.field_size, player, self.ships_available)
            player.set_field(new_field)
