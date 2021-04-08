from snake_game import InputInterface, Direction
from time import sleep
from keyboard import is_pressed


class Keyboard(InputInterface):
    """Must implement everything in InputInterface"""

    def get_next_action(self):
        next_action = None
        for _ in range(8):
            if is_pressed('up'):
                next_action = Direction.Y_POSITIVE
            elif is_pressed('down'):
                next_action = Direction.Y_NEGATIVE
            elif is_pressed('left'):
                next_action = Direction.X_NEGATIVE
            elif is_pressed('right'):
                next_action = Direction.X_POSITIVE
            sleep(0.1)
        print(next_action)
        return next_action
        # TODO: Return invalid direction when multiple keys are pressed


class MLInput(InputInterface):
    def get_next_action(self):
        raise NotImplementedError
