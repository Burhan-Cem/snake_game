from input_interface import Keyboard
import unittest
from unittest.mock import patch
from snake_game import Direction, InputInterface


class TestKeyboard(unittest.TestCase):

    @patch('keyboard.is_pressed')
    def testKeyboardInput(self, mock_is_pressed):

        mock_is_pressed.return_value = True
        input_interface = Keyboard()
        self.assertEqual(Direction.X_POSITIVE, input_interface.get_next_action())


if __name__ == '__main__':
    unittest.main()
