from tkinter.constants import CENTER, END, LEFT, RAISED
from PIL import Image, ImageTk
from poker import deal_hole_cards, deal_flop, dealRiver, dealTurn, cards_on_table, deck_builder, book_of_cards, post_flop_odds_calc, check_river_odds_calc, finalScore, reset_cards
from pre_flop_checker import pre_flop_helper
from tkinter import messagebox
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

main_window = tk.Tk()

messagebox.showinfo("Instructions", "The odds have been altered slightly. It is your job to find out which odds are inflated and bet accordingly.")

                                                                                        # user --> the human playing the game.
                                                                                        # player --> the players inside the game holding the two pair of cards.

deck_builder()                                                                          # create a new deck when the program starts.


photo_dict = {
              '0': 'cards/back.png', '14D': 'cards/1_diamond.png', '2D': 'cards/2_diamond.png', '3D': 'cards/3_diamond.png', 
              '4D': 'cards/4_diamond.png', '5D': 'cards/5_diamond.png', '6D': 'cards/6_diamond.png', 
              '7D': 'cards/7_diamond.png', '8D': 'cards/8_diamond.png', '9D': 'cards/9_diamond.png', 
              '10D': 'cards/10_diamond.png', '11D': 'cards/jack_diamond.png', '12D': 'cards/queen_diamond.png', 
              '13D': 'cards/king_diamond.png', '14H': 'cards/1_heart.png', '2H': 'cards/2_heart.png', 
              '3H': 'cards/3_heart.png', '4H': 'cards/4_heart.png', '5H': 'cards/5_heart.png', 
              '6H': 'cards/6_heart.png', '7H': 'cards/7_heart.png', '8H': 'cards/8_heart.png', 
              '9H': 'cards/9_heart.png', '10H': 'cards/10_heart.png', '11H': 'cards/jack_heart.png', 
              '12H': 'cards/queen_heart.png', '13H': 'cards/king_heart.png', '14C': 'cards/1_club.png', 
              '2C': 'cards/2_club.png', '3C': 'cards/3_club.png', '4C': 'cards/4_club.png', '5C': 'cards/5_club.png', 
              '6C': 'cards/6_club.png', '7C': 'cards/7_club.png', '8C': 'cards/8_club.png', '9C': 'cards/9_club.png', '10C': 'cards/10_club.png', '11C': 'cards/jack_club.png', '12C': 'cards/queen_club.png', '13C': 'cards/king_club.png', '14S': 'cards/1_spade.png', '2S': 'cards/2_spade.png', '3S': 'cards/3_spade.png', '4S': 'cards/4_spade.png', '5S': 'cards/5_spade.png', '6S': 'cards/6_spade.png', '7S': 'cards/7_spade.png', '8S': 'cards/8_spade.png', '9S': 'cards/9_spade.png', '10S': 'cards/10_spade.png', '11S': 'cards/jack_spade.png', '12S': 'cards/queen_spade.png', '13S': 'cards/king_spade.png'
              }                                                                            #this dictionary stores the locations for the cards as values and 
                                                                                           #the card number and suite as key


back_image = ImageTk.PhotoImage(Image.open(resource_path(photo_dict['0']))) # the upside down card


