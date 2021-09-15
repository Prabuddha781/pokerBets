from tkinter import PhotoImage
from tkinter.constants import CENTER, LEFT, RAISED
from PIL import Image, ImageTk
from poker import dealHoleCards, dealFlop, dealRiver, dealTurn, cardsOnTable, deckBuilder, bookOfCards, postFlopOddsCalc, checkRiverOddsCalc, finalScore
from preFlopChecker import preFlopHelper

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

mainWindow = tk.Tk()

odds_p1, odds_p2, odds_tie = 0.5, 0.5, 0.5

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

    def bet(self):
        amount = 0
        self.amount_on_p1.append([int(p1_bet.get()), odds_p1])
        self.amount_on_tie.append([int(p2_bet.get()), odds_p2])
        self.amount_on_p2.append([int(tie_bet.get()), odds_tie])
        amount += int(p1_bet.get()) + int(p2_bet.get()) + int(tie_bet.get())
        self.balance -= amount
        self.player_balance.grid_forget()
        self.player_balance = tk.Label(mainWindow, text="Current balance is {} coins".format(self.balance), fg='green', wraplength=180, justify=CENTER)
        self.player_balance.grid(row=0, column=9)
        self.deal_cards()

    def deal_cards(self):
        deal_next_round()
        # bettingRound()
        self.heading.grid_forget()
        self.heading = tk.Label(mainWindow, text="Betting Round: {}".format(list_of_rounds[betting_round_dummy]), justify=CENTER)
        self.heading.grid(row=0, column=5, columnspan=3)

def deal_next_round():
    if len(bookOfCards) == 52:
        global hole_cards
        hole_cards = dealHoleCards(2)
        print(hole_cards)
        odds_p1, odds_p2 = preFlopHelper(hole_cards)
        display_odds(odds_p1, odds_p2, odds_tie=0)
        add_photos()
    elif len(bookOfCards) == 48:
        dealFlop()
        odds_p1, odds_p2, odds_tie = postFlopOddsCalc()
        display_odds(odds_p1, odds_p2, odds_tie)
    elif len(bookOfCards) == 45:
        dealRiver()
    elif len(bookOfCards) == 44:
        turn = dealTurn() 
    add_post_flop_photos()

def display_odds(odds_p1, odds_p2, odds_tie=0):
    odds_p1_win = tk.Label(mainWindow, text="P1 win = {}%".format(str(odds_p1*100)), bg="#9a9898", fg="#222dca")
    odds_p1_win.grid(row=4, column=2, columnspan=2)
    odds_p2_win = tk.Label(mainWindow, text="P2 win = {}%".format(str(odds_p2*100)), bg="#9a9898", fg="#222dca")
    odds_p2_win.grid(row=4, column=8, columnspan=2)
    odds_p1_p2_tie = tk.Label(mainWindow, text="Odds of tie = {}%".format(str(odds_tie*100)), justify=CENTER, bg="#9a9898", fg="#222dca")
    odds_p1_p2_tie.grid(row=4, column=5, columnspan=2)

list_of_rounds = ['Pre-Hole', 'Pre-Flop', 'Post-Flop', 'Before Turn', 'Game-Finished:Betting Not Allowed']
betting_round_dummy = 0
def bettingRound():
    global betting_round_dummy
    if betting_round_dummy == 5:
        betting_round_dummy = -1
    betting_round_dummy += 1


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


player = PlayerBalance()

backImage = ImageTk.PhotoImage(Image.open(photoDict['0']))
images = [backImage, backImage, backImage, backImage, backImage]

def add_post_flop_photos():
    for i in range(len(cardsOnTable)):
        images[i] = ImageTk.PhotoImage(Image.open(photoDict[cardsOnTable[i]]))
    card1 = tk.Label(mainWindow, image=images[0]).grid(row=1, column=4)
    card2 = tk.Label(mainWindow, image=images[1]).grid(row=1, column=5)
    card3 = tk.Label(mainWindow, image=images[2]).grid(row=1, column=6)
    card4 = tk.Label(mainWindow, image=images[3]).grid(row=1, column=7)
    card5 = tk.Label(mainWindow, image=images[4]).grid(row=1, column=8)

