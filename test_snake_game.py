import unittest
import copy
from unittest.mock import Mock, call, patch
from snake_game import Food, Snake, Map2D, SnakeGame
from snake_game import Direction, OutputInterface


class FakeOutput(OutputInterface):

    def __init__(self):
        self.drawn_maps = []
        self.game_results = []

    def draw_map(self, game_map):
        self.drawn_maps.append(copy.deepcopy(game_map))

    def show_game_result(self, game_won):
        self.game_results.append(game_won)

    def verify_game_map(self, test_object, map_index, object_types_by_pos):
        game_map = self.drawn_maps[map_index]
        max_x, max_y = game_map.shape()
        for pos_x in range(max_x):
            for pos_y in range(max_y):
                expected_type = object_types_by_pos.get((pos_x, pos_y), type(None))
                test_object.assertEqual(expected_type, type(game_map.peek(pos_x, pos_y)), f'{pos_x} {pos_y}')


class TestGameLogic(unittest.TestCase):

    @patch('random.randint')
    def testDrawMap(self, mock_random):
        mock_input_interface = Mock()
        mock_input_interface.get_next_action.return_value = Direction.X_POSITIVE
        fake_output = FakeOutput()

        mock_random.side_effect = [2, 1,
                                   0, 0]
        SnakeGame.run(mock_input_interface, fake_output, 3, 3)
        self.assertEqual(2, len(fake_output.drawn_maps))

        fake_output.verify_game_map(self, 0, {(1, 1): Snake, (2, 1): Food})
        fake_output.verify_game_map(self, 1, {(1, 1): Snake, (2, 1): Snake, (0, 0): Food})

    @patch('random.randint')
    def testRunHitWallAndDie(self, mock_random):
        mock_input_interface = Mock()
        mock_input_interface.get_next_action.return_value = Direction.X_POSITIVE
        fake_output = FakeOutput()

        mock_random.side_effect = [0, 0]

        SnakeGame.run(mock_input_interface, fake_output, 3, 3)
        self.assertEqual(fake_output.game_results, [False])
        self.assertEqual(2, len(fake_output.drawn_maps))

        fake_output.verify_game_map(self, 0, {(1, 1): Snake, (0, 0): Food})
        fake_output.verify_game_map(self, 1, {(2, 1): Snake, (0, 0): Food})

    @patch('random.randint')
    def testRunHitSnakeAndDie(self, mock_random):
        mock_input_interface = Mock()
        fake_output = FakeOutput()

        mock_input_interface.get_next_action.side_effect = [Direction.Y_NEGATIVE,
                                                            Direction.X_NEGATIVE,
                                                            Direction.Y_POSITIVE,
                                                            Direction.Y_POSITIVE,
                                                            Direction.X_POSITIVE,
                                                            Direction.Y_NEGATIVE,
                                                            Direction.X_NEGATIVE
                                                            ]

        mock_random.side_effect = [2, 1,
                                   2, 0,
                                   1, 0,
                                   1, 1,
                                   1, 2,
                                   2, 2,
                                   0, 0]
        SnakeGame.run(mock_input_interface, fake_output, 3, 3)

        self.assertEqual(fake_output.game_results, [False])

        fake_output.verify_game_map(self, len(fake_output.drawn_maps) - 1,
                                    {(1, 1): Snake, (2, 1): Snake, (2, 0): Snake, (1, 0): Snake, (1, 2): Snake,
                                     (2, 2): Snake, (0, 0): Food})

    def testRunOutOfSpace(self):
        mock_input_interface = Mock()
        fake_output = FakeOutput()
        mock_input_interface.get_next_action.return_value = Direction.X_POSITIVE

        SnakeGame.run(mock_input_interface, fake_output, 2, 1)

        self.assertEqual(fake_output.game_results, [True])
        self.assertEqual(2, len(fake_output.drawn_maps))

        fake_output.verify_game_map(self, 1, {(0, 0): Snake, (1, 0): Snake})


