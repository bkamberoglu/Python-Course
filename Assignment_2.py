# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# @author Bulent Kamberoglu

# initialize global variables used in your code
range_1000_button_clicked = False
counter = 0;
random_number = 0


# helper function to start and restart the game
def new_game():
    print " "
    global counter
    global random_number
    clear_input_box()
    if range_1000_button_clicked:
        counter = find_secret_number(0, 1000)
        random_number = random.randrange(0, 1000)
        print "New game. Range is from 0 to 1000"
        print "Number of remaining guess is",counter
    else:
        counter = find_secret_number(0, 100)
        random_number = random.randrange(0, 100)  
        print "New game. Range is from 0 to 100"
        print "Number of remaining guess is",counter
     
        
def find_secret_number(low, high):
    x = 1
    for x in range(low, high):
        if math.pow(2, x) >= high - low + 1:
            return x
    

# define event handlers for control panel
def range100():
    global range_1000_button_clicked
    if range_1000_button_clicked:
        range_1000_button_clicked = False
    new_game()
    

def range1000():
    global range_1000_button_clicked
    range_1000_button_clicked = True
    new_game()
    
    
def input_guess(guess):
    # main game logic goes here	
    
    # remove this when you add your codepass
    global counter
    counter = counter - 1
    guess = int(guess)
    print " "
    print "Guess was", guess
    print "Number of remaining guess is", counter 
    
    if guess < random_number:
        print "Higher!"
    elif guess > random_number:
        print "Lower!"
    else:
        print "Correct!"
        new_game()
    
    if counter == 0:
        print " "
        print "Oppps!. You don't have any guess left!"
        new_game()
            
            
def clear_input_box():
    input_box.set_text("");

    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)


# register event handlers for control elements
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
input_box = frame.add_input("Enter a guess", input_guess, 200)


# call new_game and start frame
new_game()
frame.start()


# always remember to check your completed program against the grading rubric
