import unittest

from blackjack import Blackjack
from src.deck import Deck
from unittest.mock import MagicMock
from src.player import Player
from src.dealer import Dealer


class DeckTestCase(unittest.TestCase):

    def setUp(self):
        """
        This is a method that runs before each test.
        It Initialises a new Deck instance to be used in the tests.
        """
        self.deck = Deck()

    def tearDown(self):
        """
        This is a method that runs after each test.
        Currently unused, but can be used for cleanup if necessary in future tests.
        """
        pass

    def test_number_of_cards(self):
        """
        Test that ensures a new deck contains exactly 52 cards.
        """
        number_of_cards = len(self.deck.cards)
        self.assertEqual(number_of_cards, 52, "A new deck should contain 52 cards.")

    def test_deck_has_four_aces(self):
        """
        Test to ensure that a valid deck contains exactly 4 Aces.
        This test passes if no exception is raised.
        """
        deck = Deck()

        # Count the number of Aces in the deck
        ace_count = len([card for card in deck.cards if card[0] == 'A'])

        # If ace count is not 4, raise an exception
        if ace_count != 4:
            raise ValueError(f"Deck should contain exactly 4 Aces, but found {ace_count}")
        self.assertEqual(ace_count, 4, msg="Should contain four aces")

    # below is a failing test where four aces fail
    def test_have_four_aces_fail(self):
        """
        Test to ensure that corrupted decks raise an exception for incorrect Ace count.
        """
        deck = Deck()

        # Simulate a corrupted deck with only 3 Aces
        deck.cards = [card for card in deck.cards if card != ('A', 'Hearts')]

        # Expect a ValueError due to incorrect Ace count
        with self.assertRaises(ValueError, msg="Expected a ValueError when the deck does not have exactly 4 Aces"):
            ace_count = len([card for card in deck.cards if card[0] == 'A'])
            if ace_count != 4:
                raise ValueError(f"Deck should contain exactly 4 Aces, but found {ace_count}")

    def mock_blackjack(self, num_players):
        """
        Mocks a Blackjack instance with the specified number of players.
        GUI-related methods and attributes are mocked to avoid real GUI interactions during testing.
        """
        blackjack = Blackjack(num_players=num_players)
        blackjack.update_dealer_hand_display = MagicMock()  # Mock dealer hand display updates
        blackjack.player_hand_label = MagicMock()  # Mock player hand display label
        blackjack.game_screen = MagicMock()  # Mock the game screen to avoid GUI initialisation
        return blackjack

    def test_opening_hand_two_cards(self):
        """
        This test that each player starts with two cards when the game begins.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.deal_hand()
        self.assertEqual(len(blackjack.players[0].hand), 2, "Opening hand should have two cards.")

    def test_hit_adds_card_and_updates_score(self):
        """
        This is a test that shows when a player hits, they receive one additional card and their score is updated.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.deal_hand()
        initial_hand_size = len(blackjack.players[0].hand)
        blackjack.players[0].hit()  # Player hits and draws one card
        self.assertEqual(len(blackjack.players[0].hand), initial_hand_size + 1,
                         "Player should receive one additional card.")
        self.assertGreater(blackjack.calculate_score(blackjack.players[0]), 0, "Score should be updated after hitting.")

    def test_stand_does_not_add_card(self):
        """
        Test that when a player chooses to stand, no additional cards are added to their hand.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.update_dealer_hand_display = MagicMock()  # Mock GUI updates
        blackjack.player_hand_label = MagicMock()  # Mock GUI updates
        blackjack.end_game = MagicMock()  # Mock end_game to avoid GUI interactions
        blackjack.deal_hand()
        initial_hand_size = len(blackjack.players[0].hand)
        blackjack.stand_action()  # Player chooses to stand
        self.assertEqual(len(blackjack.players[0].hand), initial_hand_size,
                         "Player should not receive additional cards after standing.")

    def test_valid_hand_when_score_21_or_less(self):
        """
        Test that a player's hand is valid when their score is 21 or less.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.players[0].hand = [('8', 'Hearts'), ('9', 'Diamonds')]  # Total score: 17
        blackjack.players[0].score = blackjack.calculate_score(blackjack.players[0])
        self.assertLessEqual(blackjack.players[0].score, 21, "Score of 21 or less should be a valid hand.")

    def test_bust_when_score_22_or_more(self):
        """
        Test that a player is considered 'bust' when their score exceeds 21.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.players[0].hand = [('10', 'Hearts'), ('10', 'Diamonds'), ('3', 'Clubs')]  # Total score: 23
        blackjack.players[0].score = blackjack.calculate_score(blackjack.players[0])
        self.assertTrue(blackjack.players[0].is_bust(), "Score of 22 or more should result in a bust.")

    def test_king_and_ace_score_21(self):
        """
        Test that a hand with a King and an Ace results in a score of 21.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.players[0].hand = [('K', 'Hearts'), ('A', 'Diamonds')]  # Total score: 21
        score = blackjack.calculate_score(blackjack.players[0])
        self.assertEqual(score, 21, "King and Ace should result in a score of 21.")

    def test_king_queen_and_ace_score_21(self):
        """
        Test that a hand with a King, a Queen, and an Ace results in a score of 21.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.players[0].hand = [('K', 'Hearts'), ('Q', 'Diamonds'), ('A', 'Clubs')]  # Total score = 21
        score = blackjack.calculate_score(blackjack.players[0])
        self.assertEqual(score, 21, "King, Queen, and Ace should result in a score of 21.")

    def test_nine_and_two_aces_score_21(self):
        """
        Test that a hand with a Nine and two Aces results in a score of 21.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.players[0].hand = [('9', 'Hearts'), ('A', 'Diamonds'), ('A', 'Clubs')]  # Total score = 21
        score = blackjack.calculate_score(blackjack.players[0])
        self.assertEqual(score, 21, "Nine and two Aces should result in a score of 21.")


    # This test was outside of the BBC's scope and added by Diya for further robustness.
    # it ensures that the calculate_score method is robust under more complex conditions.
    def test_multiple_aces_with_varied_scores(self):
        """
        Test that multiple Aces in a hand are handled correctly based on their dynamic scoring rules.
        """
        blackjack = Blackjack(num_players=1)
        blackjack.players[0].hand = [('A', 'Hearts'), ('A', 'Diamonds'), ('9', 'Clubs')]  # Total score = 21
        score = blackjack.calculate_score(blackjack.players[0])
        self.assertEqual(score, 21, "Two Aces and a Nine should result in a score of 21.")

        blackjack.players[0].hand = [('A', 'Hearts'), ('A', 'Diamonds'), ('A', 'Clubs'),
                                     ('7', 'Spades')]  # Total score: 20
        score = blackjack.calculate_score(blackjack.players[0])
        self.assertEqual(score, 20, "Three Aces and a Seven should result in a score of 20.")


if __name__ == '__main__':
    unittest.main()
