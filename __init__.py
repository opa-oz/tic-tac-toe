from os import name, system
from constants import matrix, matrix_with_hint
import random


# Clean previous console input/output
def clean():
    # for windows
    if name == 'nt':
        system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        system('clear')
    print('Tic-tac Toe!')


# Is available to use the letter
def is_available_letter(letter=''):
    return letter.lower() in 'ox'


# Random choose - who is first (True - user, False - computer)
def is_player_should_turn_first():
    return random.randint(0, 1) == 0


# Is the row contains same letters
def is_cells_contain_the_same(board, indexes, letter):
    result = True
    for index in indexes:
        if board[index - 1] != letter:
            result = False

    return result


# Is this cell free
def is_space_free(board, move):
    return board[move - 1] != 'X' and board[move - 1] != 'O'


# Is board is full
def is_board_full(board):
    is_full = True
    for i in range(1, 10):
        if is_space_free(board, i):
            is_full = False

    return is_full


# Is player with `letter` is win
def is_winner(board, letter):
    return is_cells_contain_the_same(board, [7, 8, 9], letter) or \
           is_cells_contain_the_same(board, [4, 5, 6], letter) or \
           is_cells_contain_the_same(board, [1, 2, 3], letter) or \
           is_cells_contain_the_same(board, [7, 4, 1], letter) or \
           is_cells_contain_the_same(board, [8, 5, 2], letter) or \
           is_cells_contain_the_same(board, [9, 6, 3], letter) or \
           is_cells_contain_the_same(board, [7, 5, 3], letter) or \
           is_cells_contain_the_same(board, [1, 5, 9], letter)


# Set letter in cell
def make_move(board, cell, letter):
    board[cell - 1] = letter


# Ask for input 1-9
def get_player_move(board):
    print('What is your next cell? (1-9)')
    move = input()
    while move not in list('123456789') or not is_space_free(board, int(move)):
        print('Wrong number. Try again: (1-9)')
        move = input()

    return int(move)


# Get random move from possible move set and a board situation
def get_random_move(board, move_set):
    possible_moves = []
    for move in move_set:
        if is_space_free(board, move):
            possible_moves.append(move)

    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None


# Think as computer with a part of random
def get_computer_move(board, players):
    user, computer = players.values()

    # can the computer win?
    for i in range(1, 10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, i, computer)
            if is_winner(board_copy, computer):
                return i

    # can the player win?
    for i in range(1, 10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, i, user)
            if is_winner(board_copy, user):
                return i

    # can move in corners?
    move = get_random_move(board, [1, 3, 7, 9])
    if move is not None:
        return move

    # can move in center?
    if is_space_free(board, 5):
        return 5

    # can move in middles?
    move = get_random_move(board, [2, 4, 6, 8])
    if move is not None:
        return move


# Ask user to choose the letter
def select_letters():
    print('Choose a letter: (O/X)')
    letter = input().upper()
    while not is_available_letter(letter):
        print('Wrong letter. Try again: (O/X)')
        letter = input().upper()

    return {'user': 'X', 'computer': 'O'} if letter == 'X' else {'user': 'O', 'computer': 'X'}


# Copy board list
def get_board_copy(board):
    new_board = []
    for letter in board:
        new_board.append(letter)

    return new_board


# Draw board with or without hint
def draw_board(board, players, with_hint=False):
    clean()
    matrix_to_print = matrix_with_hint if with_hint else matrix
    print('{user}(User) | {computer}(Computer)'.format(user=players['user'], computer=players['computer']))
    print(matrix_to_print.format(
        cell1=board[0],
        cell2=board[1],
        cell3=board[2],
        cell4=board[3],
        cell5=board[4],
        cell6=board[5],
        cell7=board[6],
        cell8=board[7],
        cell9=board[8],
    ))


def main():
    while True:
        clean()

        board = list(' ' * 9)
        players = select_letters()
        is_player_first = is_player_should_turn_first()
        game_is_playing = True
        is_player_turn = is_player_first

        while game_is_playing:
            draw_board(board, players, is_player_turn)
            if is_player_turn:
                move = get_player_move(board)
                make_move(board, move, players['user'])

                if is_winner(board, players['user']):
                    draw_board(board, players)
                    print('You won! Yaaay!')
                    game_is_playing = False
                elif is_board_full(board):
                    draw_board(board, players)
                    print('Board is full, nobody won :(')
                    game_is_playing = False
            else:
                move = get_computer_move(board, players)
                print('Computer\'s turn: {}'.format(move))
                make_move(board, move, players['computer'])

                if is_winner(board, players['computer']):
                    draw_board(board, players)
                    print('Computer won :(')
                    game_is_playing = False
                elif is_board_full(board):
                    draw_board(board, players)
                    print('Board is full, nobody won :(')
                    game_is_playing = False

            is_player_turn = not is_player_turn

        print('Would you like to play again? (yes/no)')
        answer = input().lower()

        if answer not in ['yes', 'y']:
            break


main()
