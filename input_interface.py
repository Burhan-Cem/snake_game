from snake_game import InputInterface


class Keyboard(InputInterface):
    """Must implement everything in InputInterface"""

    def get_next_action(self):
        #TODO: Sleep function, read keyboard input
        #TODO: Multiple keys pressed == invalid input
        raise NotImplementedError


class MLInput(InputInterface):
    def get_next_action(self):
        raise NotImplementedError

