# Battleship

Battleship is a two player game in which players place ships on a grid and take 
turns guessing at the location of their opponent’s ships. The goal is to be the 
first player to guess all the locations of each of the opponent’s ships, or to 
sink each of them.

The game has two 10 x 10 grids, or boards, for each player. For each player, 
one of the boards, called the play board, manages the locations of the player’s 
ships and records the hits they receive from the opposing player. The second 
board, called the guess board, only records the player’s hits and misses 
(guesses) on the opponent’s ships. Each player cannot see their opponent’s 
arrangement of ships.

Ships are represented as consecutive squares on a board, arranged either 
horizontally or vertically. Ships cannot overlap on a given board. Each player 
has 5 ships, each of which has a different fixed size, meaning the number of 
squares occupied. The 5 ships are: Carrier (size 5), Battleship (size 4), 
Cruiser (size 3), Submarine (size 3), and Destroyer (size 2). Before the game 
starts, each player places their 5 ships on their play board without the 
opponent’s knowledge of where they are placing them.

In each turn, the current player picks a target space on the opponent’s board
to try and strike one of their ships. The player receives feedback as to 
whether their guess was a hit or a miss. If the player successfully hits one 
of the opponent’s ships, then in the following turns, the relevant square is 
colored red on both the player’s guess board and the opponent’s play board. 
Otherwise if the target was a miss, the square will be marked blue only on 
the player’s guess board, and nothing will change on the opponent’s play 
board. When all squares of a player’s ship have been hit, the ship is sunk. 
When all the ships of a given player are sunk, the game ends and the opponent 
wins the game.

In my code, each board (guess boards and play boards for each player 1 and 
player 2) is a 2-dimensional list where each element in the list represents 
a square on the Battleship grid. The contents of the board are as follows:

0 represents a square that is essentially empty, meaning it has no ship on the 
play board, and no hit or miss on the guess board.

1 represents a square that is occupied by a ship, but has not been hit.

2 represents a square that has been hit (on the current player’s play board 
this means one of the current player’s ships has been hit at the given 
location, on the current player’s guess board this means the current player hit 
one of the opponent’s ships at this location).

3 represents a square that is a miss (this can only occur on the guess board 
of each player).

Also, individual ships are represented as lists of tuples where the tuples are 
row, column coordinate pairs. Each players ships are contained in a dictionary 
mapping each ship’s name to it’s list representation. In addition, the 
dictionary SHIP SIZES maps the names of the 5 ships to their lengths and 
players are represented by integers 1 and 2 for Player1 and Player2, 
respectively.

—

For the MODEL part, I wrote a set of functions which handle the Python 
representation of the Battleship game:

1.1 init board() returns the initial list of all 0's that we will be using as 
our model to represent a 10 x 10 board

1.2 is ship on board(ship) takes in ship (the coordinate list of a ship, as 
represented in the way we described above), and returns True if all coordinates 
of the ship fall within the range of the 10 x 10 board and False otherwise.

1.3 same row(ship) and same column(ship): The function same row(ship) returns 
True if all squares the ship occupies are in the same row and False otherwise.
The function same column(ship) returns True if all squares the ship occupies 
are in the same column and False otherwise.

1.4 is valid ship(ship, size) takes in ship (the coordinate list of a ship), 
and size (the size this ship is based on the type of ship the coordinate 
list corresponds to). The function returns True if the ship is arranged
either completely horizontally or completely vertically, the ship size 
corresponds to the number of coordinates it takes up, all ship coordinates are 
on the board and the ship occupies consecutive squares on the board. To check 
if the ship occupies consecutive squares on the board, I sorted the coordinates 
and checked that either the rows (if the ship is vertical) or columns (if the 
ship is horizontal) are in ascending order.

1.5 is valid placement(ship, board) takes in ship (the coordinate list of 
a ship), and board (the board onto which the ship is to be placed), and returns 
True if all of the squares that the ship tries to occupy on the board are empty 
and False otherwise.

1.6 place ship takes in ship (the coordinate list of a ship), and board 
(a play board), and modifies board so that the relevant coordinates show where 
the ship is. This function returns None. 

1.7 Functions mark hit(board, row, col) and mark miss(board, row, col); In mark 
hit, mark the square at the position specified by row and col to be a hit. In 
mark miss, mark the square to be a miss. Both functions return None. Also, 
mark hit will be used on both guess boards and play boards, while mark miss is 
only used on guess boards.

1.8 Functions is hit(board, row, col) and is miss(board, row, col); These 
functions determine the status of an attempted strike at the coordinates 
(row,col). In is hit, the function returns True if the square specified by 
row and col is filled by a ship and False otherwise. In is miss, the function 
returns True if the square is marked as empty and False otherwise. 

1.9 The function remove location(opponent dict, opponent, row, col) is used 
when a guess is a hit to one of the opponent’s ships, so we remove that 
coordinate from the ship list of the corresponding ship in the opponent’s 
dictionary of ships. This serves to keep track of how many spaces of a ship 
remain to be hit. When a ship list is emptied of all of its coordinates, 
it has been sunk. This function removes the coordinate (row, col) from the 
opponent’s corresponding ship’s coordinate list in opponent dict. If this 
coordinate is the last remaining coordinate occupied by the ship, that ship 
has been sunk. In this case, the function prints a message 
‘YOU SUNK PLAYER{opponent’s player number}’S {ship name}’. If the coordinate is 
not anywhere in the dictionary, the function prints
‘ERROR: COORDINATE NOT FOUND’. Then the function returns None.

1.10 all ships sunk(ship dict) takes in one of the player’s ship dictionary, 
and checks whether or not all of the ships in the dictionary are sunk. 
It returns True if all the ships are sunk (the coordinate list of the ship is
an empty list) and False otherwise. 

—

For the View part, I designed the display of your Battleship game. Grey 
corresponds to a ship, red corresponds to hits, and blue corresponds to misses.

2.1 draw_guess_board takes in board (the current player’s guess board), and 
start x and start y, the x-coordinate and y-coordinate of the upper left corner 
of the board. The function draws the given board. For a specific square, it is 
red if there is a hit on the square, and blue if there is a miss. Empty squares 
are colored white. 

2.2 draw_play_board draws play board which takes in board (the current player’s 
play board), and start x and start y, the x-coordinate and y-coordinate of the 
upper left corner of the board. The function draws the play board of the input 
player. For a specific square, it is red if it is hit by opponent and gray if 
it is occupied by a ship. Empty squares are colored white. 

2.3 draw_coords takes in start x and start y, the x-coordinate and 
y- coordinate of the upper left corner of the board they are displaying the 
coordinates for, box width, the length of the side of a single box of the 
board, and font size, the font size of the text. The function draws the 
letters (A-J) down the left side of the board, aligned with the rows of the 
board, and numbers (0-9) across the top of the board, aligned with the column. 

2.4 draw_ships takes in opponent dict (the opponent’s ship dictionary) and 
start x and start y, the x-coordinate and y-coordinate of the upper left corner 
of the ship list. The function draws an overview of the state of the opponent’s 
ships. The function draws the names of the ships next to circles. A circle is 
filled in with red when the corresponding ship has been sunk. The original size 
of each ship is displayed next to its name.

2.5 draw_splash_screen takes in player (the integer representing the player 
whose turn is next), and hit, a boolean value indicating whether the previous 
turn resulted in a hit or miss (True if hit, False if miss). The function draws 
a screen that overwrites everything on the canvas, and draws a message showing 
whether the past move was a hit or miss, and draw a message indicating the next 
player. 

2.6 display_board takes in player. The function draws the input player’s guess 
board, play board, and listing of opponent’s ships by calling draw_guess_board, 
draw_play_board, and draw_ships. Each function calls with arguments for the 
current player and desired start x and start y positions for each item. The 
function also draws the coordinates along the edges of both the guess board and 
the play board by calling draw_coords twice with the relevant arguments. At the 
beginning of the function, it deletes everything on the canvas, and at the end 
it updates the window. The first three lines given in the function retrieve the 
relevant global variables given a player. They are used to define variables 
guess board, play board, and opponent dict. 

—

The Controller part is responsible for taking user input from the terminal, 
updating the model accordingly, and calling the view functions to display the 
current state of the game to the users. The controller implements many actions:
- It prompts each player to input locations in which to place their ships.
- It verifies that the given input is valid and transferring the input to a 
representation consistent with
the model.
- It processes each player’s turn: (collects input for a target box on the 
board, shecks the validity of the input, then updating the model accordingly, 
displays the outcomes of each turn)
- It is responsible switching between players.
- It checks if the game has finished.

3.1 init_game takes no arguments and initializes the play board, guess board, 
and ship dictionary for both players. All four boards and both ship 
dictionaries have been initialized at the top of the function as global 
variables. This is so they may be modified by other functions without needing 
to be passed in as arguments or returned from each function. This function 
initializes each board using init board and initializes both dictionaries to 
be empty dictionaries. 

3.2 get_player_ships takes in an integer representing a player and returns 
this player’s ship dictionary.

3.3 get_player_guess board takes in an integer representing a player and 
returns this player’s guess board.

3.4 get_player_play board takes in an integer representing a player and returns 
this player’s play board.

3.5 get_opponent takes in an integer representing the current player and 
returns an integer representing the player’s opponent.

3.6 is_valid_ship_input takes in input list, a list of strings, where each 
string identifies a square on the board. The function returns True if the 
input is of the valid form. Each string should have two characters: The first 
one should be a letter (representing row number), and the second is a number 
(representing column number). Therefore, it checks if:
- The length of each string in the input list is 2.
– The first element is a capital letter ’A’ through ’J’ inclusive. 
– The second element is a number 0 through 9 inclusive.
– The input list is not empty.
The function does not check that the pairs are next to each other.

3.7 convert_input takes in input list, a list of strings, where each string 
identifies a square on a board by the letter-number string form. The function 
converts each string of the list to a tuple (row, col) that represents the 
actual row number and column number of the square on the board. The function 
returns the resulted new list of tuples that represents a ship.

3.8 pick_ships is responsible for prompting a player to place each of his/her 
ships on their play board, checking the validity of the given input, and 
placing each ship on the player’s play board. pick_ships takes player, an 
integer representing a player, board, the player’s board, and ship dict, the 
player’s ship dictionary. The function loops over each of the ships in the 
global SHIP SIZES and prompts the player to give input of the appropriate 
size. Each square is represented using the letter-number string form described 
in previous questions. For example, an input might look like ‘A0 A1 A2’. (The 
input function returns the user input in the form of a string and that the user 
will input coordinates without the quotations.) The while loop loops as long as 
the player has not given a valid input, using is_valid_ship_input, 
is_valid_ship and is_valid_placement and continues prompting the user until 
their input is valid. Once valid input is obtained for each ship, the function:
– Converts the input using convert input into a ship list.
– Places the ship on the board.
– Inserts the ship into the player’s ship dictionary, ship dict, with the ship 
name as the key and the ship list as the value.
– Displays the board for the given player so they can see their newly placed 
ship.

3.9 is_valid_move_input takes in move, a string representing a square on the 
board. The function returns True if the string follows the letter-number way 
of identifying a valid square on the board. A move is valid if:
– Its length is 2.
– The first element is a capital letter ’A’ through ’J’ inclusive. 
– The second element is a number 0 through 9 inclusive.

3.10 is_valid_move takes in board, the current player’s guess board, row, a row 
number, and col, a column number. The function returns True if the square 
specified by the row and col on board has not been hit or missed before.

3.11 is_end_game takes in no arguments and which returns True if either player 
has all of their ships sunk and False otherwise. If either player has all their 
ships sunk, the function prints a message to indicate that the game is over and 
who the winner is. 
                              
3.12 play_game is responsible for running the game play loop for the entire 
game. Before the loop begins, the function:
– Initializes the game by calling init game.
– Displays the board for Player1 and call pick ships for Player1. 
– Displays the board for Player2 and call pick ships for Player2. 
– Initializes the variable player to 1.

The game play loop is responsible for alternating turns until the game has 
finished. In each turn the function:
– Prompts the current player to input a coordinate of a square on the 
opponent’s board to strike.
– Converts the input into a row integer and a column integer.
– Determines if the given row and column are a hit or a miss on the opponent’s 
play board using
is hit and is miss. If it’s a hit, the function marks the hit on the opponent’s 
play board and on the current player’s guess board using mark hit and removes 
the hit coordinates from the opponent’s ship dictionary by calling remove 
location. It also prints ‘HIT’. If it’s a miss, the function marks the miss on 
the current player’s guess board using mark miss, and prints ‘MISS’.

Then the function:
– Switches and updates player at the end of the turn.
– Calls draw splash screen, and immediately after, uses the input function to 
prompt the new player to press enter to begin their turn.
When the loop has ended, the function calls quit game to end the game.

