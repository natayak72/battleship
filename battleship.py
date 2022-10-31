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


class Player:
    def __init__(self, name, ai=False):
        if ai:
            self.ai = True
            self.player_name = 'Компьютер'
        else:
            self.player_name = name
            self.ai = False


    @property
    def name(self):
        return self.player_name

    @property
    def player_type(self):
        return self.ai


def init_players():
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


def is_player_won():
    """

    :return:
    """
    return False


def no_space_left():
    return True


def run_game(player_0, player_1):
    print('Игра начинается!')

    # 1.1 выбирается случайный игрок
    # 1.2 игрок расставляет свои корабли
    # 1.3 второй игрок расставляет корабли

    # --- 1.1
    if random.random() > 0.5:
        playing_player = player_0
        waiting_player = player_1
    else:
        playing_player = player_1
        waiting_player = player_0


    # --- 1.2
    # TODO реализовать Field.setShips(player)



    # 2.1 начинаются ходы

    # 3. если достигнуто условие окончания игры - выход



    print('Игра окончена!')
    return ''



def __main__():
    print('Это игра "Морской бой!"')

    player_0, player_1 = init_players()

    won_name = run_game(player_0, player_1)

    print(f'Играли игроки: ')
    print(f'{player_0.name} vs {player_1.name}')

    if won_name:
        print(f'Победил игрок {won_name}!')
    else:
        print('Ничья!')


__main__()

