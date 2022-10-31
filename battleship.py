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

    player_0 = None
    player_1 = None

    field_0 = None
    field_1 = None

    field_size = None

    def __init__(self):
        self.__init_players__()

        self.__init_fields__()


    def play(self):

        self.__fill_fields__()
        


    def __fill_fields__(self):
        # 1.2 отрисовывается поле
        # 1.3 игрок 1 расставляет свои корабли
        # 1.4 отрисовывается поле
        # 1.5 игрок 2 расставляет корабли
        self.__fill_field__(self.player_0, self.field_0)
        self.__fill_field__(self.player_1, self.field_1)

    
    def __fill_field__(self, player, field):
        field.print()
        print(f'Игрок {player.name} расставляет корабли.')

        if self.field_size == 8:
            ships_available = [3, 2, 2, 1, 1, 1]


            for ship in ships_available:
                while True:
                    ship_coords = input("Введите координаты корабля на 3 клетки (х, у): ")
                    try:
                        coord_x = int(ship_coords.spit()[0])
                        coord_y = int(ship_coords.spit()[1])

                        if coord_x > self.field_size or coord_y > self.field_size:
                            print(f'Введите координаты в пределах поля: максимум {self.field_size}')

                        # TODO проверка классом field на то, что данный корабль можно сюда поставить
                    except ValueError:
                        print("Введите координаты в виде двух чисел через пробел.")
                        continue
                    else:
                        print(f'You entered: {integer}')
                        break





    def __init_players__(self):
        self.player_0 = Player('Паша')
        self.player_1 = Player('Лена')

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
        self.field_0 = Field(self.field_size)
        self.field_1 = Field(self.field_size)
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


class Field:

    field_size = 8
    lines = None


    def __init__(self, field_size):
        self.field_size = field_size

        self.__create_field__()

        print('Поле создано')

        self.print()


    def __create_field__(self):
            self.lines = []
            header = f'{"*": ^5}'
            for i in range(self.field_size):
                header += f'{i: ^5}'

            self.lines.append(header + '\n')
            
            
            for x, line in enumerate(range(self.field_size)): 
                res_line = f'{x: ^5}'

                for cell in range(self.field_size):
                    # print(f'Строка {line}: ячейка {cell}')
                    res_line += f'{"-": ^5}'
                # print(f'Сформирована стркоа {res_line}')
                res_line += '\n'

                self.lines.append(res_line)

    
    def print(self):
        print('\n\n')
        for line in self.lines:
            print(line)


class Ship:
    size = None
    coords = None
    cells = []

    def __init__(self, size):





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
    
    

    # --- 1.1
    if random.random() > 0.5:
        playing_player = player_0
        waiting_player = player_1
    else:
        playing_player = player_1
        waiting_player = player_0


    field = Field()


    # --- 1.2
    # TODO реализовать Field.setShips(player)



    # 2.1 начинаются ходы

    # 3. если достигнуто условие окончания игры - выход



    print('Игра окончена!')
    return ''



def __main__():
    print('Это игра "Морской бой!"')

    game = BattleshipGame()

    game.run_game()


    won_name = run_game(player_0, player_1)

    print(f'Играли игроки: ')
    print(f'{player_0.name} vs {player_1.name}')

    if won_name:
        print(f'Победил игрок {won_name}!')
    else:
        print('Ничья!')


__main__()

