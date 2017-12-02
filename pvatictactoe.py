#!/usr/bin/env python
#--------------------------------------------------------------------------
# Tic Tac Toe game in Python
# Author: Marina Vukovic
# Tested with Python 3
# TO RUN:
#         sudo chmod a+x tictactoe.py
#         ./tictactoe.py
# OR JUST RUN : python3 tictactoe.py
# ---------------------------------------------------------------------------


# import modules
import random
import sys
import copy

class Game:
    "Tic-Tac-Toe class. This class holds the user interaction, and game logic"
    def __init__(self):
        self.board = [' '] * 9
        self.player_name = ''
        self.player_mark = ''
        self.ai_name = 'AI'
        self.ai_mark = ''
        self.win_combinations = ([0, 1, 2], # Horizontal
                                 [3, 4, 5],
                                 [6, 7, 8],
                                 [0, 3, 6], # Vertical
                                 [1, 4, 7],
                                 [2, 5, 8],
                                 [0, 4, 8], # Diagonal
                                 [2, 4, 6])
        self.corners = [0,2,6,8]
        self.sides = [1,3,5,7]
        self.center = 4

        self.shape = '''
           \t| {} | {} | {} |
           \t-------------
           \t| {} | {} | {} |
           \t-------------
           \t| {} | {} | {} |
           '''                    

    def print_board(self, board = None):
        "Display board"
        if board is None:						
            print(self.shape.format(*tuple(self.board[6:9] + self.board[3:6] + self.board[0:3])))
        else:
            # when the game starts, display numbers on all the grids
            print(self.shape.format(*tuple(board[6:9] + board[3:6] + board[0:3])))

    def get_mark(self):
        mark = input("Would you like your mark to be X or O?: ").upper() 
        while mark not in ["X","O"]:
            mark = input("Would you like your mark to be X or O? :").upper()
        if mark == "X":
            return ('X', 'O')
        else:
            return ('O','X')

    def help(self):
        print('''
\n\t The game board has 9 sqaures(3X3).
\n\t Two players take turns in marking the spots/grids on the board.
\n\t The first player to have 3 pieces in a horizontal, vertical or diagonal row wins the game.
\n\t To place your mark in the desired square, simply type the number corresponding with the square on the grid 
 
\n\t Press Ctrl + C to quit
''')

    def quit_game(self):
        "exits game"
        self.print_board()
        print("\n\t Thanks for playing :-) \n\t Hope we'll play again soon!\n")
        sys.exit()

    def is_winner(self, board, mark):
        "check if this mark will win the game"
        # order of checks:
        #   1. across the horizontal top
        #   2. across the horizontal middle
        #   3. across the horizontal bottom
        #   4. across the vertical left
        #   5. across the vertical middle
        #   6. across the vertical right
        #   7. across first diagonal
        #   8. across second diagonal
        for combo in self.win_combinations:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == mark):
                return True
        return False

    def get_ai_move(self):
        '''
        find the best space on the board for the ai. Objective
        is to find a winning move, a blocking move or an equalizer move. 
        AI must always win
        '''
        # check if ai can win in the next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy,i,self.ai_mark)
                if self.is_winner(board_copy, self.ai_mark):
                    return i
                
        # check if player could win on his next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy, i, self.player_mark)
                if self.is_winner(board_copy, self.player_mark):
                    return i

        # check for space in the corners, and take it
        move = self.choose_random_move(self.corners)
        if move != None:
            return move

        # If the center is free, take it
        if self.is_space_free(self.board, self.center):
            return self.center


        # else, take one free space on the sides
        return self.choose_random_move(self.sides)

    def is_space_free(self, board, index):
        "checks for free space of the board"
        # print "SPACE {} is taken" {} index
        return board[index] == ' '

    def is_board_full(self):
        "checks if the board is full"
        for i in range(1,9):
            if self.is_space_free(self.board, i):
                return False
        return True

    def make_move(self, board, index, move):
        board[index] =  move

    def choose_random_move(self, move_list):
        possible_winning_moves = []
        for index in move_list:
            if self.is_space_free(self.board, index):
                possible_winning_moves.append(index)
                if len(possible_winning_moves) != 0:
                    return random.choice(possible_winning_moves)
                else:
                    return None
       
    def start_game(self):
       "welcomes user, prints help message and hands over to the main game loop"
       # welcome user
       print('''\n\t---------------------
                \n\t|    TIC-TAC-TOE    |
                \n\t---------------------
             ''')
       self.print_board(list(range(1,10)))
       self.help()
       self.player_name = self.get_player_name()

       # get user's preferred mark 
       self.player_mark, self.ai_mark = self.get_mark()
       print("Your mark is " + self.player_mark)
        
       # randomly decide who can play first
       if random.randint(0, 1) == 0:
           print("I will go first")
           #self.make_move(self.board,random.choice(self.corners), self.ai_mark)
           #self.print_board()
           self.enter_game_loop('c')
       else:
           print("You will go first")
           # now, enter the main game loop
           self.enter_game_loop('h')


    def get_player_move(self):
        move = int(input("Pick a spot to move: (1-9) "))
        while move not in [1,2,3,4,5,6,7,8,9] or not self.is_space_free(self.board,move-1) :
            move = int(input("Invalid move. Please try again: (1-9) "))
        return move - 1

    def get_player_name(self):
        return input("Hi, I am {}".format(self.ai_name) + ". What is your name? ") 


    def enter_game_loop(self,turn):
       "starts the main game loop"
       is_running = True
       player = turn #h for human, c for computer - artifical inteligence
       while is_running:
           if player == 'h':
               user_input = self.get_player_move()
               self.make_move(self.board,user_input, self.player_mark)
               if self.is_winner(self.board, self.player_mark):
                   self.print_board()
                   print("\n\tCONGRATULATIONS {}, YOU HAVE WON THE GAME!!! \t\n".format(self.player_name))
                   #self.incr_score(self.player_name)
                   is_running = False
                   #break
               else:
                   if self.is_board_full():
                       self.print_board()
                       print("\n\t-- Match Draw --\t\n")
                       is_running = False
                       #break
                   else:
                       self.print_board()
                       player = 'c'
           # computer's turn to play
           else:
              ai_move =  self.get_ai_move()
              self.make_move(self.board, ai_move, self.ai_mark)
              if self.is_winner(self.board, self.ai_mark):
                  self.print_board()
                  print("\n\t{} HAS WON!!!!\t\n".format(self.ai_name))
                  #self.incr_score(self.ai_name)
                  is_running = False
                  break
              else:
                  if self.is_board_full():
                      self.print_board()
                      print("\n\t -- Match Draw -- \n\t")
                      is_running = False
                      #break
                  else:
                      self.print_board()
                      player = 'h'

       # when you break out of the loop, end the game
       self.end_game()

    def end_game(self):
       play_again = input("Would you like to play again? (y/n): ").lower()
       if play_again == 'y':
           self.__init__() # necessary for re-initialization of the board etc
           self.start_game()
       else:
           print("\n\t-- game over!!!--\n\t")
           self.quit_game()



if __name__ == "__main__":   
     TicTacToe = Game()
     TicTacToe.start_game()
