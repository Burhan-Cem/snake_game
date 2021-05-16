from snake_game import OutputInterface, Snake, Food
import pygame


class TextOutput(OutputInterface):
    def draw_map(self, game_map):
        dim_x, dim_y = game_map.shape()
        horizontal_border = '+' + ('-+' * dim_x)
        print(horizontal_border)
        for y in range(dim_y):
            row = '|'
            for x in range(dim_x):
                cell = game_map.peek(x, y)
                cell_type = type(cell)
                if cell is None:
                    row += '.'
                elif cell_type == Snake:
                    if cell.head_pos() == (x, y):
                        row += 'O'
                    else:
                        row += 'x'
                elif cell_type == Food:
                    row += 'F'
                else:
                    raise RuntimeError(f'Unknown object class in game_map:{cell_type}')
                row += '|'
            print(row)
        print(horizontal_border)

    def show_game_result(self, game_won):
        if game_won:
            print('Game won')
        else:
            print('Game lost')


class PygameOutput(OutputInterface):

    def __init__(self):
        pygame.init()

        # RGB color definitions
        self.background = (0, 0, 0)
        self.grid = (200, 200, 200)
        self.snake_head = (0, 255, 0)
        self.snake_tail = (0, 150, 0)
        self.food = (250, 0, 0)

        # Define screen properties
        self.box_size = 25
        self.screen = None
        self.screen_height = 0
        self.screen_width = 0

    def draw_map(self, game_map):

        def box2pixel(box_index):
            return box_index * self.box_size

        dim_x, dim_y = game_map.shape()

        # Define a surface at first call of function
        if not pygame.display.get_surface():
            self.screen_height = box2pixel(dim_y)
            self.screen_width = box2pixel(dim_x)
            self.screen = pygame.display.set_mode((self.screen_width + 1, self.screen_height + 1))
            self.screen.fill(self.background)

            def draw_grid():
                for x in range(dim_x + 1):
                    pygame.draw.line(self.screen, self.grid, [box2pixel(x), 0], [box2pixel(x), self.screen_height], 1)
                for y in range(dim_y + 1):
                    pygame.draw.line(self.screen, self.grid, [0, box2pixel(y)], [self.screen_width, box2pixel(y)], 1)
                pygame.display.flip()
            draw_grid()

        def fill_box(color, pos_x, pos_y):
            assert (pos_x < dim_x)
            assert (pos_y < dim_y)
            box = pygame.Rect(box2pixel(pos_x) + 2, box2pixel(pos_y) + 2, self.box_size - 3, self.box_size - 3)
            pygame.draw.rect(self.screen, color, box)
            pygame.display.flip()

        for x in range(dim_x):
            for y in range(dim_y):
                cell = game_map.peek(x, y)
                cell_type = type(cell)
                if cell is None:
                    fill_box(self.background, x, y)
                elif cell_type == Snake:
                    if cell.head_pos() == (x, y):
                        fill_box(self.snake_head, x, y)
                    else:
                        fill_box(self.snake_tail, x, y)
                elif cell_type == Food:
                    fill_box(self.food, x, y)
                else:
                    raise RuntimeError(f'Unknown object class in game_map:{cell_type}')

    def show_game_result(self, game_won):
        if game_won:
            print('Game won')
        else:
            print('Game lost')
