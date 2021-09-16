from tkinter import PhotoImage
from tkinter.constants import CENTER, LEFT, RAISED
from PIL import Image, ImageTk
from poker import dealHoleCards, dealFlop, dealRiver, dealTurn, cardsOnTable, deckBuilder, bookOfCards, postFlopOddsCalc, checkRiverOddsCalc, finalScore, odds_calculator
from preFlopChecker import preFlopHelper

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

mainWindow = tk.Tk()

deckBuilder()
hole_cards = []

class PlayerBalance():
    def __init__(self) -> None:
        self.balance = 1000
        self.player_balance = tk.Label(mainWindow, text="Current balance is {} coins".format(self.balance), fg='green', wraplength=180, justify=CENTER)
        self.player_balance.grid(row=0, column=9)
        self.amount_on_p1 = []
        self.amount_on_tie = []
        self.amount_on_p2 = []
        self.heading = tk.Label(mainWindow, text="Betting Round: {}".format(list_of_rounds[betting_round_dummy]), justify=CENTER)
        self.heading.grid(row=0, column=5, columnspan=3)
        self.warning = tk.Label(mainWindow, text="", bg="gray")
        self.warning.grid(row=3, column=5, columnspan=2)
        self.hole_cards = []
        self.odds_p1, self.odds_p2, self.odds_tie = 1, 1, 0

    def bet(self):
        amount = 0
        amount += int(p1_bet.get()) + int(p2_bet.get()) + int(tie_bet.get())
        if amount < self.balance:
            self.warning.grid_forget()
            self.amount_on_p1.append([int(p1_bet.get()), self.odds_p1])
            self.amount_on_tie.append([int(tie_bet.get()), self.odds_p2])
            self.amount_on_p2.append([int(p2_bet.get()), self.odds_tie])
            self.balance -= amount
            self.player_balance.grid_forget()
            self.player_balance = tk.Label(mainWindow, text="Current balance is {} coins".format(self.balance), fg='green', wraplength=180, justify=CENTER)
            self.player_balance.grid(row=0, column=9)
            self.deal_cards()
        else:
            self.warning = tk.Label(mainWindow, text="Your current bet amount exceeds your remaining balance")
            self.warning.grid(row=3, column=5, columnspan=2)

    def start_new_game(self):
        self.balance = 1000
        self.player_balance = tk.Label(mainWindow, text="Current balance is {} coins".format(self.balance), fg='green', wraplength=180, justify=CENTER)
        self.player_balance.grid(row=0, column=9)
        self.amount_on_p1 = []
        self.amount_on_tie = []
        self.amount_on_p2 = []
        self.heading = tk.Label(mainWindow, text="Betting Round: {}".format(list_of_rounds[betting_round_dummy]), justify=CENTER)
        self.heading.grid(row=0, column=5, columnspan=3)
        self.warning = tk.Label(mainWindow, text="", bg="gray")
        self.warning.grid(row=3, column=5, columnspan=2)
        odds_p1_win.grid_forget()
        odds_p2_win.grid_forget()
        odds_p1_p2_tie.grid_forget()
        self.odds_p1, self.odds_p2, self.odds_tie = 1, 1, 0
        display_odds(self.odds_p1, odds_p2, odds_tie)

    def deal_cards(self):
        self.deal_next_round()
        self.heading.grid_forget()
        self.heading = tk.Label(mainWindow, text="Betting Round: {}".format(list_of_rounds[betting_round_dummy]), justify=CENTER)
        self.heading.grid(row=0, column=5, columnspan=3)

    def deal_next_round(self):
        if len(bookOfCards) == 52:
            global self.odds_p1
            global odds_p2
            global odds_tie
            self.hole_cards = dealHoleCards(2)
            print(hole_cards)
            self.odds_p1, self.odds_p2 = preFlopHelper(hole_cards)
            self.odds_tie = 0
            self.display_odds(self.odds_p1, odds_p2, odds_tie)
            self.add_photos()

        elif len(bookOfCards) == 48:
            dealFlop()
            self.odds_p1, odds_p2, odds_tie = postFlopOddsCalc(hole_cards)
            print(self.odds_p1, odds_p2, odds_tie)
            self.display_odds(self.odds_p1, odds_p2, odds_tie)
        elif len(bookOfCards) == 45:
            dealRiver()
            self.odds_p1, odds_p2, odds_tie = checkRiverOddsCalc()
            display_odds(self.odds_p1, odds_p2, odds_tie)
        elif len(bookOfCards) == 44:
            turn = dealTurn() 
            result = finalScore()
            display_final_score(result)
            global net_win
            global net_loss
            net_win = 0
            net_loss = 0
            amount_bet_on_p1 = player.amount_on_p1
            amount_bet_on_p2 = player.amount_on_p2
            amount_bet_on_tie = player.amount_on_tie
            if result == "Player 1 Wins":
                for i in range(4):
                    net_win += amount_bet_on_p1[i][0] * (1+amount_bet_on_p1[i][1])
                    net_loss += amount_bet_on_p2[i][0]
                    net_loss += amount_bet_on_tie[i][0]
            elif result == "Player 2 Wins":
                for i in range(4):
                    net_win += amount_bet_on_p2[i][0] * (1+amount_bet_on_p2[i][1])
                    net_loss += amount_bet_on_p1[i][0]
                    net_loss += amount_bet_on_tie[i][0]
            else:
                for i in range(4):
                    net_win += amount_bet_on_tie[i][0] * (1+amount_bet_on_tie[i][1])
                    net_loss += amount_bet_on_p2[i][0]
                    net_loss += amount_bet_on_p1[i][0]
            player.balance = player.balance + net_win - net_loss
            player.player_balance.grid_forget()
            player.player_balance = tk.Label(mainWindow, text="Current balance is {} coins".format(player.balance), fg='green', wraplength=180, justify=CENTER)
            player.player_balance.grid(row=0, column=9)
            print(amount_bet_on_p1)
            print(amount_bet_on_p2)
            print(player.balance)
        add_post_flop_photos()

    def display_odds(self, odds_p1, odds_p2, odds_tie=0):
        global odds_p1_win
        global odds_p2_win
        global odds_p1_p2_tie
        odds_p1_win = tk.Label(mainWindow, text="P1 odds = 1 to {}".format(str(round(self.odds_p1, 2))), bg="#9a9898", fg="#222dca")
        odds_p1_win.grid(row=4, column=2, columnspan=2)
        odds_p2_win = tk.Label(mainWindow, text="P2 odds = 1 to {}".format(str(round(odds_p2,2))), bg="#9a9898", fg="#222dca")
        odds_p2_win.grid(row=4, column=8, columnspan=2)
        odds_p1_p2_tie = tk.Label(mainWindow, text="Odds of tie = 1 to {}".format(str(round(odds_tie,2))), justify=CENTER, bg="#9a9898", fg="#222dca")
        odds_p1_p2_tie.grid(row=4, column=5, columnspan=2)