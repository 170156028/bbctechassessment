from .player import Player


class Dealer(Player):
    def __init__(self, deck):
        # Calls the parent (Player) class's constructor to initialize shared attributes.
        super().__init__(deck=deck, player_number=0)