class Play():
    def __init__(self):
        self.betting_round = "Pre-Hole Cards"                                           #the current round of betting. Initialized to "Pre-Hole Cards"
        self.heading = tk.Label(main_window, text="Betting Round: {}".format(self.betting_round), justify=CENTER) 
        self.heading.grid(row=0, column=5, columnspan=3)
        self.images = [back_image, back_image, back_image, back_image, back_image]      #initialize the cards on table to 5 upside down cards
        self.player_cards = [[back_image, back_image], [back_image, back_image]]        #initialize the players' cards to upside down cards
        self.balance = 1000                                                             #initial balance set to 1000
        self.display_balance()
        self.starting_balance = self.balance                                            #starting balance is used to store the initial balance at the start of the hand. 
                                                                                        #this variable is called when calculating the net gain/loss in a single round
        self.amount_on_p1 = []
        self.amount_on_tie = []                                                         #the list stores the amount that a player bet and the odds they bet on at each round
        self.amount_on_p2 = []          
        self.odds_p1, self.odds_p2, self.odds_tie = 1, 1, 50   
        self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)                                             
        self.warning = tk.Label(main_window, text="", bg="gray")                        #warning label is called when the players bet in excess of what they have
        self.warning.grid(row=7, column=5, columnspan=2)                                
        self.hole_cards = []                                                            #the players' 2 cards. Initialized to null values
        self.add_post_flop_photos()                                                     #initialized cards to upside down photos
        self.add_pre_flop_photos()
        self.display_bet_entry_boxes()                                                  #show the bet boxes to the players
        self.add_bet_buttons()


    def display_balance(self):
        """This function displays the balance on to the screen.
        """
        self.player_balance = tk.Label(main_window, text="Current balance is {} coins".format(round(self.balance, 1)), fg='green', wraplength=180, justify=CENTER)
        self.player_balance.grid(row=0, column=9)


    def update_heading(self):
        """This function is called at each round. It updates the heading label to the current round.
        """
        if self.betting_round == "All cards dealt. Press Start Again to play new game.":
            self.heading.grid_forget()
            self.heading = tk.Label(main_window, text="Betting Round: {}".format(self.betting_round), justify=CENTER, fg="#2fc52f", bg="#05056d")
            self.heading.grid(row=0, column=5, columnspan=3)
        else:
            self.heading.grid_forget()
            self.heading = tk.Label(main_window, text="Betting Round: {}".format(self.betting_round), justify=CENTER)
            self.heading.grid(row=0, column=5, columnspan=3)


    def refill_coins(self):
        """This function resets the class' balance instance to 1000 coins.
        """
        self.balance = 1000
        self.player_balance.grid_forget()
        self.display_balance()
        self.start_new_game()
        self.refill_coins_btn.grid_forget()


    def bet(self):
        """
        :The function is run when the players click the bet button in the window. The variable 
        :amount is updated with the amount the users input into the entry boxes. After 
        :checking if the balance is positive and less than the user's current balance (if 
        :the condition is not satisifed, the else condition is called and a warning Label is 
        :displayed on the screen), the function updates the player's bet balance at each round. 
        :The deal_next_round() function is called. The bet entry boxes are initialized.
        """
        amount = 0
        amount += int(self.p1_bet.get()) + int(self.p2_bet.get()) + int(self.tie_bet.get())
        if amount <= self.balance and amount >= 0:
            self.warning.grid_forget()
            self.amount_on_p1.append([int(self.p1_bet.get()), self.odds_p1])
            self.amount_on_tie.append([int(self.tie_bet.get()), self.odds_tie])
            self.amount_on_p2.append([int(self.p2_bet.get()), self.odds_p2])
            self.balance -= amount
            self.player_balance.grid_forget()
            self.display_balance()
            self.forget_last_odds()
            self.deal_next_round()
        else:
            self.warning = tk.Label(main_window, text="Your current bet amount exceeds your remaining balance or your bet amount is negative")
            self.warning.grid(row=7, column=3, columnspan=6)
        self.initialize_bet_entry_boxes()


    def start_new_game(self):
        """This function resets all values to default. The function is called when the user 
        :presses the deal new hand at the end of each round."""
        self.betting_round = "Pre-Flop"
        self.update_heading()
        self.starting_balance = self.balance
        self.amount_on_p1 = []
        self.amount_on_tie = []
        self.amount_on_p2 = []
        self.hole_cards = []
        reset_cards()
        self.warning.grid_forget()
        self.warning = tk.Label(main_window, text="", bg="gray")
        self.warning.grid(row=7, column=5, columnspan=2)
        self.forget_last_odds()
        self.odds_p1, self.odds_p2, self.odds_tie = 1, 1, 0
        self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
        self.final_score.grid_forget()
        self.initialize_hole_cards_pics()
        self.initialize_cards_on_table()
        self.add_bet_buttons()
        self.start_again_button.grid_forget()
        self.refill_coins_btn.grid_forget()


    def deal_next_round(self):
        """This function is called when the bet button is clicked. The function checks the number of cards in the deck.
        : If 52, it deals the Hole cards. If 48, it deals the flop etc. When the river (last card) is dealt, this function
        calculates the total winnings or loss in the game."""
        if len(book_of_cards) == 52:
            self.betting_round = "Pre-Flop"
            self.update_heading()
            self.hole_cards = deal_hole_cards(2)
            self.odds_p1, self.odds_p2 = pre_flop_helper(self.hole_cards)
            self.odds_tie = 0
            self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
            self.add_pre_flop_photos()
        elif len(book_of_cards) == 48:
            self.betting_round = "Post-Flop"
            self.update_heading()
            deal_flop()
            self.odds_p1, self.odds_p2, self.odds_tie = post_flop_odds_calc(self.hole_cards)
            self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
        elif len(book_of_cards) == 45:
            self.betting_round = "Turn"
            self.update_heading()
            dealTurn()
            self.odds_p1, self.odds_p2, self.odds_tie = check_river_odds_calc()
            self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
        elif len(book_of_cards) == 44:
            self.betting_round = "All cards dealt. Press Start Again to play new game."
            self.update_heading()
            turn = dealRiver() 
            result, card_rank = finalScore()
            net_win = 0
            if result == "Player 1 Wins":
                for i in range(4):
                    net_win += self.amount_on_p1[i][0] * (1+self.amount_on_p1[i][1])
            elif result == "Player 2 Wins":
                for i in range(4):
                    net_win += self.amount_on_p2[i][0] * (1+self.amount_on_p2[i][1])
            else:
                for i in range(4):
                    net_win += self.amount_on_tie[i][0] * (1+self.amount_on_tie[i][1])
            self.balance = self.balance + net_win
            self.player_balance.grid_forget()
            self.display_balance()
            winning_on_this_game = self.balance - self.starting_balance
            self.display_final_score(result, winning_on_this_game, card_rank)
            self.hide_bet_buttons()
        self.add_post_flop_photos()


    def display_odds(self, odds_p1, odds_p2, odds_tie=0):
        """
        This function takes in each players' odds of winning the hand at each step of the game
        :and displays it in the screen.
        : type input: floats
        """
        self.odds_p1_win = tk.Label(main_window, text="P1 odds = 1 to {}".format(str(round(odds_p1, 2))), bg="#9a9898", fg="#222dca")
        self.odds_p1_win.grid(row=4, column=2, columnspan=2)
        self.odds_p2_win = tk.Label(main_window, text="P2 odds = 1 to {}".format(str(round(odds_p2,2))), bg="#9a9898", fg="#222dca")
        self.odds_p2_win.grid(row=4, column=8, columnspan=2)
        self.odds_p1_p2_tie = tk.Label(main_window, text="Odds of tie = 1 to {}".format(str(round(odds_tie,2))), justify=CENTER, bg="#9a9898", fg="#222dca")
        self.odds_p1_p2_tie.grid(row=4, column=5, columnspan=2)


    def forget_last_odds(self):
        """This function removes the last odd from the screen. The function is called when a new game is started."""
        self.odds_p1_win.grid_forget()
        self.odds_p2_win.grid_forget()
        self.odds_p1_p2_tie.grid_forget()


    def display_bet_entry_boxes(self):
        """This function displays the entry boxes with 0 as default value."""
        self.p1_bet = tk.Entry(main_window, width=5, relief=RAISED, justify=CENTER)
        self.p1_bet.insert(0, "0")
        self.p1_bet.grid(row=5, column=2, columnspan=2)
        self.p2_bet = tk.Entry(main_window, width=5, relief=RAISED, justify=CENTER)
        self.p2_bet.insert(0, "0")
        self.p2_bet.grid(row=5, column=8, columnspan=2)
        self.tie_bet = tk.Entry(main_window, width=5, relief=RAISED, justify=CENTER)
        self.tie_bet.insert(0, "0")
        self.tie_bet.grid(row=5, column=5, columnspan=2)


    def initialize_bet_entry_boxes(self):
        """This function clears the value from the bet entry boxes and inserts a 0 in its place."""
        self.p1_bet.delete(0, END)
        self.p1_bet.insert(0, "0")
        self.p2_bet.delete(0, END)
        self.p2_bet.insert(0, "0")
        self.tie_bet.delete(0, END)
        self.tie_bet.insert(0, "0")


    def display_final_score(self, result, winning_on_this_game, card_rank):
        """This function displays the final score in the following pattern - the player who 
        :wins (e.g. Player 1 or Player 2), the rank of the card (e.g. Highcard or Flush) and
        :the amount that was won in this round.
        :type result: string
        :type winning_on_this_game: float
        :type card_rank: string
        """
        if winning_on_this_game > 0:
            winning_in_round = "You made $$$ {}".format(round(winning_on_this_game, 1))
            text_color = "green"
        elif winning_on_this_game < 0:
            winning_in_round = "You lost $$$ {}".format(round(winning_on_this_game*-1, 1))
            text_color = "red"
        else:
            winning_in_round = "You didn't make any $$$ this round"
            text_color = "white"
        self.final_score = tk.Label(main_window, text="{} with a {}. {}".format(result, card_rank, winning_in_round), justify=CENTER, fg="#2fc52f", bg="#05056d")
        self.final_score.grid(row=2, column=3, columnspan=7)
        self.odds_p1_win.grid_forget()
        self.odds_p2_win.grid_forget()
        self.odds_p1_p2_tie.grid_forget()


    def initialize_hole_cards_pics(self):
        """This function initializes the cards that are with the players with 2 pairs of upside down cards."""
        self.player_cards = [[back_image, back_image], [back_image, back_image]]
        self.p1_card1.grid_forget()
        self.p1_card2.grid_forget()
        self.p2_card1.grid_forget()
        self.p2_card2.grid_forget()
        self.add_pre_flop_photos()


    def add_pre_flop_photos(self):
        """This function displays the  pair of cards that the players are dealt.
        """
        if len(self.hole_cards) == 2:
            for i in range(2):
                for j in range(2):
                    self.player_cards[i][j] = ImageTk.PhotoImage(Image.open(photo_dict[self.hole_cards[i][j]]))
        self.p1_card1 = tk.Label(main_window, image=self.player_cards[0][0])
        self.p1_card1.grid(row=3, column=2)
        self.p1_card2 = tk.Label(main_window, image=self.player_cards[0][1])
        self.p1_card2.grid(row=3, column=3)
        self.p2_card1 = tk.Label(main_window, image=self.player_cards[1][0])
        self.p2_card1.grid(row=3, column=8)
        self.p2_card2 = tk.Label(main_window, image=self.player_cards[1][1])
        self.p2_card2.grid(row=3, column=9)


    def initialize_cards_on_table(self):
        """This function initializes the cards that are on the table with 5 upside down cards
        """
        self.images = [back_image, back_image, back_image, back_image, back_image]
        self.card1.grid_forget()
        self.card2.grid_forget()
        self.card3.grid_forget()
        self.card4.grid_forget()
        self.card5.grid_forget()
        self.add_post_flop_photos()


    def add_post_flop_photos(self):
        """This function displays the cards that have been displayed on the table."""
        for i in range(len(cards_on_table)):
            self.images[i] = ImageTk.PhotoImage(Image.open(photo_dict[cards_on_table[i]]))
        self.card1 = tk.Label(main_window, image=self.images[0])
        self.card1.grid(row=1, column=4)
        self.card2 = tk.Label(main_window, image=self.images[1])
        self.card2.grid(row=1, column=5)
        self.card3 = tk.Label(main_window, image=self.images[2])
        self.card3.grid(row=1, column=6)
        self.card4 = tk.Label(main_window, image=self.images[3])
        self.card4.grid(row=1, column=7)
        self.card5 = tk.Label(main_window, image=self.images[4])
        self.card5.grid(row=1, column=8)


    def add_bet_buttons(self):
        """This function displays the bet buttons"""
        self.p1_bet_btn = tk.Button(main_window, text="Bet", justify=CENTER, padx=10, pady=3, command=self.bet)
        self.p1_bet_btn.grid(row=6, column=2, columnspan=2)
        self.p2_bet_btn = tk.Button(main_window, text="Bet", justify=CENTER, padx=10, pady=3, command=self.bet)
        self.p2_bet_btn.grid(row=6, column=8, columnspan=2)
        self.tie_bet_btn = tk.Button(main_window, text="Bet", justify=CENTER, padx=10, pady=3, command=self.bet)
        self.tie_bet_btn.grid(row=6, column=5, columnspan=2)


    def hide_bet_buttons(self):
        """This funciton hides the bet buttons after the final round of betting"""
        self.p1_bet_btn.grid_forget()
        self.p2_bet_btn.grid_forget()
        self.tie_bet_btn.grid_forget()
        self.start_again_button = tk.Button(main_window, text="Deal next hand", justify=CENTER, padx=10, pady=3, command=self.start_new_game)
        self.start_again_button.grid(row=9, column=9, columnspan=2)
        self.refill_coins_btn = tk.Button(main_window, text="Go back to 1000 coins", justify=CENTER, padx=10, pady=3, command=self.refill_coins)
        self.refill_coins_btn.grid(row=9, column=7, columnspan=3)

