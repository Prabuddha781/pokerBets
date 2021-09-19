from tkinter import PhotoImage
from tkinter.constants import CENTER, END, LEFT, RAISED
from PIL import Image, ImageTk
from poker import dealHoleCards, dealFlop, dealRiver, dealTurn, cardsOnTable, deckBuilder, bookOfCards, postFlopOddsCalc, checkRiverOddsCalc, finalScore, reset_cards
from preFlopChecker import preFlopHelper
from tkinter import messagebox

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

mainWindow = tk.Tk()

messagebox.showinfo("Instructions", "The odds have been altered slightly. It is your job to find out which odds are inflated and bet accordingly.")

deckBuilder()

photoDict = {'0': 'cards/back.png', '14D': 'cards/1_diamond.png', '2D': 'cards/2_diamond.png', '3D': 'cards/3_diamond.png', 
'4D': 'cards/4_diamond.png', '5D': 'cards/5_diamond.png', '6D': 'cards/6_diamond.png', 
'7D': 'cards/7_diamond.png', '8D': 'cards/8_diamond.png', '9D': 'cards/9_diamond.png', 
'10D': 'cards/10_diamond.png', '11D': 'cards/jack_diamond.png', '12D': 'cards/queen_diamond.png', 
'13D': 'cards/king_diamond.png', '14H': 'cards/1_heart.png', '2H': 'cards/2_heart.png', 
'3H': 'cards/3_heart.png', '4H': 'cards/4_heart.png', '5H': 'cards/5_heart.png', 
'6H': 'cards/6_heart.png', '7H': 'cards/7_heart.png', '8H': 'cards/8_heart.png', 
'9H': 'cards/9_heart.png', '10H': 'cards/10_heart.png', '11H': 'cards/jack_heart.png', 
'12H': 'cards/queen_heart.png', '13H': 'cards/king_heart.png', '14C': 'cards/1_club.png', 
'2C': 'cards/2_club.png', '3C': 'cards/3_club.png', '4C': 'cards/4_club.png', '5C': 'cards/5_club.png', 
'6C': 'cards/6_club.png', '7C': 'cards/7_club.png', '8C': 'cards/8_club.png', '9C': 'cards/9_club.png', '10C': 'cards/10_club.png', '11C': 'cards/jack_club.png', '12C': 'cards/queen_club.png', '13C': 'cards/king_club.png', '14S': 'cards/1_spade.png', '2S': 'cards/2_spade.png', '3S': 'cards/3_spade.png', '4S': 'cards/4_spade.png', '5S': 'cards/5_spade.png', '6S': 'cards/6_spade.png', '7S': 'cards/7_spade.png', '8S': 'cards/8_spade.png', '9S': 'cards/9_spade.png', '10S': 'cards/10_spade.png', '11S': 'cards/jack_spade.png', '12S': 'cards/queen_spade.png', '13S': 'cards/king_spade.png'}

backImage = ImageTk.PhotoImage(Image.open(photoDict['0']))


