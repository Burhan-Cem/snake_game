from snake_game import InputInterface, Direction
from time import sleep
import keyboard
from random import random

class Keyboard(InputInterface):
    """Must implement everything in InputInterface"""
    def __init__(self, action_duration):
        self.action_duration = action_duration

    def get_next_action(self):
        next_action = None
        num_loops = max(int(self.action_duration / 0.1), 1)
        for _ in range(num_loops):
            if keyboard.is_pressed('up'):
                next_action = Direction.Y_NEGATIVE
            elif keyboard.is_pressed('down'):
                next_action = Direction.Y_POSITIVE
            elif keyboard.is_pressed('left'):
                next_action = Direction.X_NEGATIVE
            elif keyboard.is_pressed('right'):
                next_action = Direction.X_POSITIVE
            sleep(0.1)
        return next_action
        # TODO: Return invalid direction when multiple keys are pressed


class MLInput(InputInterface):
    def get_next_action(self):
        raise NotImplementedError
        
        
class RandomInput(InputInterface):
    def get_next_action(self):
        directions = [Direction.X_NEGATIVE, Direction.Y_NEGATIVE, Direction.X_POSITIVE, Direction.Y_POSITIVE]
        return choice(directions)
