from tkinter import PhotoImage
from tkinter.constants import CENTER, LEFT
from PIL import Image, ImageTk


try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

if tk.TkVersion >= 8.6:
    extension = 'png'
else:
    extension = 'png'

mainWindow = tk.Tk()

class PlayerBalance():
    def __init__(self) -> None:
        self.balance = 1000
    def bet(self, amount):
        self.balance -= amount

betting_round_dummy = -1
def bettingRound():
    list_of_rounds = ['Pre-Hole', 'Pre-Flop', 'Post-Flop', 'Before Turn']
    global betting_round_dummy
    if betting_round_dummy == 3:
        betting_round_dummy = 0
    else:
        betting_round_dummy += 1
        return list_of_rounds[betting_round_dummy]

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
mainWindow.columnconfigure(1, weight=3)
mainWindow.columnconfigure(2, weight=3)
mainWindow.columnconfigure(3, weight=5)
mainWindow.columnconfigure(4, weight=5)
mainWindow.columnconfigure(5, weight=5)
mainWindow.columnconfigure(6, weight=5)
mainWindow.columnconfigure(7, weight=5)
mainWindow.columnconfigure(8, weight=5)
mainWindow.columnconfigure(9, weight=3)
mainWindow.columnconfigure(10, weight=2)

mainWindow.rowconfigure(0, weight=2)
mainWindow.rowconfigure(1, weight=2)
mainWindow.rowconfigure(2, weight=10)
mainWindow.rowconfigure(3, weight=10)
mainWindow.rowconfigure(4, weight=2)
mainWindow.rowconfigure(5, weight=2)

player = PlayerBalance()

heading = tk.Label(mainWindow, text="Betting Round: {}".format(bettingRound()), wraplength=110, justify=CENTER).grid(row=0, column=5)

player_balance = tk.Label(mainWindow, text="Current balance is {} coins".format(player.balance), fg='green', wraplength=180, justify=CENTER).grid(row=0, column=10)

p1 = tk.Label(mainWindow, text="Player 1: Phil Ivey", fg='black', bg="gray", wraplength=130, justify=CENTER).grid(row=1, column=3)
p2 = tk.Label(mainWindow, text="Player 2: Daniel Negreanu", fg='yellow', bg="gray", wraplength=130, justify=CENTER).grid(row=1, column=9)

cardsOnTable = ["12D", "3H", "2S"]

backImage = ImageTk.PhotoImage(Image.open(photoDict['0']))
images = [backImage, backImage, backImage, backImage, backImage]
for i in range(len(cardsOnTable)):
    images[i] = ImageTk.PhotoImage(Image.open(photoDict[cardsOnTable[i]]))

card1 = tk.Label(mainWindow, image=images[0]).grid(row=2, column=4)
card2 = tk.Label(mainWindow, image=images[1]).grid(row=2, column=5)
card3 = tk.Label(mainWindow, image=images[2]).grid(row=2, column=6)
card4 = tk.Label(mainWindow, image=images[3]).grid(row=2, column=7)
card5 = tk.Label(mainWindow, image=images[4]).grid(row=2, column=8)

cards = [[backImage, backImage], [backImage, backImage]]

actual_card = [['8C', '10S'], ['5C', '3H']]

if actual_card:
    for i in range(2):
        for j in range(2):
            cards[i][j] = actual_card[i][j]



mainWindow.mainloop()