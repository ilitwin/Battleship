#BATTLESHIP GAME

import tkinter
from tkinter import Canvas

# N: size of grid side
N = 10

EMPTY = 0
SHIP = 1
HIT = 2
MISS = 3

SHIP_SIZES = {'CARRIER': 5, 'BATTLESHIP': 4, 'CRUISER': 3, 'SUBMARINE': 3, 
                                                                'DESTROYER': 2}

### GLOBALS FOR THE VIEW ###
LEFT_TOP_MARGIN = 40
BOTTOM_RIGHT_MARGIN = 20
GUESS_BOX_SIZE = 20
PLAY_BOX_SIZE = 30
GUESS_BOARD_OFFSET = GUESS_BOX_SIZE * N
PLAY_BOARD_OFFSET = PLAY_BOX_SIZE * N
WIDTH = BOTTOM_RIGHT_MARGIN+LEFT_TOP_MARGIN+N*GUESS_BOX_SIZE+N*PLAY_BOX_SIZE
HEIGHT = BOTTOM_RIGHT_MARGIN+LEFT_TOP_MARGIN+N*GUESS_BOX_SIZE+N*PLAY_BOX_SIZE
CIRCLE_WIDTH = 20

WINDOW = tkinter.Tk() # Initialization of canvas using tkinter
CANVAS = Canvas(WINDOW, width=WIDTH, height=HEIGHT)
CANVAS.pack()

####### MODEL #######

# creates a 2-dimensional N by N list of 0s
# @return {2D list}
def init_board():
    board = []
    for row in range(N):
        board.append([EMPTY]*N)
    return board

# checks that coordinates of ship are within the bounds of the board
# @param ship {list} list of tuple coordinates
# @return {boolean}
def is_ship_on_board(ship): 
    for i in range(len(ship)):
        if ship[i][0] not in range(N) or ship[i][1] not in range(N): 
            return False 
    return True

# checks if the letter (row) of all the coordinates of a ship are the same
# @param ship {list} list of tuple coordinates
# @return {boolean}
def same_row(ship):
    for i in range(len(ship)):
        if ship[0][0] != ship[i][0]:
            return False
    return True

# checks if the number (column) of all the coordinates of a ship are the same
# @param ship {list} list of tuple coordinates
# @return {boolean}
def same_column(ship):
    for i in range(len(ship)):
        if ship[0][1] != ship[i][1]:
            return False
    return True

# checks that ship:
#     - is completely vertical OR completely horizontal
#     - has correct size
#     - occupies consecutive squares on board
# @param ship {list} list of tuple coordinates
# @param size {int}
# @return {boolean}
def is_valid_ship(ship, size):
    if same_column(ship) != True and same_row(ship) != True: # checks if 
                      # the ship is completely vertical OR completely horizontal
        return False
    if len(ship) != size: # checks if the ship has correct size
        return False
    if is_ship_on_board(ship) != True: # checks if the ship is within the board
        return False
    ship.sort() # sorts the coordinates
    if same_row(ship) == True: # when the ship is vertical
        for i in range(size-1):
            if ship[i][1] != ship[i+1][1] - 1: # checks if cols are in 
                                                            # ascending order
                return False
    if same_column(ship) == True: # when the ship is horizontal
        for j in range(size-1):
            if ship[j][0] != ship[j+1][0] - 1: # checks if rows are in 
                                                            # ascending order
                return False
    return True

# checks that all coordinates of a ship are unoccupied
# @params ship {list} list of tuple coordinates
# @params board {2D list}
# @return {boolean}
def is_valid_placement(ship, board):
    count = 0
    for i in range(len(ship)):
        if board[ship[i][0]][ship[i][1]] == EMPTY:
            count = count + 1
    if count == len(ship):
        return True # all of the squares the ship tries to occupy are empty
    else:
        return False

