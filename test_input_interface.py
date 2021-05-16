from input_interface import Keyboard
import unittest
from unittest.mock import patch
from snake_game import Direction, InputInterface


class TestKeyboard(unittest.TestCase):

    @patch('keyboard.is_pressed')
    def testUp(self, mock_is_pressed):
        mock_is_pressed.side_effect = lambda x: x == 'up'
        self.assertEqual(Direction.Y_NEGATIVE, Keyboard().get_next_action(0))

    @patch('keyboard.is_pressed')
    def testDown(self, mock_is_pressed):
        mock_is_pressed.side_effect = lambda x: x == 'down'
        self.assertEqual(Direction.Y_POSITIVE, Keyboard().get_next_action(0))

    @patch('keyboard.is_pressed')
    def testLeft(self, mock_is_pressed):
        mock_is_pressed.side_effect = lambda x: x == 'left'
        self.assertEqual(Direction.X_NEGATIVE, Keyboard().get_next_action(0))

    @patch('keyboard.is_pressed')
    def testRight(self, mock_is_pressed):
        mock_is_pressed.side_effect = lambda x: x == 'right'
        self.assertEqual(Direction.X_POSITIVE, Keyboard().get_next_action(0))

    # TODO: Test multiple keyboard inputs, take last valid input


if __name__ == '__main__':
    unittest.main()
