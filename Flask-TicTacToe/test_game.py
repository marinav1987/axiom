import unittest
from unittest.mock import Mock
from game import Game


class TestGame(unittest.TestCase):
    'Class TestGame that contains tests for the game'

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
        game.is_board_empty= Mock(return_value=False)
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


if __name__ == '__main__':
    unittest.main()