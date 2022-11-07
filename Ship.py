"""
    Class Ship
"""


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
