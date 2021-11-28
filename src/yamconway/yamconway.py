from time import sleep
from random import seed
from enum import Enum
from yamconway.ConnectedBoard import ConnectedBoard


class YamConway:
    ALIVE_CELL_CHAR = '#'
    EMPTY_CELL_CHAR = '-'
    NR_OF_NBRS_TO_STARVE = 2
    NR_OF_NBRS_TO_CREATE = 3
    step = 0
    presentation = None
    board1: ConnectedBoard = None
    board2: ConnectedBoard = None

    class PresentationType(Enum):
        PRETTY = 1
        NUMBERS = 2

    def __init__(self, rows=20, cells_in_row=20, randomize=True, presentation=PresentationType.PRETTY):
        self.board1 = ConnectedBoard(
            rows_no=rows, cells_in_row=cells_in_row, randomize=True, name='board1')
        self.board2 = ConnectedBoard(
            rows_no=rows, cells_in_row=cells_in_row, randomize=False, name='board2')
        self.stats = YamConway.YamConStats()
        self.presentation = presentation

    class YamConStats:
        verbose = False
        births = 0
        deaths = 0

        def cell_died(self):
            self.deaths = self.deaths + 1
            if self.verbose:
                self._verbose()

        def cell_was_born(self):
            self.births = self.births + 1
            if self.verbose:
                self._verbose()

        def _verbose(self):
            print(f'born {self.births} died {self.deaths}')

    def run_simulation_with_console_output(self, turns, delay):
        seed(1)
        self.print_conboard_nbrs(self.board1)
        print('*********** START ***********')
        for _ in range(turns):
            self.next_turn()
            if self.presentation == self.PresentationType.PRETTY:
                self.print_conboard_pretty(self.board1)
            elif self.presentation == self.PresentationType.NUMBERS:
                self.print_conboard_nbrs(self.board1)
            sleep(delay)
        print('Stats:')
        print('Born {} Died {}'.format(self.stats.births, self.stats.deaths))

    @staticmethod
    def print_board(board):
        for row in range(len(board)):
            print(board[row])

    def print_conboard_pretty(self, board: ConnectedBoard):
        print("=" * len(board.cells))
        print(f'{board.name} {board.count_alive_cells()} step {self.step}')
        for row in board.cells:
            row_repr = ""
            for cell in row:
                if cell.alive:
                    row_repr = row_repr + self.ALIVE_CELL_CHAR
                else:
                    row_repr = row_repr + self.EMPTY_CELL_CHAR
            print(row_repr)

    def print_conboard_nbrs(self, board: ConnectedBoard):
        print("=" * len(board.cells))
        print(f'{board.name} {board.count_alive_cells()} step {self.step}')
        for row in board.cells:
            row_repr = ""
            for cell in row:
                if cell.alive:
                    row_repr = row_repr + str(cell.count_alive_neighbors())
                else:
                    row_repr = row_repr + self.EMPTY_CELL_CHAR
            print(row_repr)

    def get_network_board(self):
        result = ""
        for row in self.board1:
            for cell in row:
                result = result + str(cell)
        return result

    @staticmethod
    def board_to_pretty_string(board):
        result = ""
        print("=" * len(board[0]))
        for row in board:
            row_repr = ""
            for cell in row:
                if cell:
                    row_repr = row_repr + "O"
                else:
                    row_repr = row_repr + "."
            print(row_repr)
        return result

    def update_conboard(self, source_board: ConnectedBoard, target_board: ConnectedBoard):
        print(f'updating from {source_board.name} to {target_board.name}')
        for row_index, row in enumerate(source_board.cells):
            for cell_index, cell in enumerate(row):
                alive_nbrs = cell.count_alive_neighbors()
                if cell.alive:
                    if alive_nbrs < self.NR_OF_NBRS_TO_STARVE:
                        target_board.cells[row_index][cell_index].setAlive(
                            False)
                        self.stats.cell_died()
                    elif alive_nbrs >= self.NR_OF_NBRS_TO_STARVE and alive_nbrs <= self.NR_OF_NBRS_TO_CREATE:
                        target_board.cells[row_index][cell_index].setAlive(
                            True)
                    else:
                        target_board.cells[row_index][cell_index].setAlive(
                            False)
                        self.stats.cell_died()
                else:
                    if alive_nbrs == self.NR_OF_NBRS_TO_CREATE:
                        target_board.cells[row_index][cell_index].setAlive(
                            True)
                        self.stats.cell_was_born()
                    else:
                        target_board.cells[row_index][cell_index].setAlive(
                            False)

    def next_turn(self):
        self.update_conboard(self.board1, self.board2)
        self.step += 1
        self.board1, self.board2 = self.board2, self.board1
