import random


class Deck:
    def __init__(self):
        # Generate a full deck of 52 cards by combining ranks and suits
        self.cards = [
            (rank, suit) for rank in list(range(2, 11)) + ['J', 'Q', 'K', 'A']
            for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ]
        # Shuffle the deck to randomise the order of cards.
        random.shuffle(self.cards)

    def draw_card(self):
        # Pop and return the top card from the deck, or return None if the deck is empty.
        return self.cards.pop() if self.cards else None
