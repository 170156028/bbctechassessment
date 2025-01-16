from src.deck import Deck
from src.player import Player
from src.dealer import Dealer
from tkinter import *
from PIL import ImageTk, Image
import random





class Blackjack:
    # Initialises the Blackjack game.
    def __init__(self, num_players=1):
        self.deck = Deck() # Create a deck of cards.
        # Create players and assign them to the game. Each player gets a number
        self.players = [Player(deck=self.deck, player_number=player_number + 1) for player_number in range(num_players)]  # List of hands for each player
        self.dealer = Dealer(deck=self.deck)  # The dealer uses the same deck.
        self.current_player_index = 0  # Tracks whose turn it is

    def deal_hand(self):
        # Deal two cards to each player
        for player in self.players:
            player.init_draw_cards()
        # Deal two cards to the dealer
        self.dealer.init_draw_cards()

    def calculate_score(self, player):
        # Assign numeric values to cards. Aces are initially valued at 1
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10,
                  'A': 1}
        # Calculate the total score for the player's hand.
        score = sum(values[str(card[0])] for card in player.hand)

        # Count the number of Aces in the player's hand.
        num_aces = sum(1 for card in player.hand if card[0] == 'A')
        # Adjust Ace values to 11 where possible without causing a bust.
        while num_aces > 0 and score + 10 <= 21:
            score += 10
            num_aces -= 1
        # Update the player's score attribute.
        player.score = score
        return player.score

    def hit(self): # Handle the logic for when a player chooses to "hit".
        current_player = self.players[self.current_player_index] # Logic to draw a card for the player is shown here
        current_player.hit()
        # Recalculate and return the updated score for the player.
        return self.calculate_score(current_player)
    def hit_action(self):
        # Perform the hit action for the current player.
        score = self.hit()
        # Update the GUI to reflect the current player's updated hand and score
        self.update_player_display()
        # If the player's score exceeds 21, they bust, and it's the next player's turn.
        if self.is_bust(self.current_player_index):  # Player busts
            self.player_hand_label.config(text=f"Player {self.current_player_index + 1}: Bust!")
            self.next_player()

    def stand_action(self):
        # Move to the next player without drawing additional cards.
        self.next_player()

    def next_player(self):
        self.current_player_index += 1 # Advance to the next player.
        if self.current_player_index >= len(self.players):  # All players have taken their turn
            self.current_player_index = 0  # Reset for the next round (if needed)
            self.dealer_turn()  # Proceed to the dealer's turn
        else:
            self.update_player_display()  # Update display for the next player

    def dealer_turn(self):
        dealer_score = self.calculate_score(self.dealer) # Calculate the dealer's initial score.
        # Dealer must hit until their score reaches at least 17 or higher
        while dealer_score < 17:
            self.dealer.hit()
            dealer_score = self.calculate_score(self.dealer)

        # Add a small chance for the dealer to draw again at 17-19 to introduce risk
        if 17 <= dealer_score <= 19 and random.random() < 0.5:
            self.dealer.hit()
            dealer_score = self.calculate_score(self.dealer)
        # Determine the winners of the game after the dealer's turn ends.
        self.determine_winners(self.players, dealer_score)



    def determine_winners(self, players, dealer_score):
        results = [] # List to store the results of the game.
        self.update_dealer_hand_display(reveal=True) # Reveal the dealer's full hand

        # Separate players into non-busted and busted
        non_bust_players = [player for player in players if not player.is_bust()]
        busted_players = [player for player in players if player.is_bust()]

        # Handle busted players
        for busted_player in busted_players:
            results.append(f"Player {busted_player.player_number} busts and loses, Score {busted_player.score}")

        # Handle what to do if dealer busts
        if self.dealer.is_bust():
            results.append(f"Dealer busts, Score {self.dealer.score}")

        else:
            # Dealer did not bust; so evaluate against non-busted players
            max_score = max(player.score for player in non_bust_players) if non_bust_players else 0
            max_score_players = [player for player in non_bust_players if player.score == max_score]
            looser_players = [player for player in non_bust_players if player not in max_score_players]

            # This part checks if dealer wins, ties, or loses
            for max_score_player in max_score_players:
                if max_score_player.score > dealer_score:
                    results.append(f"Player {max_score_player.player_number} Wins, Score {max_score_player.score}")
                    results.append(f"Dealer loses, Score {self.dealer.score}")
                elif max_score_player.score == dealer_score:
                    results.append(
                        f"Player {max_score_player.player_number} and Dealer tie, Score {max_score_player.score}")
                else:
                    results.append(f"Player {max_score_player.player_number} loses, Score {max_score_player.score}")
                    results.append(f"Dealer wins, Score {self.dealer.score}")

            # This handles other non-busted players who didn't achieve max score
            for looser_player in looser_players:
                results.append(f"Player {looser_player.player_number} loses, Score {looser_player.score}")

        # Updates the GUI results message
        self.player_hand_label.config(text="\n".join(results))

        # End the game by disabling buttons and locks the state
        self.end_game()



    def update_player_display(self):
        current_player = self.players[self.current_player_index] # Get the current player.
        score = self.calculate_score(current_player)  # Calculate the player's score.

        # Updates the label to reflect the current player's hand
        self.player_hand_label.config(
            text=f"Player {self.current_player_index + 1}'s hand: {current_player.hand}, Score: {score}"
        )

        # Clears the player's hand display with card images
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()

        for card in current_player.hand:
            card_image = self.get_card_image(card) # Load the image for each card.
            card_label = Label(self.player_hand_frame, image=card_image, bg="green")
            card_label.image = card_image  # Keep a reference to avoid garbage collection
            card_label.pack(side=LEFT, padx=5)


    # Update the dealer's hand display, optionally hiding one card.
    def update_dealer_hand_display(self, reveal=False):
        # Clear the dealer's hand frame to avoid overlapping card images
        for widget in self.dealer_hand_frame.winfo_children():
            widget.destroy()
        # Loop through each card in the dealer's hand
        for i, card in enumerate(self.dealer.hand):
            # If reveal is False, hide the first card (simulate face-down card)
            if i == 0 and not reveal:  # Hide the first card if reveal is False
                card_image = ImageTk.PhotoImage(Image.open("./src/Classic/card_back.png").resize((100, 150)))
            else:
                # Otherwise, show the actual card
                card_image = self.get_card_image(card)
            # Display the card image in the dealer's hand frame
            card_label = Label(self.dealer_hand_frame, image=card_image, bg="green")
            card_label.image = card_image # Retain a reference to prevent garbage collection
            card_label.pack(side=LEFT, padx=5)

    def end_game(self):
        # Disable buttons at the end of the game
        for widget in self.game_screen.winfo_children():
            if isinstance(widget, Button):
                widget.config(state=DISABLED)

    def is_bust(self, current_player_index):
        # Check if the player's score exceeds 21 (bust)
        return self.players[current_player_index].is_bust()

    def start_game(self, win):
        win.destroy()  # Close the welcome screen

        # Create the main game screen
        self.game_screen = Tk()
        self.game_screen.title("Diya's Multiplayer Blackjack Game!")
        self.game_screen.geometry("1080x720")
        self.game_screen.configure(bg="green")  # Green background for the game screen

        # Deal initial hands for all players and dealer
        self.deal_hand()

        # Frame for player's hand
        self.player_hand_frame = Frame(self.game_screen, bg="green")
        self.player_hand_frame.place(relx=0.5, rely=0.6, anchor=CENTER)

        # Frame for dealer's hand
        self.dealer_hand_frame = Frame(self.game_screen, bg="green")
        self.dealer_hand_frame.place(relx=0.5, rely=0.3, anchor=CENTER)

        # Label for the current player's hand (placeholder)
        self.player_hand_label = Label(
            self.game_screen,
            text="",  # Will be updated dynamically by `update_player_display`
            font=("Arial", 16),
            bg="red",
            fg="white",
        )
        self.player_hand_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Hit button for drawing another card
        hit_button = Button(
            self.game_screen,
            text="Hit",
            font=("Arial", 16),
            bg="white",
            fg="black",
            command=self.hit_action,  # Call hit_action when clicked
        )
        hit_button.place(relx=0.4, rely=0.8, anchor=CENTER)

        # Stand button for ending a player's turn
        stand_button = Button(
            self.game_screen,
            text="Stand",
            font=("Arial", 16),
            bg="white",
            fg="black",
            command=self.stand_action,  # Call stand_action when clicked
        )
        stand_button.place(relx=0.6, rely=0.8, anchor=CENTER)

        # Display Player 1's hand immediately
        self.update_player_display()

        # Run the main event loop for the game screen
        self.game_screen.mainloop()



    def get_card_image(self, card):
        # Load the image for a given card.
        rank, suit = card

        # Map face card abbreviations to full names
        rank_map = {
            "J": "jack",
            "Q": "queen",
            "K": "king",
            "A": "ace"
        }

        # Use the mapped name if it's a face card, otherwise use the rank as is
        rank_str = rank_map.get(str(rank), str(rank).lower())

        # Generate the card image file name
        card_name = f"{rank_str}_of_{suit.lower()}.png"
        card_path = f"./src/Classic/{card_name}"

        # Debugging output to verify the path
        print(f"Loading card image from: {card_path}")

        # Load and resize the image
        try:
            return ImageTk.PhotoImage(Image.open(card_path).resize((100, 150)))  # Resize as needed
        except FileNotFoundError:
            # If the file is missing, log an error and raise an exception
            print(f"Error: File not found - {card_path}")
            raise

    def play(self):
        # Display the welcome screen with a background image.
        win = Tk()
        win.title("Welcome to Diya's Blackjack Game! :)")
        win.geometry("1080x720") # Set the window size

        # Load and set the background image
        blackjack_img = "./src/blackjackbackgroundimage.webp"
        bg = ImageTk.PhotoImage(Image.open(blackjack_img).resize((1080, 720)))
        bg_label = Label(win, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

        # Welcome message (on top of the background)
        welcome_message = Label(
            win,
            text="Welcome to Diya's Blackjack Game! :)", # text itself
            font=("Arial", 24, "bold"), # text font
            bg="red",  # Background for the text box
            fg="white",  # Text colour
        )
        welcome_message.place(relx=0.5, rely=0.3, anchor=CENTER) # Centre the label

        # Play button to start game
        play_button = Button(
            win,
            text="Play",
            font=("Arial", 20, "bold"),
            bg="red", # button background colour
            fg="white", # button text colour
            command=lambda: self.start_game(win),  # Pass the current window to destroy it and on to game logic
        )
        play_button.place(relx=0.5, rely=0.5, anchor=CENTER) # Centre the button
        # Start the main event loop for the welcome screen
        win.mainloop()



if __name__ == '__main__':
    num_players = 2  # Example: 2 players
    blackjack = Blackjack(num_players)
    blackjack.play()

