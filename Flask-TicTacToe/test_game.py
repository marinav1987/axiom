import unittest
from unittest.mock import Mock,patch
from game import Game


class TestGame(unittest.TestCase):
    'Class TestGame that contains tests for the game'

    def test_calculate_move(self):
        '''Method that tests computer move on the corners'''
        game = Game()
        game.random_corner = Mock(return_value=[0, 0])
        self.assertEqual(game.calculate_move(), {'row': 0, 'col': 0})
        x = game.calculate_move()
        self.assertEqual(x['row'] , 0)
        self.assertEqual(x['col'], 0)

    def test_calculate_move1(self):
        '''Method that tests computer move based on the minimax algorithm'''
        game = Game()
        game.is_board_empty = Mock(return_value=False)
        game.minimax = Mock(return_value=[2, None])
        self.assertEqual(game.calculate_move(), False)

    def test_calculate_move2(self):
        '''Method that tests computer move based on the minimax algorithm'''
        game = Game()
        game.is_board_empty = Mock(return_value=False)
        game.minimax = Mock(return_value=[-2, None])
        self.assertEqual(game.calculate_move(), False)

    def test_calculate_move3(self):
        '''Method that tests computer move based on the minimax algorithm'''
        game = Game()
        game.is_board_empty = Mock(return_value=False)
        game.minimax = Mock(return_value=[[1, 1], [2, 2]])
        self.assertEqual(game.calculate_move(), {'row': 2, 'col': 2})

    def test_minimax(self):
        '''Method that tests computer and player best move for a given board'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', 'X'],
            [' ', ' ', ' ']
        ]

        best_move = game.minimax(mark='O', alpha=[-2, None], beta=[2, None])
        self.assertEqual(best_move[1],[2, 1])

        best_move1 = game.minimax(mark='X', alpha=[-2, None], beta=[2, None])
        self.assertEqual(best_move1[1], [2, 2])

    def test_minimax1(self):
        '''Method that tests computer best move for a given board
           Check if the return assigned value [-1, None]'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', 'X'],
            [' ', 'O', ' ']
        ]

        best_move = game.minimax(mark='O', alpha=[-2, None], beta=[2, None])
        self.assertEqual(best_move[0], -1)
        self.assertEqual(best_move[1], None)

    def test_minimax2(self):
        '''Method that tests computer best move for a given board
           Check if the return assigned value [1, None]'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', 'X'],
            [' ', ' ', 'X']
        ]

        best_move = game.minimax(mark='O', alpha=[-2, None], beta=[2, None])
        self.assertEqual(best_move[0], 1)
        self.assertEqual(best_move[1], None)

    def test_minimax3(self):
        '''Method that tests computer best move for a given board
           Check if the return assigned value [0, None]'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', 'X'],
            ['O', 'X', 'O']
        ]

        best_move = game.minimax(mark='O', alpha=[-2, None], beta=[2, None])
        self.assertEqual(best_move[0], 0)
        self.assertEqual(best_move[1], None)

    def test_opponent(self):
        '''Method that tests opposite mark'''
        game = Game()
        resultX = game.opponent(mark='X')
        resultO = game.opponent(mark='O')
        self.assertTrue(resultX, 'O')
        self.assertTrue(resultO, 'X')

    def test_get_moves(self):
        '''Method that tests a list of available moves'''
        game = Game()
        game.board[1][2]='X'
        self.assertTrue(game.get_moves(), 8)

    def test_tied1(self):
        '''Method that tests if the match draw'''
        game = Game()
        game.has_won = Mock(return_value=False)
        game.is_board_full = Mock(return_value=True)
        self.assertEqual(game.tied(), True)

    def test_tied2(self):
        '''Method that tests if the tied returns false'''
        game = Game()
        # game.won_horizontal = Mock(return_value=[[1, 0], [1, 1], [1, 2]])
        game.has_won = Mock(return_value=[[1, 0], [1, 1], [1, 2]])
        game.is_board_full = Mock(return_value=False)
        self.assertEqual(game.tied(), False)

    def test_is_board_full1(self):
        '''Method that tests if the board is not full'''
        game = Game()
        game.board = [
            ['O', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' ']
        ]
        self.assertNotEqual(game.is_board_full(), True)

    def test_is_board_full2(self):
        '''Method that tests if the board is full'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', 'X'],
            ['O', 'X', 'O']
        ]
        self.assertEqual(game.is_board_full(), True)

    def test_is_board_empty1(self):
        '''Method that tests if the board is empty'''
        game = Game()
        game.board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        self.assertEqual(game.is_board_empty(), True)

    def test_is_board_empty2(self):
        '''Method that tests if the board is not empty'''
        game = Game()
        game.board = [
            ['O', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' ']
        ]
        self.assertEqual(game.is_board_empty(), False)

    def test_has_won1(self):
        '''Method that tests has_won when it returns
        the winning horizontal combination as a list'''
        game = Game()
        game.won_horizontal = Mock(return_value=[[1, 0], [1, 1], [1, 2]])
        self.assertEqual(game.has_won(mark='O'), [[1, 0], [1, 1], [1, 2]])

    def test_has_won2(self):
        '''Method that tests has_won when it returns
        the winning vertical combination as a list'''
        game = Game()
        game.won_vertical = Mock(return_value=[[0, 1], [1, 1], [2, 1]])
        self.assertEqual(game.has_won(mark='O'), [[0, 1], [1, 1], [2, 1]])

    def test_has_won3(self):
        '''Method that tests has_won when it returns
        the winning diagonal combination as a list'''
        game = Game()
        game.won_diagonal = Mock(return_value=[[0, 0], [1, 1], [2, 2]])
        self.assertEqual(game.has_won(mark='X'), [[0, 0], [1, 1], [2, 2]])

    def test_has_won4(self):
        '''Method that tests has_won when it returns
        the winning list of coordinates as a false'''
        game = Game()
        game.won_horizontal = Mock(return_value=False)
        game.won_vertical = Mock(return_value=False)
        game.won_diagonal = Mock(return_value=None)
        self.assertEqual(game.has_won(mark='O'), False)

    def test_won_vertical(self):
        '''Method that tests if it returns
         the winning vertical combination as a list or false'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', ' '],
            ['X', 'O', ' ']
        ]
        self.assertEqual(game.won_vertical(mark='O'), [[0, 1], [1, 1], [2, 1]])
        self.assertEqual(game.won_vertical(mark='X'), False)

    def test_won_horizontal(self):
        '''Method that tests if it returns
        the winning horizontal combination as a list or false'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', 'O'],
            ['X', ' ', ' ']
        ]
        self.assertEqual(game.won_horizontal(mark='O'), [[1, 0], [1, 1], [1, 2]])
        self.assertEqual(game.won_horizontal(mark='X'), False)

    def test_won_diagonal1(self):
        '''Method that tests if it returns
         the winning diagonal combination as a list'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'X', 'O'],
            ['O', ' ', 'X']
        ]
        self.assertEqual(game.won_diagonal(mark='X'), [[0, 0], [1, 1], [2, 2]])

    def test_won_diagonal2(self):
        '''Method that tests if it returns
        the winning diagonal combination as a list'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', 'X', 'O'],
            ['X', ' ', ' ']
        ]
        self.assertEqual(game.won_diagonal(mark='X'), [[2, 0], [1, 1], [0, 2]])

    def test_move(self):
        '''Method that tests if the empty space is left
        Method returns new game object'''
        game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', ' ', 'O'],
            ['O', ' ', 'X']
        ]

        new_game = game.move(mark='O', row=1, col=1)
        self.assertEqual(new_game.board[1][1], 'O')

    def test_make_player_move(self):
        '''Method that tests if player makes move'''
        game = Game()
        res_game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', ' ', 'O'],
            ['O', ' ', 'X']
        ]
        res_game.board = [
            ['X', 'O', 'X'],
            ['O', 'X', 'O'],
            ['O', ' ', 'X']
        ]
        self.assertEqual(game.make_player_move(row=1, col=1).board[1][1], res_game.board[1][1])

    def test_make_computer_move(self):
        '''Method that tests if computer makes move'''
        game = Game()
        res_game = Game()
        game.board = [
            ['X', 'O', 'X'],
            ['O', ' ', 'O'],
            ['O', ' ', 'X']
        ]
        res_game.board = [
            ['X', 'O', 'X'],
            ['O', 'O', 'O'],
            ['O', ' ', 'X']
        ]
        self.assertEqual(game.make_computer_move(row=1, col=1).board[1][1], res_game.board[1][1])


if __name__ == '__main__':
    unittest.main()