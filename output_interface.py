from snake_game import OutputInterface, Snake, Food


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
    def draw_map(self, game_map):
        raise NotImplementedError
