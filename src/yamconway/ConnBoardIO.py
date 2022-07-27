from yamconway.ConnectedBoard import ConnectedBoard

class ConnBoardIO:
    def __init__():
        pass

    @staticmethod
    def print_board(board):
        for row in range(len(board)):
            print(board[row])

    @staticmethod
    def load_from_file(board : ConnectedBoard, path_to_file: str = None):
        with open(path_to_file) as specimen:
            dead_marker = specimen.readline().rstrip()
            data = specimen.readlines()
            board.reset_cells()
            board.rows_no = len(data)
            board.cells_in_row = len(data[0].rstrip())
            #board._init_cells(randomize=False)
            board._make_cells(randomize=False)
            for row_idx, row in enumerate(data):
                for char_idx, character in enumerate(row.rstrip()):
                    board.cells[row_idx][char_idx].setAlive(
                        character != dead_marker)

    @staticmethod
    def save_to_file(board : ConnectedBoard, file_path_name:str):
        with open(file_path_name,'w') as output_file:
            output_file.write(board.EMPTY_CELL_CHAR)
            for row in board.cells:
                row_to_write = ''
                for cell in row:
                    if cell.alive:
                        row_to_write = row_to_write + board.ALIVE_CELL_CHAR
                    else:
                        row_to_write = row_to_write + board.EMPTY_CELL_CHAR
                output_file.write('\n' + row_to_write)