# updates board by marking all coordinates that the ship occupies
# @param ship {list} list of tuple coordinates
# @param board {2D list}
# @return {None}
def place_ship(ship, board):
    for i in range(len(ship)):
        board[ship[i][0]][ship[i][1]] = SHIP
    return None

# marks hit on board at given coordinate
# @param board {2D list}
# @param row {int}
# @param col {int}
# @return {None}  
def mark_hit(board, row, col): # used on both guess boards and play boards
    board[row][col] = HIT
    return None

# marks miss on board at given coordinate
# @param board {2D list}
# @param row {int}
# @param col {int}
# @return {None}  
def mark_miss(board, row, col): # only used on guess boards
    board[row][col] = MISS
    return None

# checks if board at given coordinate is a hit
# @param board {2D list} 
# @param row {int}
# @param col {int}
# @return {boolean}
def is_hit(board, row, col):
    if board[row][col]== SHIP:
        return True
    else:
        return False

# checks if board at given coordinate is a miss
# @param board {2D list}
# @param row {int}
# @param col {int}
# @return {boolean}
def is_miss(board, row, col):
    if board[row][col] == EMPTY:
        return True
    else:
        return False

# removes location from relevant ship in opponent's dictionary
# @param opponent_dict {dict} opponent's ships
# @param player {int} current player either 1 or 2
# @param row {int}
# @param col {int}
# @return {None}
def remove_location(opponent_dict, opponent, row, col):
    coordinate = (row,col)
    list_of_sunk_ships = [] #list of names of sunk ships
    count = 0 #initialized the count of time coordinates are found 
                                                            #in opponent_dict
    for ship_names in opponent_dict.keys():
        if opponent_dict[ship_names] == []: 
            list_of_sunk_ships = list_of_sunk_ships + [ship_names] #update the 
                                                  #list of names of sunk ships
    for key in opponent_dict.keys():
        if coordinate in opponent_dict[key]:
            count = count + 1
            opponent_dict[key].remove(coordinate) #ship has been sunk
            if (opponent_dict[key] == []) and (key not in list_of_sunk_ships):
                print('YOU SUNK PLAYER', str(opponent) + "'S", key)
    if count == 0:
        print('ERROR: COORDINATE NOT FOUND')
    return None

# checks if all the ships in the dictionary are empty
# @param ship_dict {dict}
# @return {boolean}
def all_ships_sunk(ship_dict):
    for key in ship_dict.keys():
        if ship_dict[key] != []: 
            return False   
    return True

####### VIEW #######

# draws guess board
# @param board {2D list} a guess board
# @param start_x {int} pixel x-value at which to start drawing
# @param start_y {int} pixel y-value at which to start drawing
# @return {None}
def draw_guess_board(board, start_x, start_y):
    # draw the rectangle as a background
    CANVAS.create_rectangle(start_x, start_y, start_x+GUESS_BOARD_OFFSET, 
                start_y+GUESS_BOARD_OFFSET, fill = "white", width = 3) 
    # draw 9 horizontal lines
    CANVAS.create_line(start_x, start_y+GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+GUESS_BOX_SIZE, width = 3) 
    CANVAS.create_line(start_x, start_y+2*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+2*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+3*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+3*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+4*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+4*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+5*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+5*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+6*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+6*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+7*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+7*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+8*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+8*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+9*GUESS_BOX_SIZE, 
                start_x+N*GUESS_BOX_SIZE, start_y+9*GUESS_BOX_SIZE, width = 3)
    # draw 9 vertical lines
    CANVAS.create_line(start_x+GUESS_BOX_SIZE, start_y, 
                start_x+GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+2*GUESS_BOX_SIZE, start_y, 
                start_x+2*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+3*GUESS_BOX_SIZE, start_y, 
                start_x+3*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+4*GUESS_BOX_SIZE, start_y, 
                start_x+4*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+5*GUESS_BOX_SIZE, start_y, 
                start_x+5*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+6*GUESS_BOX_SIZE, start_y, 
                start_x+6*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+7*GUESS_BOX_SIZE, start_y, 
                start_x+7*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+8*GUESS_BOX_SIZE, start_y, 
                start_x+8*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+9*GUESS_BOX_SIZE, start_y, 
                start_x+9*GUESS_BOX_SIZE, start_y+N*GUESS_BOX_SIZE, width = 3)
    # color the boxes on the game grid
    for row in range(N):
        for col in range(N):
            left = col*GUESS_BOX_SIZE+start_x # left edge of the box 
                                                                 # to be colored
            right = (col+1)*GUESS_BOX_SIZE+start_x # right edge of the box 
                                                                 # to be colored
            top = row*GUESS_BOX_SIZE+start_y # top edge of the box to be colored
            bottom = (row+1)*GUESS_BOX_SIZE+start_y # bottom edge of the box 
                                                                 # to be colored
            if board[row][col] == HIT: # hit square is red
                CANVAS.create_rectangle(left, top, right, bottom,
                                      fill="red",width = 3)
            elif board[row][col] == MISS:# miss square is blue
                CANVAS.create_rectangle(left, top, right, bottom,
                                      fill="blue",width = 3)
            else: # empty square is white
                CANVAS.create_rectangle(left, top, right, bottom,
                                      fill="white",width = 3)
    return None

