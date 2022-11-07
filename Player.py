"""
    Class Player
"""


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
