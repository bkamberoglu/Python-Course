# implementation of card game - Memory

import simplegui
import random

# @author Bulent Kamberoglu

WIDTH = 1600
HEIGHT = 200
EACH_CARD_WIDTH = WIDTH /16

cardList = []
correctList = []
exposedList = []
state = 0, 
preCard = -1
turns = 0 


# helper function to initialize globals
def new_game():
    global cardList, correctList, exposedList, state, preCard, turns
    cardList = [(i % 8) for i in range(16)]
    random.shuffle(cardList)
    exposedList = [False for i in range(16)]
    correctList = [False for i in range(8)]
    state = 0
    turns = 0
    preCard = -1
    label.set_text("Turns = " + str(turns))   
    
def changeState(selectedCard):
    global state, exposedList, preCard, turns
    if state == 0:
        state = 1
        turns += 1
    elif state == 1:
        if preCard == cardList[selectedCard]:
            correctList[cardList[selectedCard]] = True            
        state = 2
    else:
        for i in range(16):
            if not correctList[cardList[i]]:
                exposedList[i] = False
        turns += 1
        state = 1
    label.set_text("Turns = " + str(turns))
    
     
# define event handlers
def mouseclick(pos):
    global state, exposedList, preCard
    for i in range(16):
        if pos[0] >= EACH_CARD_WIDTH * i and pos[0] < EACH_CARD_WIDTH * (i + 1) and not exposedList[i]:
            changeState(i)
            preCard = cardList[i]
            exposedList[i] = True
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
     for i in range(16):
        if exposedList[i]:
            canvas.draw_text(str(cardList[i]), [EACH_CARD_WIDTH * i + WIDTH / 60, HEIGHT / 2 + 20], 70, "White")
        else:
            canvas.draw_text(" ", [EACH_CARD_WIDTH * i + WIDTH / 60, 60], 30, "White")
        canvas.draw_line([EACH_CARD_WIDTH * (i + 1), 0], [EACH_CARD_WIDTH * (i + 1), HEIGHT], 2, "White")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.set_canvas_background('Green')

frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric