#
#
# This is the Tic-Tac-Toe game
#
#

def printboard(number=0, mark=' ', matrix=None):
    """ Prints the board with the desired location and mark """

    while (number not in range(1, 10)) and mark != ' ':
        number = int(input('\nSorry, insert a number between 1 and 9: '))
    
    print('')
    y = 5
    win = 0
    
    if number != 0:
        matrix[number-1] = mark

    for x in range(1, 10):        
        print(f" { matrix[y+x] } ", end="")      
        if x in {3, 6}:
            print(f"\n-----------")
            y -= 6
        elif x != 9:
            print("|", end="")
    
    if all(v == matrix[0] for v in matrix[0:3]):
        win = 1
    elif all(v == matrix[3] for v in matrix[3:6]):
        win = 1
    elif all(v == matrix[6] for v in matrix[6:9]):
        win = 1
        
    elif all(v == matrix[0] for v in matrix[0:10:3]):
        win = 1
    elif all(v == matrix[1] for v in matrix[1:10:3]):
        win = 1
    elif all(v == matrix[2] for v in matrix[2:10:3]):
        win = 1
    
    elif all(v == matrix[0] for v in matrix[0:10:4]):
        win = 1
    elif all(v == matrix[2] for v in matrix[2:7:2]):
        win = 1

    print('\n')
    return (win, matrix)     

def first_selection(): # Ask for first location - Returns chosen number

    # Ask for location of first move.
    global matrix, game_won
    [game_won, matrix] = printboard(matrix=list(range(1, 10))) # Initialize board
    matrix_number = input("Ok Player 1, please choose the number from above "
                          f"where you want '{p1marker}' to be inserted: ")

    # If selected number is not correct, ask again.
    while matrix_number not in str(set(range(1, 10))):
        matrix_number = input(f"\nSorry, insert a number between 1 and 9: ")
    
    # Return the chosen number.
    return int(matrix_number)

def play_again():
    # Ask for input
    replay = input('Do you want to play agian - Yes/No? ').lower()

    # Check if input is correct, otherwise ask again
    while replay not in {'yes', 'no'}:
        print("Please, enter 'Yes' or 'No'")
        replay = input('Do you want to play agian - Yes/No? ').lower()
    
    # If yes, then play again
    if replay == 'yes':
        global matrix_number 
        matrix_number = first_selection() # Save chosen number location
    else:
        print("\nSee you later!\n")
    
    # Return the answer
    return replay

def selectmarker(): # Ask which marker players wants
    # Select marker
    p1marker = input("\tPlayer 1, please pick a marker 'X' or 'O' and hit Enter: ").upper()

    # Check if it is the correct input
    while not p1marker in {'X', 'O'}:
        print("\nWe are not starting good in here! I said:")
        p1marker = input("\tPlease pick a marker 'X' or 'O' and hit Enter: ").upper()

    if p1marker == 'X': 
        p2marker = 'O'
    else: 
        p2marker = 'X'

    return p1marker, p2marker

# Introduce and Initialize the game
replay = 'yes'
print('\n'*50) 
print("Welcome to Tic Tac Toe!")

# Start selection of markers
[p1marker, p2marker] = selectmarker()

# Make first move
matrix_number = first_selection()

# Start Loop
while replay == 'yes':

# Player 1 insertion:
    # Print board with player 1 selection
    [game_won, matrix] = printboard(matrix_number, p1marker, matrix) 

    # Check if player 1 wins
    if game_won:
        print('\n\n\t***** Player 1, you win! *****\n')
        replay = play_again()
        continue
        
# Player 2 insertion:
    # Ask for player 2 desired input
    matrix_number = int(input("Player 2, your turn. What's your move? "))

    # Print board with player 2 selection
    [game_won, matrix] = printboard(matrix_number, p2marker, matrix)

    # Check if player 2 wins
    if game_won:
        print('\n\n\t***** Player 2, you win! *****\n')
        replay = play_again()
        continue

# Ask for player 1 desired input
    matrix_number = int(input("Player 1, your turn. What's your move? "))