# draws play board
# @param board {2D list} a play board
# @param start_x {int} pixel x-value at which to start drawing
# @param start_y {int} pixel y-value at which to start drawing
# @return {None}
def draw_play_board(board, start_x, start_y):
    # draw the rectangle as a background
    CANVAS.create_rectangle(start_x, start_y, start_x+PLAY_BOARD_OFFSET, 
                start_y+PLAY_BOARD_OFFSET, fill = "white", width = 3) 
    # draw 9 horizontal lines
    CANVAS.create_line(start_x, start_y+PLAY_BOX_SIZE, N*PLAY_BOX_SIZE, 
                start_y+PLAY_BOX_SIZE, width = 3) 
    CANVAS.create_line(start_x, start_y+2*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+2*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+3*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+3*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+4*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+4*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+5*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+5*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+6*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+6*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+7*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+7*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+8*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+8*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x, start_y+9*PLAY_BOX_SIZE, 
                start_x+N*PLAY_BOX_SIZE, start_y+9*PLAY_BOX_SIZE, width = 3)
    # draw 9 vertical lines
    CANVAS.create_line(start_x+PLAY_BOX_SIZE, start_y, 
                start_x+PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3) 
    CANVAS.create_line(start_x+2*PLAY_BOX_SIZE, start_y, 
                start_x+2*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+3*PLAY_BOX_SIZE, start_y, 
                start_x+3*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+4*PLAY_BOX_SIZE, start_y, 
                start_x+4*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+5*PLAY_BOX_SIZE, start_y, 
                start_x+5*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+6*PLAY_BOX_SIZE, start_y, 
                start_x+6*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+7*PLAY_BOX_SIZE, start_y, 
                start_x+7*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+8*PLAY_BOX_SIZE, start_y, 
                start_x+8*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    CANVAS.create_line(start_x+9*PLAY_BOX_SIZE, start_y, 
                start_x+9*PLAY_BOX_SIZE, start_y+N*PLAY_BOX_SIZE, width = 3)
    # color the boxes on the game grid
    for row in range(N):
        for col in range(N):
            left = col*PLAY_BOX_SIZE+start_x # left edge of the box 
                                                                # to be colored
            right = (col+1)*PLAY_BOX_SIZE+start_x # right edge of the box 
                                                                # to be colored
            top = row*PLAY_BOX_SIZE+start_y # top edge of the box to be colored
            bottom = (row+1)*PLAY_BOX_SIZE+start_y # bottom edge of the box 
                                                                # to be colored
            if board[row][col] == HIT: # hit square is red
                CANVAS.create_rectangle(left, top, right, bottom,
                                      fill="red",width = 3)
            elif board[row][col] == SHIP: # square with a ship is gray
                CANVAS.create_rectangle(left, top, right, bottom,
                                      fill="gray",width = 3)
            else: # empty square is white
                CANVAS.create_rectangle(left, top, right, bottom,
                                      fill="white",width = 3)
    return None

# draws coordinates along left and top of board
# @param start_x {int} pixel x-value for the board's left edge
# @param start_y {int} pixel y-value for the board's top edge
# @param box_width {int} width of a single box for the relevant board
#        corresponds to the number of pixels between letters/numbers
# @param font_size {int} size of font letters/numbers will be drawn in
# @return {None} 
def draw_coords(start_x,start_y,box_width,font_size): 
    letters=['A','B','C','D','E','F','G','H','I','J'] 
    for col in range(N): # prints numbers on the top side of the board. 
          # Numbers are above the edge of the grid in the distance of font_size.
          # They are distributed in the equal distance from each other.
        CANVAS.create_text(start_x+0.5*box_width+col*box_width, 
        start_y-font_size, text=col, font = ("Courier New", font_size, "bold"), 
                                                                fill = "black")
    for row in range(N): # prints letter on the left side of the board. 
          # Letter are to the left of the edge of the grid in the distance of 
          # font_size. They are distributed in the equal distance from 
                                                                   # each other.
        CANVAS.create_text(start_x-font_size, 
                    start_y+0.5*box_width+row*box_width, text=letters[row], 
                    font = ("Courier New", font_size, "bold"), fill = "black")
    return None

# draws list of opponents ships and marks which have been sunk
# @param opponent_dict {dict} opponent's ship dictionary
# @param start_x {int} pixel x-value at which to start drawing
# @param start_y {int} pixel y-value at which to start drawing
# @return {None}
def draw_ships(opponent_dict, start_x, start_y):
    font_size=12
    x0=start_x # top left corner of the circle
    y0=start_y # top left corner of the circle
    x1=start_x+CIRCLE_WIDTH # bottom right corner of the circle
    y1=start_y+CIRCLE_WIDTH # bottom right corner of the circle 

    if 'CARRIER' in opponent_dict.keys() and opponent_dict["CARRIER"]==[]: 
                                                            # the ship is sunk 
        color='red' # color of the circle fill 
    else:
        color='white' # color of the circle fill 
    CANVAS.create_oval(x0, y0, x1, y1, outline = "black", fill = color, 
                                                                    width = 1)
    text_to_print='CARRIER'+' '+'('+str(SHIP_SIZES['CARRIER'])+')' 
                                              # name of the ship and its length 
    CANVAS.create_text(x1+CIRCLE_WIDTH*3, (y0+y1)/2, text=text_to_print, 
                    font = ("Courier New", font_size, "bold"), fill = "black") 
              # print the text in the distance of 2*circle width from the circle


    if 'BATTLESHIP' in opponent_dict.keys() and opponent_dict["BATTLESHIP"]==[]:
                                                             # the ship is sunk 
        color='red' # color of the circle fill 
    else:
        color='white' # color of the circle fill 
    CANVAS.create_oval(x0, y0+2*CIRCLE_WIDTH, x1, y1+2*CIRCLE_WIDTH, 
                outline = "black", fill = color, width = 1) # draw the circle  
    text_to_print='BATTLESHIP'+' '+'('+str(SHIP_SIZES['BATTLESHIP'])+')' 
                                             # name of the ship and its length 
    CANVAS.create_text(x1+CIRCLE_WIDTH*3, 
                (y0+2*CIRCLE_WIDTH+y1+2*CIRCLE_WIDTH)/2, text=text_to_print, 
                     font = ("Courier New", font_size, "bold"), fill = "black") 
              # print the text in the distance of 2*circle width from the circle

    if 'CRUISER' in opponent_dict.keys() and opponent_dict["CRUISER"]==[]: 
                                                             # the ship is sunk 
        color='red' # color of the circle fill 
    else:
        color='white' # color of the circle fill 
    CANVAS.create_oval(x0, y0+4*CIRCLE_WIDTH, x1, y1+4*CIRCLE_WIDTH, 
                outline = "black", fill = color, width = 1)  # draw the circle
    text_to_print='CRUISER'+' '+'('+str(SHIP_SIZES['CRUISER'])+')' 
                                             # name of the ship and its length 
    CANVAS.create_text(x1+CIRCLE_WIDTH*3, 
                    (y0+4*CIRCLE_WIDTH+y1+4*CIRCLE_WIDTH)/2, text=text_to_print,
                     font = ("Courier New", font_size, "bold"), fill = "black") 
             # print the text in the distance of 2*circle width from the circle

    if 'SUBMARINE' in opponent_dict.keys() and opponent_dict["SUBMARINE"]==[]: 
                                                             # the ship is sunk 
        color='red' # color of the circle fill 
    else:
        color='white' # color of the circle fill 
    CANVAS.create_oval(x0, y0+6*CIRCLE_WIDTH, x1, y1+6*CIRCLE_WIDTH, 
                outline = "black", fill = color, width = 1)  # draw the circle
    text_to_print='SUBMARINE'+' '+'('+str(SHIP_SIZES['SUBMARINE'])+')' 
                                             # name of the ship and its length 
    CANVAS.create_text(x1+CIRCLE_WIDTH*3, 
                    (y0+6*CIRCLE_WIDTH+y1+6*CIRCLE_WIDTH)/2, text=text_to_print,
                     font = ("Courier New", font_size, "bold"), fill = "black") 
             # print the text in the distance of 2*circle width from the circle 

    if 'DESTROYER' in opponent_dict.keys() and opponent_dict["DESTROYER"]==[]: 
                                                            # the ship is sunk 
        color='red' # color of the circle fill 
    else:
        color='white' # color of the circle fill 
    CANVAS.create_oval(x0, y0+8*CIRCLE_WIDTH, x1, y1+8*CIRCLE_WIDTH, 
                 outline = "black", fill = color, width = 1)  # draw the circle
    text_to_print='DESTROYER'+' '+'('+str(SHIP_SIZES['DESTROYER'])+')' 
                                             # name of the ship and its length 
    CANVAS.create_text(x1+CIRCLE_WIDTH*3, 
                    (y0+8*CIRCLE_WIDTH+y1+8*CIRCLE_WIDTH)/2, text=text_to_print,
                     font = ("Courier New", font_size, "bold"), fill = "black")
             # print the text in the distance of 2*circle width from the circle 
    return None

# draws splash screen between turns, displays hit/miss and next player
# @param player {int} current player either 1 or 2
# @param hit {boolean} True if turn resulted in a hit, False if it's a miss
# @return {None}
def draw_splash_screen(player, hit):
    CANVAS.create_rectangle(0, 0, WIDTH, HEIGHT, fill = "white", width = 1, 
         outline='white') # draws a screen to overwrite everything on the canvas
    if hit == True:
        text_to_print1= "HIT!"
    else:
        text_to_print1= "MISS!"
    CANVAS.create_text(WIDTH/2, HEIGHT/2-CIRCLE_WIDTH, text=text_to_print1, 
            font = ("Courier New", 40, "bold"), fill = "black", anchor='center')
                                                 # print the first line of text
    if player==1:
        next_player=2
    else:
        next_player=1
    text_to_print2='PLAYER'+' '+str(next_player)+' '+'BEGIN TURN'
    CANVAS.create_text(WIDTH/2, HEIGHT/2+CIRCLE_WIDTH, text=text_to_print2,
             font = ("Courier New", 20, "bold"), fill ="black", anchor='center')
                                                # print the second line of text
    return None

# draws entire display: guess board and coordinates,
# play board and coordinates, and ships.
# @param player {int} current player either 1 or 2
# @return {None}
def display_board(player):
    guess_board = get_player_guess_board(player)
    play_board = get_player_play_board(player)
    opponent_dict = get_player_ships(get_opponent(player))

    CANVAS.delete(tkinter.ALL)
    CANVAS.create_rectangle(0, 0, WIDTH, HEIGHT, fill="white", width = 0, 
                                    outline='white') # creates the background
    draw_guess_board(guess_board, LEFT_TOP_MARGIN, LEFT_TOP_MARGIN) 
                                                     # draws the guess board
    draw_coords(LEFT_TOP_MARGIN,LEFT_TOP_MARGIN,GUESS_BOX_SIZE,10) 
                                        # draws coordinates for the guess board
    draw_play_board(play_board, LEFT_TOP_MARGIN+N*GUESS_BOX_SIZE, 
                        LEFT_TOP_MARGIN+N*GUESS_BOX_SIZE) # draws the play board
    draw_coords(LEFT_TOP_MARGIN+N*GUESS_BOX_SIZE, 
                        LEFT_TOP_MARGIN+N*GUESS_BOX_SIZE, PLAY_BOX_SIZE,16) 
                                        # draws coordinates for the play board
    draw_ships(opponent_dict, LEFT_TOP_MARGIN, 
                        2*LEFT_TOP_MARGIN+N*GUESS_BOX_SIZE) # draws an overview
                                          # of the state of the opponent’s ships
    WINDOW.update() 

####### CONTROLLER #######

# initializes global variables: 4 boards and 2 dictionaries
# @return {None}
def init_game():
    global PLAYER1_GUESS_BOARD, PLAYER1_PLAY_BOARD 
    global PLAYER2_GUESS_BOARD, PLAYER2_PLAY_BOARD
    global PLAYER1_SHIPS, PLAYER2_SHIPS
    PLAYER1_GUESS_BOARD= init_board() # a board of empty cells  
    PLAYER1_PLAY_BOARD= init_board() # a board of empty cells  
    PLAYER2_GUESS_BOARD= init_board() # a board of empty cells  
    PLAYER2_PLAY_BOARD= init_board() # a board of empty cells  
    PLAYER1_SHIPS={}
    PLAYER2_SHIPS={}
    return None

# returns the given player's ship dictionary
# @param player {int} current player either 1 or 2
# @return {dict}
def get_player_ships(player):
    if player == 1:
        return PLAYER1_SHIPS
    else:
        return PLAYER2_SHIPS

# returns the given player's guess board
# @param player {int} current player either 1 or 2
# @return {2D list}
def get_player_guess_board(player):
    if player == 1:
        return PLAYER1_GUESS_BOARD
    else:
        return PLAYER2_GUESS_BOARD
  
# returns the given player's play board
# @param player {int} current player either 1 or 2
# @return {2D list}
def get_player_play_board(player):
    if player == 1:
        return PLAYER1_PLAY_BOARD
    else:
        return PLAYER2_PLAY_BOARD

# returns the number corresponding to the opposite player
# @param player {int} current player either 1 or 2
# @return {int} opposite player
def get_opponent(player):
    if player==1:
        opponent=2
    else:
        opponent=1
    return opponent

# checks if the input from the user is valid for a ship:
#   - input_list is not empty
#   - length of each string in the input is 2
#   - first element of each is a letter 'A' through 'J'
#   - second element of each is a number 0 through 9
# @param input_list {list} list of strings
# @return {boolean}
def is_valid_ship_input(input_list):
    list_of_letters=['A','B','C','D','E','F','G','H','I','J']
    list_of_numbers=['0','1','2','3','4','5','6','7','8','9']
    if input_list==[]: 
        return False
    else:
        for i in range(len(input_list)):
            if len(input_list[i])!=2:
                return False
            if input_list[i][0] not in list_of_letters:
                return False
            if input_list[i][1] not in list_of_numbers:
                return False
    return True

# converts input from list of strings into list of integer tuple coord. pairs
# @param input_list {list} list of strings
# @return {list} list of coordinate tuples 
def convert_input(input_list):
    letters_dictionary={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
                                                                    'I':8,'J':9}
    new_list=[] # initializes the list of coordinate tuples
    for i in range(len(input_list)):
        coordinate = (letters_dictionary[input_list[i][0]],
                                                     int(input_list[i][1]))
        new_list=new_list+[coordinate]
    return new_list

# runs loop prompting player to input locations for their ships and placing 
                                                    # them on their play board
# @param player {int} current player either 1 or 2
# @param board {2D list} current player's play board
# @param ship_dict {dict} current player's ship dictionary
# @return {None}
def pick_ships(player, board, ship_dict):
    print("PLAYER {}, PLACE YOUR SHIPS".format(player)) 
    for (name,size) in SHIP_SIZES.items(): # prompts the player to input the 
                                                # list of points for each ship
        inp = input("PLACE A SHIP OF SIZE {}: ".format(size))
        input_list = inp.split()
        while not (is_valid_ship_input(input_list) and 
                           is_valid_ship(convert_input(input_list),size) and 
                           is_valid_placement(convert_input(input_list),board)):
                # loops till the player inputs a valid list of points for a ship
            print("INVALID SHIP, TRY AGAIN")
            inp = input("PLACE A SHIP OF SIZE {}: ".format(size))
            input_list = inp.split() 
        new_list=convert_input(input_list) # converts the player's input into 
                                                             # a coordinate list
        if player==1:
            ship_dict=PLAYER1_SHIPS
            place_ship(new_list, PLAYER1_PLAY_BOARD) # places the ship on 
                                                            # the player's board
            if size==5:
                PLAYER1_SHIPS['CARRIER']=new_list # assignes the coordinates of 
                                              # the ship to the name of the ship
            if size==4:
                PLAYER1_SHIPS['BATTLESHIP']=new_list
            if size==2:
                PLAYER1_SHIPS['DESTROYER']=new_list
            if size==3: # there are 2 ships with the lenght of 3
                if 'CRUISER' in PLAYER1_SHIPS.keys():
                    PLAYER1_SHIPS['SUBMARINE']=new_list
                else:
                    PLAYER1_SHIPS['CRUISER']=new_list
            display_board(1)
        if player==2:
            ship_dict=PLAYER2_SHIPS
            place_ship(new_list, PLAYER2_PLAY_BOARD) # places the ship on the 
                                                                # player's board
            if size==5:
                PLAYER2_SHIPS['CARRIER']=new_list # assignes the coordinates 
                                           # of the ship to the name of the ship
            if size==4:
                PLAYER2_SHIPS['BATTLESHIP']=new_list
            if size==2:
                PLAYER2_SHIPS['DESTROYER']=new_list
            if size==3: # there are 2 ships with the lenght of 3
                if 'CRUISER' in PLAYER2_SHIPS.keys():
                    PLAYER2_SHIPS['SUBMARINE']=new_list
                else:
                    PLAYER2_SHIPS['CRUISER']=new_list
            display_board(2)
    print("ALL SHIPS HAVE BEEN PLACED")
    return None

# checks if the input from the user is valid for a target:
#   - length is 2
#   - first element is a letter 'A' through 'J'
#   - second element is a number 0 through 9
# @param move {str} input for a target to hit
# @return {boolean} 
def is_valid_move_input(move):
    if len(move)!=2:
        return False
    if move[0] not in ['A','B','C','D','E','F','G','H','I','J']:
        return False
    if move[1] not in ['0','1','2','3','4','5','6','7','8','9']:
        return False
    return True

# checks if a move is valid for the given board
# @param board {2D list} current player's guess board
# @param row {int} 
# @param col {int}
# @return {boolean}
def is_valid_move(board, row, col):
    if board[row][col]==MISS or board[row][col]==HIT: # the player 
                                            # cannot choose a hit or a miss cell
        return False
    return True

# checks if all of either player's ships are sunk
# @return {boolean}
def is_end_game():
    if all_ships_sunk(PLAYER1_SHIPS) == True:
        print('GAME OVER')
        print('PLAYER 2 WON')
        return True
    if all_ships_sunk(PLAYER2_SHIPS) == True:
        print('GAME OVER')
        print('PLAYER 1 WON')
        return True
    else:
        return False

# quits the game -- nothing to modify here
def quit_game():
    print("GOODBYE!")
    try: WINDOW.destroy()
    except: return None
  
# game play loop for entire game 
# @return {None}  
def play_game():
    init_game()
    display_board(1) 
    pick_ships(1, PLAYER1_PLAY_BOARD, PLAYER1_SHIPS) # Player 1 picks the ships
    display_board(2)
    pick_ships(2, PLAYER2_PLAY_BOARD, PLAYER2_SHIPS) # Player 2 picks the ships
    player=1 # initializes the player
    while not is_end_game(): 
        display_board(player)
        # Loop for continually getting move from a a player until valid. 
        move = input("PLAYER {} ENTER A COORDINATE TO STRIKE: ".format(player))
        while not (is_valid_move_input(move) and 
                                is_valid_move(get_player_guess_board(player),
                                                 ord(move[0])-65,int(move[1]))):
            print("INVALID MOVE, TRY AGAIN")
            move = input("PLAYER {} ENTER A COORDINATE TO STRIKE: ".
                                                                format(player))
        new_list=convert_input([move]) # convert the move to a list with one  
                                                                   # coordinate
        if get_opponent(player)==2: # for Player 1
            if is_hit(PLAYER2_PLAY_BOARD, new_list[0][0], new_list[0][1])==True:
                mark_hit(PLAYER2_PLAY_BOARD, new_list[0][0], new_list[0][1]) 
                                            # mark hit on opponent's play board
                mark_hit(PLAYER1_GUESS_BOARD, new_list[0][0], new_list[0][1]) 
                                            # mark hit on Player 1's guess board
                remove_location(PLAYER2_SHIPS, 2, new_list[0][0],new_list[0][1])
                print("HIT")
                draw_splash_screen(1, True) # draw a 'HIT' screen asking 
                                                             # Player 2 to begin
            if is_miss(PLAYER2_PLAY_BOARD, new_list[0][0],new_list[0][1])==True:
                mark_miss(PLAYER1_GUESS_BOARD, new_list[0][0], new_list[0][1]) 
                                           # mark miss on Player 1's guess board
                print("MISS")  
                draw_splash_screen(1, False) # draw a 'MISS' screen asking 
                                                             # Player 2 to begin
        if get_opponent(player)==1: # for Player 2
            if is_hit(PLAYER1_PLAY_BOARD, new_list[0][0], new_list[0][1])==True:
                mark_hit(PLAYER1_PLAY_BOARD, new_list[0][0], new_list[0][1]) 
                                             # mark hit on opponent's play board
                mark_hit(PLAYER2_GUESS_BOARD, new_list[0][0], new_list[0][1]) 
                                            # mark hit on Player 2's guess board
                remove_location(PLAYER1_SHIPS, 1, new_list[0][0],new_list[0][1])
                print("HIT")
                draw_splash_screen(2, True) # draw a 'HIT' screen asking 
                                                             # Player 1 to begin
            if is_miss(PLAYER1_PLAY_BOARD, new_list[0][0],new_list[0][1])==True:
                mark_miss(PLAYER2_GUESS_BOARD, new_list[0][0], new_list[0][1]) 
                                           # mark miss on Player 2's guess board
                print("MISS")    
                draw_splash_screen(2, False) # draw a 'MISS' screen asking 
                                                             # Player 1 to begin
        input("Press ENTER to begin your turn: ")
        player=get_opponent(player) # switch the player 
    quit_game()

