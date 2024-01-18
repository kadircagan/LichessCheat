import pyautogui
import time

def moove_location(start_x,start_y,x_plus,y_plus,moove,gamecolor):

    #start_x = start_x+x_plus*7
    start_y = start_y+y_plus*7
    if gamecolor =="b":
        letters_array = ["h", "g", "f","e","d","c","b","a"]
        numbers_Array = ["8", "7", "6","5","4","3","2","1"]
    else:
        letters_array = ["a", "b", "c","d","e","f","g","h"]
        numbers_Array = ["1", "2", "3","4","5","6","7","8"]


    index1 = letters_array.index(moove[:1])
    index2 = numbers_Array.index(moove[1:])

    start_x = start_x+x_plus*index1
    start_y= start_y-y_plus*index2
    
    return start_x,start_y


def makeMove(start_x,start_y,end_x,end_y,moove,gamecolor):
    #start_x = 600
    #start_y = 200
    #end_x = 1300
    #end_y = 900



    x_plus =int((end_x-start_x)/7)
    y_plus =int((end_y-start_y)/7)


    first_moove = moove[:2]
    second_moove = moove[2:]



    # Set up positions
    moove_start_x ,moove_start_y = moove_location(start_x,start_y,x_plus,y_plus,first_moove,gamecolor)
    moove_end_x ,moove_end_y = moove_location(start_x,start_y,x_plus,y_plus,second_moove,gamecolor)

    print(moove_start_x,moove_start_y)
    print(moove_end_x,moove_end_y)
    # Move the mouse cursor to the starting position
    pyautogui.moveTo(moove_start_x, moove_start_y, duration=0.1)

    # Perform right-click at the starting position
    pyautogui.mouseDown(button="right")

    # Pause for a short duration


    # Drag the mouse cursor to the end position
    pyautogui.moveTo(moove_end_x, moove_end_y, duration=0.1)

    # Release the mouse button at the end position
    pyautogui.mouseUp(button="right")

    # Pause for a short duration

#print(moove_location(600,200,(1300-600)/7,(900-200)/7,"c4"))
#makeMove(600,200,1300,900,"b2c4")