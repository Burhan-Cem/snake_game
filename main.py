from input_interface import Keyboard, MLInput
from snake_game import SnakeGame
from output_interface import TextOutput, PygameOutput
from config import settings


def main():
    if settings.input_interface == 'Keyboard':
        input_interface = Keyboard(settings.time_step_seconds)
    elif settings.input_interface == 'ML':
        input_interface = MLInput()
    else:
        raise RuntimeError(f'Unknown input interface {settings.input_interface}')

    if settings.output_interface == 'Text':
        output_interface = TextOutput()
    elif settings.output_interface == 'Pygame':
        output_interface = PygameOutput()
    else:
        raise RuntimeError(f'Unknown output interface {settings.output_interface}')

    SnakeGame.run(input_interface, output_interface, settings.dim_x, settings.dim_y)


if __name__ == "__main__":
    # Executed only if run as a script
    main()
