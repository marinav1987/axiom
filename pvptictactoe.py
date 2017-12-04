#!/usr/bin/env python
# --------------------------------------------------------------------------
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
import sqlite3


class Game:
    "Tic-Tac-Toe class. This class holds the user interaction, and game logic"

    def __init__(self):
        self.board = [' '] * 9
        self.player1_name = ''
        self.player1_mark = ''
        self.player2_name = ''
        self.player2_mark = ''
        self.win_combinations = ([0, 1, 2],  # Horizontal
                                 [3, 4, 5],
                                 [6, 7, 8],
                                 [0, 3, 6],  # Vertical
                                 [1, 4, 7],
                                 [2, 5, 8],
                                 [0, 4, 8],  # Diagonal
                                 [2, 4, 6])
        self.corners = [0, 2, 6, 8]
        self.sides = [1, 3, 5, 7]
        self.center = 4

        self.shape = '''
           \t| {} | {} | {} |
           \t-------------
           \t| {} | {} | {} |
           \t-------------
           \t| {} | {} | {} |
           '''

    def print_board(self, board=None):
        "Display board"
        if board is None:
            print(self.shape.format(*tuple(self.board[6:9] + self.board[3:6] + self.board[0:3])))
        else:
            # when the game starts, display numbers on all the grids
            print(self.shape.format(*tuple(board[6:9] + board[3:6] + board[0:3])))

    def get_mark(self):
        mark = input("Would you like your mark to be X or O?: ").upper()
        while mark not in ["X", "O"]:
            mark = input("Would you like your mark to be X or O? :").upper()
        if mark == "X":
            return ('X', 'O')
        else:
            return ('O', 'X')


    def setup_database(self):
        # Create a connection object
        # The data will be stored in the scores.db
        conn = sqlite3.connect("scores.db")
        # Create a cursor object
        con = conn.cursor()
        # Create the table players if not exists
        con.execute('''
        CREATE TABLE IF NOT EXISTS `players` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `name`	TEXT NOT NULL UNIQUE,
        `score`	INTEGER NOT NULL DEFAULT 0
        );
        ''')
        # Save(commit the changes)
        conn.commit()
        # Close the connection
        conn.close()

    def incr_decr_score_player1_win(self):
        # the player gets 10 points if win
        # the player gets -10 if lose
        conn = sqlite3.connect("scores.db")
        con = conn.cursor()
        con.execute("select * from players")
        rows = con.fetchall()
        # if play the game first time
        if len(rows) == 0:
            con.execute("insert into players(name, score) values (?,?)", (self.player1_name, '10'))
            con.execute("insert into players(name, score) values (?,?)", (self.player2_name, '-10'))
        else:
            names = []
            for i in rows:
                names.append(i[1])
            if self.player1_name in names and self.player2_name not in names:
                con.execute("select score from players where name = '" + self.player1_name + "'")
                score_player1 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player1 + 10) + "' where name = '" + self.player1_name + "'")
                con.execute("insert into players(name,score) values (?,?)", (self.player2_name, '-10'))
            elif self.player1_name not in names and self.player2_name in names:
                con.execute("insert into players(name,score) values (?,?)", (self.player1_name, '10'))
                con.execute("select score from players where name = '" + self.player2_name + "'")
                score_player2 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player2 - 10) + "' where name = '" + self.player2_name + "'")
            elif self.player1_name in names and self.player2_name in names:
                con.execute("select score from players where name = '" + self.player1_name + "'")
                score_player1 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player1 + 10) + "' where name = '" + self.player1_name + "'")
                con.execute("select score from players where name = '" + self.player2_name + "'")
                score_player2 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player2 -10) + "' where name = '" + self.player2_name + "'")
            else:
                con.execute("insert into players(name,score) values (?,?)", (self.player1_name, '10'))
                con.execute("insert into players(name,score) values (?,?)", (self.player2_name, '-10'))
        # Save(commit the changes)
        conn.commit()
        # Close the connection
        conn.close()

    def incr_decr_score_player2_win(self):
        # the player gets 10 points if win
        # the player gets -10 if lose
        conn = sqlite3.connect("scores.db")
        con = conn.cursor()
        con.execute("select * from players")
        rows = con.fetchall()
        # if play the game first time
        if len(rows) == 0:
            con.execute("insert into players(name, score) values (?,?)", (self.player1_name, '-10'))
            con.execute("insert into players(name, score) values (?,?)", (self.player2_name, '10'))
        else:
            names = []
            for i in rows:
                names.append(i[1])
            if self.player1_name in names and self.player2_name not in names:
                con.execute("select score from players where name = '" + self.player1_name + "'")
                score_player1 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player1 - 10) + "' where name = '" + self.player1_name + "'")
                con.execute("insert into players(name,score) values (?,?)", (self.player2_name, '10'))
            elif self.player1_name not in names and self.player2_name in names:
                con.execute("insert into players(name,score) values (?,?)", (self.player1_name, '-10'))
                con.execute("select score from players where name = '" + self.player2_name + "'")
                score_player2 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player2 + 10) + "' where name = '" + self.player2_name + "'")
            elif self.player1_name in names and self.player2_name in names:
                con.execute("select score from players where name = '" + self.player1_name + "'")
                score_player1 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player1 -10) + "' where name = '" + self.player1_name + "'")
                con.execute("select score from players where name = '" + self.player2_name + "'")
                score_player2 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player2 + 10) + "' where name = '" + self.player2_name + "'")
            else:
                con.execute("insert into players(name,score) values (?,?)", (self.player1_name, '10'))
                con.execute("insert into players(name,score) values (?,?)", (self.player2_name, '-10'))
        # Save(commit the changes)
        conn.commit()
        # Close the connection
        conn.close()

    def incr_score_match_draw(self):
        # each player gets 5 points
        conn = sqlite3.connect("scores.db")
        con = conn.cursor()
        con.execute("select * from players")
        rows = con.fetchall()
        # if play the game first time
        if len(rows) == 0:
            con.execute("insert into players(name, score) values (?,?)", (self.player1_name, '5'))
            con.execute("insert into players(name, score) values (?,?)", (self.player2_name, '5'))
        else:
            names = []
            for i in rows:
                names.append(i[1])
            if self.player1_name in names and self.player2_name not in names:
                con.execute("select score from players where name = '" + self.player1_name + "'")
                score_player1 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player1 + 5) + "' where name = '" + self.player1_name + "'")
                con.execute("insert into players(name,score) values (?,?)", (self.player2_name, '5'))
            elif self.player1_name not in names and self.player2_name in names:
                con.execute("insert into players(name,score) values (?,?)", (self.player1_name, '5'))
                con.execute("select score from players where name = '" + self.player2_name + "'")
                score_player2 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player2 + 5) + "' where name = '" + self.player2_name + "'")
            elif self.player1_name in names and self.player2_name in names:
                con.execute("select score from players where name = '" + self.player1_name + "'")
                score_player1 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player1 + 5) + "' where name = '" + self.player1_name + "'")
                con.execute("select score from players where name = '" + self.player2_name + "'")
                score_player2 = con.fetchone()[0]
                con.execute("update players set score = '" + str(
                    score_player2 + 5) + "' where name = '" + self.player2_name + "'")
            else:
                con.execute("insert into players(name,score) values (?,?)", (self.player1_name, '5'))
                con.execute("insert into players(name,score) values (?,?)", (self.player2_name, '5'))
        # Save(commit the changes)
        conn.commit()
        # Close the connection
        conn.close()


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

    def is_space_free(self, board, index):
        "checks for free space of the board"
        # print "SPACE {} is taken" {} index
        return board[index] == ' '

    def is_board_full(self):
        "checks if the board is full"
        for i in range(1, 9):
            if self.is_space_free(self.board, i):
                return False
        return True

    def make_move(self, board, index, move):
        board[index] = move

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
        # welcomes user, prints help message and hands over to the main game loop
        # welcome user
        print('''\n\t---------------------
                 \n\t|    TIC-TAC-TOE    |
                 \n\t---------------------
             ''')
        self.print_board(list(range(1, 10)))
        self.help()
        self.player1_name = self.get_player1_name()
        self.player2_name = self.get_player2_name()

        self.setup_database()

        # get user's preferred mark
        self.player1_mark, self.player2_mark = self.get_mark()
        print("{}'s mark is {} ".format(self.player1_name, self.player1_mark))
        print("{}'s mark is {} ".format(self.player2_name,self.player2_mark))

        # randomly decide who can play first
        if random.randint(0, 1) == 0:
            print("{} will go first".format(self.player1_name))
            # self.print_board()
            self.enter_game_loop('p1')# first player
        else:
            print("{} will go first".format(self.player2_name))
            # now, enter the main game loop
            self.enter_game_loop('p2')# second player


    def get_player_move(self):
        move = int(input("Pick a spot to move: (1-9) "))
        while move not in [1, 2, 3, 4, 5, 6, 7, 8, 9] or not self.is_space_free(self.board, move - 1):
            move = int(input("Invalid move. Please try again: (1-9) "))
        return move - 1

    def get_player1_name(self):
        return input("What is the name of the first player? ").upper()

    def get_player2_name(self):
        return input("What is the name of the second player? ").upper()

    def enter_game_loop(self, turn):
        "starts the main game loop"
        is_running = True
        player = turn  # p1 for the first player, p2 for the second player
        while is_running:
            if player == 'p1':
                user_input = self.get_player_move()
                self.make_move(self.board, user_input, self.player1_mark)
                if self.is_winner(self.board, self.player1_mark):
                    self.print_board()
                    print("\n\tCONGRATULATIONS {}, YOU HAVE WON THE GAME!!! \t\n".format(self.player1_name))
                    self.incr_decr_score_player1_win()
                    is_running = False
                    # break
                else:
                    if self.is_board_full():
                        self.print_board()
                        print("\n\t-- Match Draw --\t\n")
                        is_running = False
                        self.incr_score_match_draw()
                        # break
                    else:
                        self.print_board()
                        player = 'p2'

            # second player's turn to play
            else:
                user_input = self.get_player_move()
                self.make_move(self.board, user_input, self.player2_mark)
                if self.is_winner(self.board, self.player2_mark):
                    self.print_board()
                    print("\n\t{} HAS WON!!!!\t\n".format(self.player2_name))
                    self.incr_decr_score_player2_win()
                    is_running = False
                    # break
                else:
                    if self.is_board_full():
                        self.print_board()
                        print("\n\t -- Match Draw -- \n\t")
                        is_running = False
                        self.incr_score_match_draw()
                        # break
                    else:
                        self.print_board()
                        player = 'p1'

        # Create a connection object
        # The data will be stored in the scores.db
        conn = sqlite3.connect("scores.db")
        # Create a cursor object
        con = conn.cursor()
        con.execute("select name,score from players order by score desc, name asc")
        username, top_score = con.fetchone()
        print("The leader is {} with {} points".format(username, top_score))
        # Close the connection
        conn.close()
        # when you break out of the loop, end the game
        self.end_game()

    def end_game(self):
        play_again = input("Would you like to play again? (y/n): ").lower()
        if play_again == 'y':
            self.__init__()  # necessary for re-initialization of the board etc
            self.start_game()
        else:
            print("\n\t-- game over!!!--\n\t")
            self.quit_game()


if __name__ == "__main__":
    TicTacToe = Game()
    TicTacToe.start_game()