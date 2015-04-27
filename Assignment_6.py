# Mini-project #6 - Blackjack

import simplegui
import random

# @author Bulent Kamberoglu

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

message = "Hit or stand?"
uncover_dealers_card = True


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, flipped):
        if not flipped:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.cover_second = False

    def __str__(self):
        stringCard = ''
        for card in self.cards:
            stringCard = stringCard + " " + str(card)
        return stringCard

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0 
        for card in self.cards:
            value += VALUES[card.get_rank()]
        if self.count_aces() == 0:
            return value
        else:
            if value + 10 > 21:
                return value
            else:
                return value + 10        
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            if self.cover_second and i == 1:
                card.draw(canvas, [pos[0] + i * (CARD_SIZE[0] + 20), pos[1]], True)
            else:
                card.draw(canvas, [pos[0] + i * (CARD_SIZE[0] + 20), pos[1]], False)
            i += 1
    
 
    def busted(self):
        return self.get_value() > 21
     
    def number_cards(self):
        number = 0
        for card in self.cards:
            number += 1
        return number
    
    def hit(self, deck):
        self.add_card(deck.deal_card())
        
   
    def count_aces(self):
        aces = 0
        for card in self.cards:
            if card.get_rank() == 'A':
                aces += 1
        return aces
   
    def is_second_covered(self):
        return self.cover_second
    
    def set_cover_second(self, cover):
        self.cover_second = cover
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]  
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        for card in self.deck:
            print card,



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, message, score

    init()
    if in_play:
        score -= 1
    in_play = True
    player_hand.hit(deck)
    player_hand.hit(deck)
    dealer_hand.hit(deck)
    dealer_hand.hit(deck)	
    
   # This is not required in the project otherwise, it can be used to check blackjack 
   # when a new game is dealed
   # if dealer_hand.get_value() == 21:
   #     score -= 1
   #     in_play = False
   #     message = "Blackjack!! Dealer wins! New deal?"
   # else:
   #     if player_hand.get_value() == 21:
   #         score += 1
   #         in_play = False
   #         message = "Blackjack!! Player wins! New deal?"
   #     else:
   #         message = "Hit or stand?"
   #         dealer_hand.set_cover_second(True)
    
    message = "Hit or stand?"
    dealer_hand.set_cover_second(True)
    
def init():
    global in_play, player_hand, dealer_hand, deck
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    
def hit():
    global in_play, score, message
    if not player_hand.busted() and in_play:
        player_hand.hit(deck)
        if player_hand.busted():
            dealer_hand.set_cover_second(False)
            message = "Player is busted! New deal?"
            in_play = False
            score -= 1
       
def stand():
    global dealer_hand, in_play, score, message
    if in_play:
        if not player_hand.busted():
            dealer_hand.set_cover_second(False)
            while dealer_hand.get_value() < 17:
                dealer_hand.hit(deck)
            if dealer_hand.busted():
                message = "Dealer busted. Player wins! New deal?"
                score += 1
            else:
                if dealer_hand.get_value() >= player_hand.get_value():
                    message = "Dealer wins! New deal?"
                    score -= 1
                else:
                    message = "Player wins! New deal?"
                    score += 1
            in_play = False
    else:
        message = "New deal?"

# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", (50, 100), 36, "Blue")
    canvas.draw_text("Score " + str(score), (480, 100), 24, "Black")
    canvas.draw_text(message, (200, 375), 24, "Black")
    canvas.draw_text("Dealer", (60, 175), 24, "Black")
    canvas.draw_text("Player", (60, 375), 24, "Black")
    player_hand.draw(canvas, (60, 410))
    dealer_hand.draw(canvas, (60, 210))


# initialization frame
frame = simplegui.create_frame("Blackjack", 700, 700)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric