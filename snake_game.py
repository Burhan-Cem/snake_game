from collections import deque
from enum import Enum
import random


class Direction(Enum):
    Y_POSITIVE = 1
    X_POSITIVE = 2
    Y_NEGATIVE = 3
    X_NEGATIVE = 4


class InputInterface:
    def get_next_action(self):
        raise NotImplementedError


class OutputInterface:
    def draw_map(self, game_map):
        raise NotImplementedError

    def show_game_result(self, game_won):
        raise NotImplementedError


class SnakeGame:
    def run(self, input_interface, output_interface, dim_x, dim_y, max_iteration=1000000):
        game_map = Map2D(dim_x, dim_y)
        snake = Snake(game_map, (dim_x-1) // 2, (dim_y-1) // 2, Direction.X_POSITIVE)
        max_snake_length = dim_x * dim_y

        Food(game_map)

        output_interface.draw_map(game_map)
        move_result = snake.move()
        while move_result not in [Snake.MoveResult.HIT_SNAKE, Snake.MoveResult.HIT_WALL]:
            if move_result == Snake.MoveResult.ATE_FOOD:
                if len(snake) == max_snake_length:
                    output_interface.draw_map(game_map)
                    output_interface.show_game_result(True)
                    return
                Food(game_map)

            output_interface.draw_map(game_map)

            direction = input_interface.get_next_action()
            snake.set_direction(direction)
            move_result = snake.move()

            max_iteration -= 1
            if max_iteration == 0:
                raise RuntimeError('Max iteration reached.')

        output_interface.show_game_result(False)


class Map2D:
    def __init__(self, dim_x, dim_y):
        self.map = []
        for _ in range(dim_x):
            self.map.append([None]*dim_y)
        assert dim_x > 0
        assert dim_y > 0

    def try_put(self, object_to_put, pos_x, pos_y):
        """Returns None if put is successful. Otherwise returns blocking object."""
        self.validate_position(pos_x, pos_y)
        if self.map[pos_x][pos_y] is None:
            self.map[pos_x][pos_y] = object_to_put
        else:
            return self.map[pos_x][pos_y]

    def put(self, object_to_put, pos_x, pos_y):
        """Returns the object in (pos_x, pos_y) before this function."""
        self.validate_position(pos_x, pos_y)
        old_object, self.map[pos_x][pos_y] = self.map[pos_x][pos_y], object_to_put
        return old_object

    def peek(self, pos_x, pos_y):
        """Returns object in (pos_x, pos_y)"""
        self.validate_position(pos_x, pos_y)
        return self.map[pos_x][pos_y]

    def shape(self):
        """Returns map dimensions as a tuple"""
        return len(self.map), len(self.map[0])

    def validate_position(self, pos_x, pos_y):
        if not self.inside_map_boundary(pos_x, pos_y):
            raise ValueError(f'Position ({pos_x},{pos_y}) is outside of the current map dimensions')

    def inside_map_boundary(self, pos_x, pos_y):
        x_max = len(self.map)
        y_max = len(self.map[0])
        return 0 <= pos_x < x_max and 0 <= pos_y < y_max


class Food:
    def __init__(self, game_map, max_retries=10000):
        dim_x, dim_y = game_map.shape()

        def generate_pos(x_max, y_max):
            x_pos = random.randint(0, x_max - 1)
            y_pos = random.randint(0, y_max - 1)
            return x_pos, y_pos

        for i in range(max_retries):
            if game_map.try_put(self, *generate_pos(dim_x, dim_y)) is None:
                return
        raise RuntimeError(f'Cannot place food in game_map in {max_retries} tries')


class Snake:
    def __init__(self, game_map, head_x, head_y, direction):
        self.direction = direction
        self.game_map = game_map
        self.positions = deque()
        self.positions.append((head_x, head_y))

        blocking_object = game_map.try_put(self, head_x, head_y)
        if blocking_object:
            raise ValueError(f'Position ({head_x}, {head_y}) is blocked by {blocking_object}.')

    def __len__(self):
        return len(self.positions)

    def head_pos(self):
        return self.positions[0]

    def end_pos(self):
        return self.positions[-1]

    def set_direction(self, direction):
        """Changes direction only if it is valid."""

        def same_axis(direction1, direction2):
            y_axis = [Direction.Y_POSITIVE, Direction.Y_NEGATIVE]
            x_axis = [Direction.X_POSITIVE, Direction.X_NEGATIVE]
            return ((direction1 in x_axis and direction2 in x_axis)
                    or (direction1 in y_axis and direction2 in y_axis))

        if direction is None:
            return
        elif not same_axis(self.direction, direction):
            self.direction = direction

    class MoveResult(Enum):
        HIT_SNAKE = 1
        ATE_FOOD = 2
        HIT_WALL = 3
        MOVED = 4

    def move(self):
        """Returns move result."""
        new_x, new_y = self.positions[0]
        if self.direction == Direction.Y_POSITIVE:
            new_y += 1
        elif self.direction == Direction.X_POSITIVE:
            new_x += 1
        elif self.direction == Direction.Y_NEGATIVE:
            new_y -= 1
        elif self.direction == Direction.X_NEGATIVE:
            new_x -= 1
        else:
            raise RuntimeError(f'Invalid direction {self.direction}.')

        if not self.game_map.inside_map_boundary(new_x, new_y):
            return Snake.MoveResult.HIT_WALL

        blocking_object = self.game_map.try_put(self, new_x, new_y)
        if type(blocking_object) == Snake:
            if self.end_pos() == (new_x, new_y):
                self.positions.appendleft((new_x, new_y))
                self.positions.pop()
                # TODO: 2 yilan olursa yilanlarin ve mapin uyumlu olmalari lazim
                return Snake.MoveResult.MOVED
            else:
                return Snake.MoveResult.HIT_SNAKE
        elif type(blocking_object) == Food:
            self.positions.appendleft((new_x, new_y))
            self.game_map.put(self, new_x, new_y)
            return Snake.MoveResult.ATE_FOOD
        elif blocking_object is None:
            self.positions.appendleft((new_x, new_y))
            self.game_map.put(None, *self.positions.pop())
            return Snake.MoveResult.MOVED
        raise RuntimeError(f'Blocking object unknown type {type(blocking_object)}')