main_window.title("PokerBets")
main_window.geometry("1350x720")
main_window.configure(bg="gray")

main_window.columnconfigure(0, weight=2)
main_window.columnconfigure(1, weight=5)
main_window.columnconfigure(2, weight=5)
main_window.columnconfigure(3, weight=5)
main_window.columnconfigure(4, weight=5)
main_window.columnconfigure(5, weight=5)
main_window.columnconfigure(6, weight=5)
main_window.columnconfigure(7, weight=5)
main_window.columnconfigure(8, weight=5)
main_window.columnconfigure(9, weight=5)
main_window.columnconfigure(10, weight=2)

main_window.rowconfigure(0, weight=2)
main_window.rowconfigure(1, weight=7)
main_window.rowconfigure(2, weight=2)
main_window.rowconfigure(3, weight=5)
main_window.rowconfigure(4, weight=2)
main_window.rowconfigure(5, weight=2)
main_window.rowconfigure(6, weight=2)
main_window.rowconfigure(7, weight=2)
main_window.rowconfigure(8, weight=2)
main_window.rowconfigure(9, weight=2)
main_window.rowconfigure(10, weight=2)
main_window.rowconfigure(11, weight=2)
main_window.rowconfigure(12, weight=2)
main_window.rowconfigure(13, weight=2)


p1 = tk.Label(main_window, text="Player 1: Phil Ivey", fg='black', bg="gray", wraplength=130, justify=CENTER).grid(row=2, column=2, columnspan=2)
p2 = tk.Label(main_window, text="Player 2: Daniel Negreanu", fg='yellow', bg="gray", justify=CENTER).grid(row=2, column=8, columnspan=2)


player = Play()#calls the Play class to initalize the game.

main_window.mainloop()