class PlayerBalance():
    def __init__(self):
        self.betting_round = "Pre-Hole Cards"
        self.heading = tk.Label(mainWindow, text="Betting Round: {}".format(self.betting_round), justify=CENTER)
        self.heading.grid(row=0, column=5, columnspan=3)
        self.images = [backImage, backImage, backImage, backImage, backImage]
        self.cards = [[backImage, backImage], [backImage, backImage]]
        self.balance = 1000
        self.display_balance()
        self.starting_balance = self.balance
        self.amount_on_p1 = []
        self.amount_on_tie = []
        self.amount_on_p2 = []
        self.warning = tk.Label(mainWindow, text="", bg="gray")
        self.warning.grid(row=7, column=5, columnspan=2)
        self.hole_cards = []
        self.odds_p1, self.odds_p2, self.odds_tie = 1, 1, 0
        self.add_post_flop_photos()
        self.add_photos()
        self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
        self.display_bet_entry_boxes()

    def display_balance(self):
        self.player_balance = tk.Label(mainWindow, text="Current balance is {} coins".format(self.balance), fg='green', wraplength=180, justify=CENTER)
        self.player_balance.grid(row=0, column=9)

    def update_heading(self):
        if self.betting_round == "All cards dealt. Press Start Again to play new game.":
            self.heading.grid_forget()
            self.heading = tk.Label(mainWindow, text="Betting Round: {}".format(self.betting_round), justify=CENTER, fg="#2fc52f", bg="#05056d")
            self.heading.grid(row=0, column=5, columnspan=3)
        else:
            self.heading.grid_forget()
            self.heading = tk.Label(mainWindow, text="Betting Round: {}".format(self.betting_round), justify=CENTER)
            self.heading.grid(row=0, column=5, columnspan=3)

    def bet(self):
        amount = 0
        amount += int(self.p1_bet.get()) + int(self.p2_bet.get()) + int(self.tie_bet.get())
        if amount <= self.balance:
            self.warning.grid_forget()
            self.amount_on_p1.append([int(self.p1_bet.get()), self.odds_p1])
            self.amount_on_tie.append([int(self.tie_bet.get()), self.odds_p2])
            self.amount_on_p2.append([int(self.p2_bet.get()), self.odds_tie])
            self.balance -= amount
            self.player_balance.grid_forget()
            self.display_balance()
            self.forget_last_odds()
            self.deal_next_round()
        else:
            self.warning = tk.Label(mainWindow, text="Your current bet amount exceeds your remaining balance")
            self.warning.grid(row=7, column=5, columnspan=2)
        self.initialize_bet_entry_boxes()
        print(self.amount_on_p1)
        print(self.amount_on_p2)
        print(self.amount_on_tie)

    def start_new_game(self):
        self.starting_balance = self.balance
        self.amount_on_p1 = []
        self.amount_on_tie = []
        self.amount_on_p2 = []
        self.hole_cards = []
        reset_cards()
        self.warning = tk.Label(mainWindow, text="", bg="gray")
        self.warning.grid(row=7, column=5, columnspan=2)
        self.forget_last_odds()
        self.odds_p1, self.odds_p2, self.odds_tie = 1, 1, 0
        self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
        self.final_score.grid_forget()
        self.initialize_hole_cards_pics()
        self.initialize_cards_on_table()

    def deal_next_round(self):
        if len(bookOfCards) == 52:
            self.betting_round = "Pre-Flop"
            self.update_heading()
            self.hole_cards = dealHoleCards(2)
            self.odds_p1, self.odds_p2 = preFlopHelper(self.hole_cards)
            self.odds_tie = 0
            self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
            self.add_photos()
        elif len(bookOfCards) == 48:
            self.betting_round = "Post-Flop"
            self.update_heading()
            dealFlop()
            self.odds_p1, self.odds_p2, self.odds_tie = postFlopOddsCalc(self.hole_cards)
            self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
        elif len(bookOfCards) == 45:
            self.betting_round = "Turn"
            self.update_heading()
            dealTurn()
            self.odds_p1, self.odds_p2, self.odds_tie = checkRiverOddsCalc()
            self.display_odds(self.odds_p1, self.odds_p2, self.odds_tie)
        elif len(bookOfCards) == 44:
            self.betting_round = "All cards dealt. Press Start Again to play new game."
            self.update_heading()
            turn = dealRiver() 
            result = finalScore()
            global net_win
            global net_loss
            net_win = 0
            net_loss = 0
            # check these three lines again
            amount_bet_on_p1 = self.amount_on_p1
            amount_bet_on_p2 = self.amount_on_p2
            amount_bet_on_tie = self.amount_on_tie
            if result == "Player 1 Wins":
                for i in range(4):
                    net_win += amount_bet_on_p1[i][0] * (1+amount_bet_on_p1[i][1])
            elif result == "Player 2 Wins":
                for i in range(4):
                    net_win += amount_bet_on_p2[i][0] * (1+amount_bet_on_p2[i][1])
            else:
                for i in range(4):
                    net_win += amount_bet_on_tie[i][0] * (1+amount_bet_on_tie[i][1])
            self.balance = self.balance + net_win
            self.player_balance.grid_forget()
            self.display_balance()
            winning_on_this_game = self.balance - self.starting_balance
            self.display_final_score(result, winning_on_this_game)
        self.add_post_flop_photos()

    def display_odds(self, odds_p1, odds_p2, odds_tie=0):
        self.odds_p1_win = tk.Label(mainWindow, text="P1 odds = 1 to {}".format(str(round(odds_p1, 2))), bg="#9a9898", fg="#222dca")
        self.odds_p1_win.grid(row=4, column=2, columnspan=2)
        self.odds_p2_win = tk.Label(mainWindow, text="P2 odds = 1 to {}".format(str(round(odds_p2,2))), bg="#9a9898", fg="#222dca")
        self.odds_p2_win.grid(row=4, column=8, columnspan=2)
        self.odds_p1_p2_tie = tk.Label(mainWindow, text="Odds of tie = 1 to {}".format(str(round(odds_tie,2))), justify=CENTER, bg="#9a9898", fg="#222dca")
        self.odds_p1_p2_tie.grid(row=4, column=5, columnspan=2)

    def forget_last_odds(self):
        self.odds_p1_win.grid_forget()
        self.odds_p2_win.grid_forget()
        self.odds_p1_p2_tie.grid_forget()

    def display_bet_entry_boxes(self):
        self.p1_bet = tk.Entry(mainWindow, width=5, relief=RAISED, justify=CENTER)
        self.p1_bet.insert(0, "0")
        self.p1_bet.grid(row=5, column=2, columnspan=2)
        self.p2_bet = tk.Entry(mainWindow, width=5, relief=RAISED, justify=CENTER)
        self.p2_bet.insert(0, "0")
        self.p2_bet.grid(row=5, column=8, columnspan=2)
        self.tie_bet = tk.Entry(mainWindow, width=5, relief=RAISED, justify=CENTER)
        self.tie_bet.insert(0, "0")
        self.tie_bet.grid(row=5, column=5, columnspan=2)

    def initialize_bet_entry_boxes(self):
        self.p1_bet.delete(0, END)
        self.p1_bet.insert(0, "0")
        self.p2_bet.delete(0, END)
        self.p2_bet.insert(0, "0")
        self.tie_bet.delete(0, END)
        self.tie_bet.insert(0, "0")

    def display_final_score(self, result, winning_on_this_game):
        if winning_on_this_game > 0:
            winning_in_round = "You made $$$ {}".format(winning_on_this_game)
            text_color = "green"
            wrap_length = 210
        elif winning_on_this_game < 0:
            winning_in_round = "You lost $$$ {}".format(winning_on_this_game*-1)
            text_color = "red"
            wrap_length = 210
        else:
            winning_in_round = "You didn't make any $$$ this round"
            text_color = "white"
            wrap_length = 110
        self.final_score = tk.Label(mainWindow, text="{}.{}".format(result, winning_in_round), bg="#9a9898", fg=text_color, font=("Helvetica", 22))
        self.final_score.grid(row=2, column=3, columnspan=7)
        self.odds_p1_win.grid_forget()
        self.odds_p2_win.grid_forget()
        self.odds_p1_p2_tie.grid_forget()

    def initialize_hole_cards_pics(self):
        self.cards = [[backImage, backImage], [backImage, backImage]]
        self.p1_card1.grid_forget()
        self.p1_card2.grid_forget()
        self.p2_card1.grid_forget()
        self.p2_card2.grid_forget()
        self.add_photos()

    def add_photos(self):
        if len(self.hole_cards) == 2:
            for i in range(2):
                for j in range(2):
                    self.cards[i][j] = ImageTk.PhotoImage(Image.open(photoDict[self.hole_cards[i][j]]))
        self.p1_card1 = tk.Label(mainWindow, image=self.cards[0][0])
        self.p1_card1.grid(row=3, column=2)
        self.p1_card2 = tk.Label(mainWindow, image=self.cards[0][1])
        self.p1_card2.grid(row=3, column=3)
        self.p2_card1 = tk.Label(mainWindow, image=self.cards[1][0])
        self.p2_card1.grid(row=3, column=8)
        self.p2_card2 = tk.Label(mainWindow, image=self.cards[1][1])
        self.p2_card2.grid(row=3, column=9)

    def initialize_cards_on_table(self):
        self.images = [backImage, backImage, backImage, backImage, backImage]
        self.card1.grid_forget()
        self.card2.grid_forget()
        self.card3.grid_forget()
        self.card4.grid_forget()
        self.card5.grid_forget()
        self.add_post_flop_photos()

    def add_post_flop_photos(self):
        for i in range(len(cardsOnTable)):
            self.images[i] = ImageTk.PhotoImage(Image.open(photoDict[cardsOnTable[i]]))
        self.card1 = tk.Label(mainWindow, image=self.images[0])
        self.card1.grid(row=1, column=4)
        self.card2 = tk.Label(mainWindow, image=self.images[1])
        self.card2.grid(row=1, column=5)
        self.card3 = tk.Label(mainWindow, image=self.images[2])
        self.card3.grid(row=1, column=6)
        self.card4 = tk.Label(mainWindow, image=self.images[3])
        self.card4.grid(row=1, column=7)
        self.card5 = tk.Label(mainWindow, image=self.images[4])
        self.card5.grid(row=1, column=8)
