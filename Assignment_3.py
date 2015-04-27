# template for "Stopwatch: The Game"

import simplegui

# @author Bulent Kamberoglu

# define global variables
interval = 100
started = False

position = [75, 100]
milliseconds = 0 
seconds = 0
minutes = 0
t = 0

count_correct_answer = 0
count_wrong_answer = 0
maximum_run_time = 10000


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global milliseconds
    global seconds
    global minutes 
    milliseconds = (t % 10)
    seconds = (t - milliseconds )// 10 
    seconds, minutes = seconds % 60, seconds // 60 
    str_seconds = str(seconds)
    if milliseconds > 9:
        milliseconds = 0 
        seconds = seconds + 1 
    if( seconds > 59) : 
        minutes = minutes + 1
        seconds = seconds - 60 
        str_seconds = str(seconds) 
    if len(str(seconds)) == 1:
        str_seconds = "0" + str(seconds)
    
    return str(minutes) + ":" + str_seconds + "." + str(milliseconds)

    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global started
    started = True
    timer.start()
       
def stop_handler():
     global started, count_correct_answer, count_wrong_answer
     timer.stop()
     if started == True:
        if milliseconds == 0:
            count_correct_answer += 1
        else:
            count_wrong_answer += 1 
      
     started = False

def reset_handler():
    global started, t, count_correct_answer, count_wrong_answer
    started = False
    timer.stop()
    t = 0
    count_correct_answer = 0
    count_wrong_answer = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global t, maximum_run_time
    t = t + 1
    if t == maximum_run_time:
        timer.stop() 

# define draw handler

def draw_handler(canvas):
    canvas.draw_text(format(t), position, 30, "White")
    canvas.draw_text(str(count_correct_answer),[100,20], 20, "Green")
    canvas.draw_text("/",[110,20], 20, "Green")
    canvas.draw_text(str(count_wrong_answer),[115,20], 20, "Green")

    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(interval, timer_handler)


# register event handlers
frame.add_button("Start", start_handler, 100)
frame.add_button("Stop", stop_handler, 100)
frame.add_button("Reset", reset_handler, 100)

# start frame
frame.start()


# Please remember to review the grading rubric
