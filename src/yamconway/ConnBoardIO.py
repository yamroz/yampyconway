from yamconway.ConnectedBoard import ConnectedBoard,Cell
from yamconway.settings import ALIVE_CELL_CHAR, EMPTY_CELL_CHAR
from os import linesep


class ConnBoardIO:

    @staticmethod
    def get_row_cells_ascii(row: list[Cell]) -> str:
        """
        Returns row as a string made from alive and empty cell representations.
        """
        return "".join(
            [ALIVE_CELL_CHAR if cell.alive else EMPTY_CELL_CHAR for cell in row]
        )

    @staticmethod
    def board_to_string(board: ConnectedBoard) -> str:
        board_str: str = ""
        for row in board.rows:
            board_str += ConnBoardIO.get_row_cells_ascii(row)
            board_str += linesep
        return board_str

    @staticmethod
    def load_from_file(board: ConnectedBoard, path_to_file: str | None = None):
        try:
            with open(path_to_file) as specimen:  # type: ignore
                dead_marker = specimen.readline().rstrip()
                data = specimen.readlines()
                board.reset_cells()
                board.rows_no = len(data)
                board.cells_in_row = len(data[0].rstrip())
                # board._init_cells(randomize=False)
                board._make_cells(randomize=False)
                for row_idx, row in enumerate(data):
                    for char_idx, character in enumerate(row.rstrip()):
                        board.rows[row_idx][char_idx].setAlive(character != dead_marker)
        except FileNotFoundError:
            print(f"File {path_to_file} not found. Board not loaded.")

    @staticmethod
    def save_to_file(board: ConnectedBoard, file_path_name: str):
        with open(file_path_name, "w") as output_file:
            output_file.write(EMPTY_CELL_CHAR)
            for row in board.rows:
                row_to_write = ""
                for cell in row:
                    if cell.alive:
                        row_to_write = row_to_write + ALIVE_CELL_CHAR
                    else:
                        row_to_write = row_to_write + EMPTY_CELL_CHAR
                output_file.write("\n" + row_to_write)
