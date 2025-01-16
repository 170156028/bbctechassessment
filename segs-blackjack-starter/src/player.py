class Player:
    MAX_SCORE = 21

    def __init__(self, deck, player_number):
        self.hand = [] # The player's current hand of cards, initially empty.
        self.score = 0 # The initial score is set to 0
        self.deck = deck # Reference to the shared deck object for drawing cards.
        self.player_number = player_number # Unique identifier for the player.


    def init_draw_cards(self):
        # Adds two cards from the deck to the player's hand
        self.hand.extend([self.deck.cards.pop(), self.deck.cards.pop()])


    def hit(self):
        # Draw one card from the deck and add it to the player's hand, if cards remain in the deck.
        self.hand.append(self.deck.cards.pop() if self.deck.cards else None)


    def is_bust(self):
        # Returns True if the player's score exceeds 21; otherwise, returns False.
        return self.score > self.MAX_SCORE
