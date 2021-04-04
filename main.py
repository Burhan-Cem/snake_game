from input_interface import Keyboard
from snake_game import SnakeGame
from output_interface import TextOutput


def main():
    input_interface = Keyboard()
    output_interface = TextOutput()
    SnakeGame.run(input_interface, output_interface, 5, 5)


if __name__ == "__main__":
    # Executed only if run as a script
    main()