class TestMap2D(unittest.TestCase):
    def testTriesToPutStringToFreePosition(self):
        game_map = Map2D(1, 2)

        self.assertIsNone(game_map.try_put('testString', 0, 1))
        self.assertEqual(game_map.peek(0, 1), 'testString')
        self.assertIsNone(game_map.peek(0, 0))

    def testTriesToPutStringToOccupiedPosition(self):
        game_map = Map2D(1, 2)
        game_map.put('blocker', 0, 1)

        self.assertEqual(game_map.try_put('testString', 0, 1), 'blocker')
        self.assertEqual(game_map.peek(0, 1), 'blocker')
        self.assertIsNone(game_map.peek(0, 0))

    def testPutsStringToFreePosition(self):
        game_map = Map2D(2, 2)
        game_map.put('testString', 0, 1)

        self.assertEqual(game_map.peek(0, 1), 'testString')
        self.assertIsNone(game_map.peek(0, 0))
        self.assertIsNone(game_map.peek(1, 0))
        self.assertIsNone(game_map.peek(1, 1))

    def testPutsStringToOccupiedPosition(self):
        game_map = Map2D(2, 2)
        game_map.put('existing', 0, 1)

        game_map.put('newObject', 0, 1)

        self.assertEqual(game_map.peek(0, 1), 'newObject')
        self.assertIsNone(game_map.peek(0, 0))
        self.assertIsNone(game_map.peek(1, 0))
        self.assertIsNone(game_map.peek(1, 1))

    def testShape(self):
        game_map = Map2D(1, 5)
        self.assertEqual(game_map.shape(), (1, 5))

    def testValidatePosition(self):
        game_map = Map2D(2, 2)
        game_map.validate_position(0, 1)

    def testInvalidPosition(self):
        game_map = Map2D(2, 2)

        with self.assertRaises(ValueError) as context:
            game_map.validate_position(2, 2)
        self.assertIn('outside of the current map dimensions', str(context.exception))

    def testInsideMapBoundary(self):
        game_map = Map2D(2, 3)
        self.assertTrue(game_map.inside_map_boundary(1, 2))
        self.assertFalse(game_map.inside_map_boundary(2, 0))
        self.assertFalse(game_map.inside_map_boundary(-4, 0))
        self.assertFalse(game_map.inside_map_boundary(0, 3))
        self.assertFalse(game_map.inside_map_boundary(0, -1))


class TestFood(unittest.TestCase):

    def testInsertsFoodOnEmptyMap(self):
        mock_map = Mock()
        mock_map.shape.return_value = [1, 1]
        mock_map.try_put.return_value = None
        food = Food(mock_map)
        mock_map.try_put.assert_called_once_with(food, 0, 0)

    def testInsertsFoodOnThirdTry(self):
        mock_map = Mock()
        mock_map.shape.return_value = [1, 1]
        mock_map.try_put.side_effect = [object(), object(), None]
        food = Food(mock_map)
        calls = [call(food, 0, 0)] * 3
        mock_map.try_put.assert_has_calls(calls)

    def testRaisesErrorAfterMaxRetries(self):
        mock_map = Mock()
        mock_map.shape.return_value = [1, 1]
        mock_map.try_put.return_value = object()
        with self.assertRaises(RuntimeError) as context:
            Food(mock_map, max_retries=3)
        self.assertIn('Cannot place food', str(context.exception))

    def testInsertsFoodOnValidPosition(self):
        mock_map = Mock()
        mock_map.shape.return_value = [2, 2]
        mock_map.try_put.side_effect = [object()] * 50 + [None]
        food = Food(mock_map)
        calls = [call(food, 0, 0), call(food, 1, 0), call(food, 0, 1), call(food, 1, 1)]
        mock_map.try_put.assert_has_calls(calls, any_order=True)


class TestSnake(unittest.TestCase):
    def testPutsSnakeOnEmptyPosition(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 2, Direction.X_POSITIVE)
        self.assertEqual(game_map.peek(1, 2), snake)

    def testFailsToPutSnakeOnFilledPosition(self):
        game_map = Map2D(3, 3)
        game_map.put('blocker', 1, 2)
        with self.assertRaises(ValueError) as context:
            Snake(game_map, 1, 2, Direction.X_POSITIVE)
        self.assertIn('is blocked by', str(context.exception))

    def testSnakeLength(self):
        game_map = Map2D(2, 1)
        snake = Snake(game_map, 0, 0, Direction.X_POSITIVE)
        self.assertEqual(len(snake), 1)
        Food(game_map)
        snake.move()
        self.assertEqual(len(snake), 2)

    def testReturnsHeadPosition(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 2, Direction.X_POSITIVE)
        self.assertEqual(snake.head_pos(), (1, 2))

    def testReturnsEndPosition(self):
        game_map = Map2D(2, 1)
        snake = Snake(game_map, 1, 0, Direction.X_NEGATIVE)
        Food(game_map)
        snake.move()
        self.assertEqual(snake.end_pos(), (1, 0))

    def testHeadPositionIsCorrectAfterMove(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 1, Direction.X_POSITIVE)
        snake.move()
        self.assertEqual(snake.head_pos(), (2, 1))

    def testMovementSuccessfulDirectionChange(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 1, Direction.X_POSITIVE)
        snake.move()
        snake.set_direction(Direction.Y_POSITIVE)
        snake.move()
        self.assertEqual(game_map.peek(2, 2), snake)

    def testMovementUnsuccessfulDirectionChange(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 0, 1, Direction.X_POSITIVE)
        snake.move()
        snake.set_direction(Direction.X_NEGATIVE)
        snake.move()
        self.assertEqual(game_map.peek(2, 1), snake)

    def testMoveXPositive(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 1, Direction.X_POSITIVE)
        self.assertEqual(snake.move(), Snake.MoveResult.MOVED)
        self.assertIs(game_map.peek(2, 1), snake)
        self.assertIsNone(game_map.peek(1, 1))

    def testMoveXNegative(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 1, Direction.X_NEGATIVE)
        self.assertEqual(snake.move(), Snake.MoveResult.MOVED)
        self.assertIs(game_map.peek(0, 1), snake)
        self.assertIsNone(game_map.peek(1, 1))

    def testMoveYPositive(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 1, Direction.Y_POSITIVE)
        self.assertEqual(snake.move(), Snake.MoveResult.MOVED)
        self.assertIs(game_map.peek(1, 2), snake)
        self.assertIsNone(game_map.peek(1, 1))

    def testMoveYNegative(self):
        game_map = Map2D(3, 3)
        snake = Snake(game_map, 1, 1, Direction.Y_NEGATIVE)
        self.assertEqual(snake.move(), Snake.MoveResult.MOVED)
        self.assertIs(game_map.peek(1, 0), snake)
        self.assertIsNone(game_map.peek(1, 1))

    def testMoveInUndefinedDirection(self):
        game_map = Map2D(1, 1)
        snake = Snake(game_map, 0, 0, 'not_a_direction')
        with self.assertRaises(RuntimeError) as context:
            snake.move()
        self.assertIn('Invalid direction', str(context.exception))

    def testMoveSnakeOnCircularPath(self):
        game_map = Map2D(2, 2)
        snake = Snake(game_map, 0, 0, Direction.X_POSITIVE)
        Food(game_map)
        Food(game_map)
        Food(game_map)
        snake.move()
        snake.set_direction(Direction.Y_POSITIVE)
        snake.move()
        snake.set_direction(Direction.X_NEGATIVE)
        snake.move()
        snake.set_direction(Direction.Y_NEGATIVE)
        self.assertEqual(snake.move(), Snake.MoveResult.MOVED)
        self.assertEqual(snake.head_pos(), (0, 0))
        self.assertEqual(snake.end_pos(), (1, 0))

    def testMoveResultHitWall(self):
        game_map = Map2D(1, 1)
        snake = Snake(game_map, 0, 0, Direction.Y_NEGATIVE)
        self.assertEqual(snake.move(), Snake.MoveResult.HIT_WALL)

    def testMoveResultHitSnake(self):
        game_map = Map2D(2, 1)
        snake = Snake(game_map, 0, 0, Direction.X_POSITIVE)
        Snake(game_map, 1, 0, Direction.X_POSITIVE)
        self.assertEqual(snake.move(), Snake.MoveResult.HIT_SNAKE)
        self.assertIs(game_map.peek(0, 0), snake)

    def testMoveResultAteFood(self):
        game_map = Map2D(2, 1)
        snake = Snake(game_map, 0, 0, Direction.X_POSITIVE)
        Food(game_map)
        self.assertEqual(snake.move(), Snake.MoveResult.ATE_FOOD)
        self.assertIs(game_map.peek(0, 0), snake)
        self.assertIs(game_map.peek(1, 0), snake)
        self.assertEqual(snake.head_pos(), (1, 0))

    def testMoveResultHitUnknownObject(self):
        game_map = Map2D(2, 1)
        snake = Snake(game_map, 0, 0, Direction.X_POSITIVE)
        game_map.put('some_object', 1, 0)
        with self.assertRaises(RuntimeError) as context:
            snake.move()
        self.assertIn('Blocking object unknown type', str(context.exception))


if __name__ == '__main__':
    unittest.main()