# Set up the screen and frames for the dealer and player

mainWindow.title("PokerBets")
mainWindow.geometry("1280x720")
mainWindow.configure(bg="gray")

mainWindow.columnconfigure(0, weight=2)
mainWindow.columnconfigure(1, weight=5)
mainWindow.columnconfigure(2, weight=5)
mainWindow.columnconfigure(3, weight=5)
mainWindow.columnconfigure(4, weight=5)
mainWindow.columnconfigure(5, weight=5)
mainWindow.columnconfigure(6, weight=5)
mainWindow.columnconfigure(7, weight=5)
mainWindow.columnconfigure(8, weight=5)
mainWindow.columnconfigure(9, weight=5)
mainWindow.columnconfigure(10, weight=2)

mainWindow.rowconfigure(0, weight=2)
mainWindow.rowconfigure(1, weight=7)
mainWindow.rowconfigure(2, weight=2)
mainWindow.rowconfigure(3, weight=5)
mainWindow.rowconfigure(4, weight=2)
mainWindow.rowconfigure(5, weight=2)
mainWindow.rowconfigure(6, weight=2)
mainWindow.rowconfigure(7, weight=2)
mainWindow.rowconfigure(8, weight=2)
mainWindow.rowconfigure(9, weight=2)
mainWindow.rowconfigure(10, weight=2)
mainWindow.rowconfigure(11, weight=2)
mainWindow.rowconfigure(12, weight=2)
mainWindow.rowconfigure(13, weight=2)

p1 = tk.Label(mainWindow, text="Player 1: Phil Ivey", fg='black', bg="gray", wraplength=130, justify=CENTER).grid(row=2, column=2, columnspan=2)
p2 = tk.Label(mainWindow, text="Player 2: Daniel Negreanu", fg='yellow', bg="gray", justify=CENTER).grid(row=2, column=8, columnspan=2)

player = PlayerBalance()

p1_bet_btn = tk.Button(mainWindow, text="Bet", justify=CENTER, padx=10, pady=3, command=player.bet).grid(row=6, column=2, columnspan=2)
p2_bet_btn = tk.Button(mainWindow, text="Bet", justify=CENTER, padx=10, pady=3, command=player.bet).grid(row=6, column=8, columnspan=2)
tie_bet_btn = tk.Button(mainWindow, text="Bet", justify=CENTER, padx=10, pady=3, command=player.bet).grid(row=6, column=5, columnspan=2)

start_again_button = tk.Button(mainWindow, text="Start Again", justify=CENTER, padx=10, pady=3, command=player.start_new_game).grid(row=9, column=9, columnspan=2)

mainWindow.mainloop()