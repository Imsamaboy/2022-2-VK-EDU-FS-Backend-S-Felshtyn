import unittest

from exceptions.InputException import InputException
from main.TicTacToeGame import TicTacToeGame


class TestTicTacToe(unittest.TestCase):
    """
    Testing Tic-Tac-Toe class logic
    """

    def test_input(self) -> None:
        """
        Testing users inputs
        :return:
        """
        correct_inputs = ["1", "2", "7", "8", "5"]
        incorrect_inputs_value_error = ["Привет", "Hello", ",!asg.", "[1, 2, 3]", "+++"]
        incorrect_inputs_input_exception = ["-1", "10", "-100", "22", "69", "-666"]

        for input_text in correct_inputs:
            self.assertEqual(TicTacToeGame.validate_input(input_text), int(input_text))

        for input_text in incorrect_inputs_value_error:
            self.assertRaises(ValueError, TicTacToeGame.validate_input, input_text)

        for input_text in incorrect_inputs_input_exception:
            self.assertRaises(InputException, TicTacToeGame.validate_input, input_text)

    def test_victory_and_draw_check(self) -> None:
        """
        Testing checks on victory and draw
        :return: None
        """
        game = TicTacToeGame()
        game.players = {"Vic": "X", "Lik": "O"}

        game.pos = {"X": [1, 3, 4, 6, 8], "O": [2, 5, 7, 9]}
        self.assertEqual(game.victory_check("Vic"), False)
        game.pos = {"X": [1, 4, 7, 5, 9], "O": [2, 3, 6, 8]}
        self.assertEqual(game.victory_check("Vic"), True)

        game.pos = {"X": [1, 3, 9], "O": [2, 5, 8]}
        self.assertEqual(game.victory_check("Lik"), True)
        game.pos = {"X": [1, 2, 4], "O": [3, 5, 7]}
        self.assertEqual(game.victory_check("Lik"), True)

        game.pos = {"X": [1, 3, 4, 8, 9], "O": [2, 5, 6, 7]}
        self.assertEqual(game.draw_check(), True)
        game.pos = {"X": [3, 4, 5, 8, 9], "O": [1, 2, 6, 7]}
        self.assertEqual(game.draw_check(), True)

        game.pos = {"X": [1, 3, 9], "O": [2, 5, 8]}
        self.assertEqual(game.draw_check(), False)
        game.pos = {"X": [1, 2, 4], "O": [3, 5, 7]}
        self.assertEqual(game.draw_check(), False)


if __name__ == '__main__':
    unittest.main()
