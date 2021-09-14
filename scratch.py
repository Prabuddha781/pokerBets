from tkinter import *
from poker import deckBuilder

deck = [str(cards) + suits for suits in ["D", "H", "C", "S"] for cards in range(1,14)]

suits = ['diamond', 'heart', 'club', 'spade']
face_cards = ['jack', 'queen', 'king']

card_images = []
for suit in suits:
    # first the number cards 1 to 10
    for card in range(1, 11):
        name = 'cards/{}_{}.png'.format(str(card), suit)
        card_images.append(name)

    # next the face cards
    for card in face_cards:
        name = 'cards/{}_{}.png'.format(str(card), suit)
        card_images.append(name)

dict_card_images = {}
for i in range(52):
    dict_card_images[deck[i]] = card_images[i]

print(dict_card_images)


{'1D': 'cards/1_diamond.png', '2D': 'cards/2_diamond.png', '3D': 'cards/3_diamond.png', 
'4D': 'cards/4_diamond.png', '5D': 'cards/5_diamond.png', '6D': 'cards/6_diamond.png', 
'7D': 'cards/7_diamond.png', '8D': 'cards/8_diamond.png', '9D': 'cards/9_diamond.png', 
'10D': 'cards/10_diamond.png', '11D': 'cards/jack_diamond.png', '12D': 'cards/queen_diamond.png', 
'13D': 'cards/king_diamond.png', '1H': 'cards/1_heart.png', '2H': 'cards/2_heart.png', 
'3H': 'cards/3_heart.png', '4H': 'cards/4_heart.png', '5H': 'cards/5_heart.png', 
'6H': 'cards/6_heart.png', '7H': 'cards/7_heart.png', '8H': 'cards/8_heart.png', 
'9H': 'cards/9_heart.png', '10H': 'cards/10_heart.png', '11H': 'cards/jack_heart.png', 
'12H': 'cards/queen_heart.png', '13H': 'cards/king_heart.png', '1C': 'cards/1_club.png', 
'2C': 'cards/2_club.png', '3C': 'cards/3_club.png', '4C': 'cards/4_club.png', '5C': 'cards/5_club.png', 
'6C': 'cards/6_club.png', '7C': 'cards/7_club.png', '8C': 'cards/8_club.png', '9C': 'cards/9_club.png', '10C': 'cards/10_club.png', '11C': 'cards/jack_club.png', '12C': 'cards/queen_club.png', '13C': 'cards/king_club.png', '1S': 'cards/1_spade.png', '2S': 'cards/2_spade.png', '3S': 'cards/3_spade.png', '4S': 'cards/4_spade.png', '5S': 'cards/5_spade.png', '6S': 'cards/6_spade.png', '7S': 'cards/7_spade.png', '8S': 'cards/8_spade.png', '9S': 'cards/9_spade.png', '10S': 'cards/10_spade.png', '11S': 'cards/jack_spade.png', '12S': 'cards/queen_spade.png', '13S': 'cards/king_spade.png'}