card1 = tk.Label(mainWindow, image=images[0]).grid(row=1, column=4)
card2 = tk.Label(mainWindow, image=images[1]).grid(row=1, column=5)
card3 = tk.Label(mainWindow, image=images[2]).grid(row=1, column=6)
card4 = tk.Label(mainWindow, image=images[3]).grid(row=1, column=7)
card5 = tk.Label(mainWindow, image=images[4]).grid(row=1, column=8)

p1 = tk.Label(mainWindow, text="Player 1: Phil Ivey", fg='black', bg="gray", wraplength=130, justify=CENTER).grid(row=2, column=2, columnspan=2)
p2 = tk.Label(mainWindow, text="Player 2: Daniel Negreanu", fg='yellow', bg="gray", justify=CENTER).grid(row=2, column=8, columnspan=2)

cards = [[backImage, backImage], [backImage, backImage]]

def add_photos():
    if len(hole_cards) == 2:
        for i in range(2):
            for j in range(2):
                cards[i][j] = ImageTk.PhotoImage(Image.open(photoDict[hole_cards[i][j]]))
    p1_card1 = tk.Label(mainWindow, image=cards[0][0]).grid(row=3, column=2)
    p1_card2 = tk.Label(mainWindow, image=cards[0][1]).grid(row=3, column=3)
    p2_card1 = tk.Label(mainWindow, image=cards[1][0]).grid(row=3, column=8)
    p2_card2 = tk.Label(mainWindow, image=cards[1][1]).grid(row=3, column=9)

p1_card1 = tk.Label(mainWindow, image=cards[0][0]).grid(row=3, column=2)
p1_card2 = tk.Label(mainWindow, image=cards[0][1]).grid(row=3, column=3)
p2_card1 = tk.Label(mainWindow, image=cards[1][0]).grid(row=3, column=8)
p2_card2 = tk.Label(mainWindow, image=cards[1][1]).grid(row=3, column=9)

odds_p1_win = tk.Label(mainWindow, text="P1 win = {}%".format(str(odds_p1*100)), bg="#9a9898", fg="#222dca")
odds_p1_win.grid(row=4, column=2, columnspan=2)
odds_p2_win = tk.Label(mainWindow, text="P2 win = {}%".format(str(odds_p2*100)), bg="#9a9898", fg="#222dca")
odds_p2_win.grid(row=4, column=8, columnspan=2)
odds_p1_p2_tie = tk.Label(mainWindow, text="Odds of tie = {}%".format(str(odds_tie*100)), justify=CENTER, bg="#9a9898", fg="#222dca")
odds_p1_p2_tie.grid(row=4, column=5, columnspan=2)

p1_bet = tk.Entry(mainWindow, width=5, relief=RAISED, justify=CENTER)
p1_bet.insert(0, "0")
p1_bet.grid(row=5, column=2, columnspan=2)
p2_bet = tk.Entry(mainWindow, width=5, relief=RAISED, justify=CENTER)
p2_bet.insert(0, "0")
p2_bet.grid(row=5, column=8, columnspan=2)
tie_bet = tk.Entry(mainWindow, width=5, relief=RAISED, justify=CENTER)
tie_bet.insert(0, "0")
tie_bet.grid(row=5, column=5, columnspan=2)

p1_bet_btn = tk.Button(mainWindow, text="Bet", justify=CENTER, padx=10, pady=3, command=player.bet).grid(row=6, column=2, columnspan=2)
p2_bet_btn = tk.Button(mainWindow, text="Bet", justify=CENTER, padx=10, pady=3, command=player.bet).grid(row=6, column=8, columnspan=2)
tie_bet_btn = tk.Button(mainWindow, text="Bet", justify=CENTER, padx=10, pady=3, command=player.bet).grid(row=6, column=5, columnspan=2)

mainWindow.mainloop()