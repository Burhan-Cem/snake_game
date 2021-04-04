import unittest
from unittest.mock import call, patch

from output_interface import TextOutput
from snake_game import *


class TestTextOutput(unittest.TestCase):

    @patch('builtins.print')
    def testOutputOfEmptyMap(self, mock_print):
        game_map = Map2D(2, 2)
        text_output = TextOutput()
        text_output.draw_map(game_map)
        calls = [call('+-+-+'),
                 call('|.|.|'),
                 call('|.|.|'),
                 call('+-+-+')]
        mock_print.assert_has_calls(calls)

    @patch('builtins.print')
    def testOutputOfSnakeObjectInMap(self, mock_print):
        game_map = Map2D(1, 2)
        snake = Snake(game_map, 0, 0, Direction.Y_POSITIVE)
        Food(game_map)
        snake.move()
        text_output = TextOutput()
        text_output.draw_map(game_map)
        calls = [call('+-+'),
                 call('|x|'),
                 call('|O|'),
                 call('+-+')]
        mock_print.assert_has_calls(calls)

    @patch('builtins.print')
    def testOutputOfFoodObjectInMap(self, mock_print):
        game_map = Map2D(1, 1)
        Food(game_map)
        text_output = TextOutput()
        text_output.draw_map(game_map)
        calls = [call('+-+'),
                 call('|F|'),
                 call('+-+')]
        mock_print.assert_has_calls(calls)

    @patch('builtins.print')
    def testOutputOfUnknownObjectInMap(self, _mock_print):
        game_map = Map2D(1, 1)
        game_map.put('some_object', 0, 0)
        text_output = TextOutput()
        with self.assertRaises(RuntimeError) as context:
            text_output.draw_map(game_map)
        self.assertIn('Unknown object class', str(context.exception))

    @patch('builtins.print')
    def testGameResult(self, mock_print):
        text_output = TextOutput()
        text_output.show_game_result(True)
        text_output.show_game_result(False)

        calls = [call('Game won'),
                 call('Game lost')]
        mock_print.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
