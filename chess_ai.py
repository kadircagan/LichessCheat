from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import chess
import re
import chess.engine
from stockfish import Stockfish
from pynput.mouse import Listener
import arrows
import keyboard
import threading


gamecolor= "w"

def handle_click(x, y, button, pressed, listener):
    if pressed:
        print("Mouse clicked at x =", x, "y =", y, "button =", button)
        listener.stop()
        set_board_Coordinates.result = (x, y)  # Store the result in a variable

def set_board_Coordinates():
    listener = Listener(on_click=lambda x, y, button, pressed: handle_click(x, y, button, pressed, listener))
    listener.start()
    listener.join()

    return set_board_Coordinates.result  # Return the stored result
    
def create_board_from_hash_map(hash_map):
    array_2d = [[1 for _ in range(8)] for _ in range(8)]
    

    for key, value in hash_map.items():
        y= int(value[1]/70)
        x=int(value[0]/70)
        if key[0]=="b":
            array_2d[y][x]= key[1]
        else:
            array_2d[y][x]= key[1].upper()
#    for row in array_2d:
#        print(row)

    return array_to_fen(array_2d)


def array_to_fen(board):
    fen = ''
    empty_count = 0

    for row in board:
        for square in row:
            if isinstance(square, int):
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += str(square)
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += '/'

    fen = fen[:-1]  # Remove the trailing slash '/'

    # Replace multiple consecutive digits with a single digit
    for i in range(8, 0, -1):
        fen = fen.replace('1' * i, str(i))

    fen += ' '+gamecolor+' '+'- - 0 1'  # Add remaining FEN components

    return fen



def listener_thread():
    while True:
        keyboard.wait('m')
        arrows.makeMove(start_x,start_y,end_x,end_y,moove,gamecolor)


gamecolor = input("Enter your color: ")


engine = chess.engine.SimpleEngine.popen_uci("E:\yapayZeka\chessai\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

#stockfish = Stockfish(path="E:\yapayZeka\chessai\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})
stockfish = Stockfish("E:\yapayZeka\chessai\stockfish_14_win_x64_avx2\stockfish_14_x64_avx2.exe")
stockfish.set_depth(20)
stockfish.set_skill_level(20)
start_time = time.time()
board = chess.Board()

fen = "rkbqkb1r/ppp3p1/5k2/3pp3/8/2P3P1/PP1PPPBP/RK1QK1NR w - - 0 1"
board.set_fen(fen)

print(board)


webdriver_service = Service('E:\yapayZeka\chessai\chromedriver.exe')  # WebDriver'ın yerel yolunu sağlayın

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--start-minimized') 
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# set the board
start_x, start_y = set_board_Coordinates()
end_x, end_y = set_board_Coordinates()
moove=""

thread = threading.Thread(target=listener_thread)
thread.start()


kadir = True
hash_map = {}
i=0
while kadir:
    hash_map = {}
    elapsed_time = time.time() - start_time
    driverStr="https://lichess.org/0cl0Cp7Hm6xH"
    
    if gamecolor =="b":
        driverStr= driverStr[:-4]
        driverStr = driverStr+"/white"
        driver.get(driverStr)  # Sayfanın URL'sini belirtin if it is black you have to take as black
    else:
        driver.get(driverStr)
    
    pieces = driver.find_elements(By.XPATH, '//*[@id="main-wrap"]/main/div[1]/div[1]/div/cg-container/cg-board/piece')

    for piece in pieces:
        class_value = piece.get_attribute('class')
        #print(class_value)
        i=i+1
        style = piece.get_attribute('style')
        transform_value = ''
        if style:
            style_properties = style.split(';')
            for prop in style_properties:
                if 'transform' in prop:
                    transform_value = prop.split(':')[1].strip()
                    break

        # Stringdeki tüm sayıları int olarak almak için regex kullanma
        numbers = [int(num) for num in re.findall(r'\d+', transform_value)]




        
        stringvalueArray = class_value.split(" ")
        if stringvalueArray[1] =="knight":
            stringvalue = stringvalueArray[0][0] + "n"
        else:
            stringvalue = stringvalueArray[0][0] + stringvalueArray[1][0]
        stringvalue = stringvalue+str(i)
        if stringvalue in hash_map:
            if hash_map[stringvalue] != [numbers[0],numbers[1]]:
                
                hash_map[stringvalue] =  [numbers[0],numbers[1]]
        else:
            hash_map[stringvalue] =  [numbers[0],numbers[1]]
    i=0

    boardsfen = create_board_from_hash_map(hash_map)
    board.set_fen(boardsfen)

    stockfish.set_fen_position(boardsfen)
    #result = engine.play(board, chess.engine.Limit(depth=20, time=10))
    result = stockfish.get_best_move()
    moove=result

    print(result)
    print(board)

    print("########################")

    time.sleep(1)

        



thread.join()
driver.quit()


