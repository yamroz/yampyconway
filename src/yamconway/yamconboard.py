from random import choice
from typing import Iterator


class Cell:
    neighbors = None
    alive: bool = False

    def __init__(self, randomize=True):
        if randomize:
            self.alive = choice([True, False])
        else:
            self.alive = False
        self.neighbors = []

    def setAlive(self, alive: bool):
        self.alive = alive

    def count_alive_neighbors(self):
        return sum(n.alive for n in self.neighbors)


class ConnectedBoard:
    ALIVE_CELL_CHAR = '#'
    EMPTY_CELL_CHAR = '-'

    def __init__(self, name: str, rows_no: int = 16, cells_in_row: int = 16, randomize: bool = True):
        self.name = name
        self.cells_in_row = cells_in_row
        self.rows_no = rows_no
        self._init_cells(randomize)

    def _init_cells(self, randomize: bool = True):
        self.cells: Cell = []
        self._make_cells(randomize)
        self._connect_neighbours()

    def alive_cells(self):
        res = 0
        for row in self.cells:
            for cell in row:
                if cell.alive:
                    res += 1
        return res

    def _make_cells(self, randomize=True):
        for new_row_no in range(self.rows_no):
            self.cells.append([])
            for _ in range(self.cells_in_row):
                self.cells[new_row_no].append(Cell(randomize))

    def _connect_neighbours(self):
        """
        Each cell has to have list of neighbors to collect information about.
        This method will create such lists.
        To make it efficient each cell will be examined to put it's reference to correct
        neighbor list.
        """
        for row_idx in range(self.rows_no):
            for col_idx in range(self.cells_in_row):
                # get neighbors for convenience
                nbrs = self.cells[row_idx][col_idx].neighbors
                # lets firs take cells not on edges
                if (row_idx > 0 and row_idx < self.rows_no - 1 and
                        col_idx > 0 and col_idx < self.cells_in_row - 1):
                    nbrs.append(self.cells[row_idx-1][col_idx-1])  # left top
                    nbrs.append(self.cells[row_idx-1][col_idx])  # top
                    nbrs.append(self.cells[row_idx-1][col_idx+1])  # right top
                    nbrs.append(self.cells[row_idx][col_idx-1])  # left
                    nbrs.append(self.cells[row_idx][col_idx+1])  # right
                    nbrs.append(self.cells[row_idx+1]
                                [col_idx-1])  # left bottom
                    nbrs.append(self.cells[row_idx+1][col_idx])  # bottom
                    nbrs.append(self.cells[row_idx+1]
                                [col_idx+1])  # right bottom
                else:
                    # top row not corners
                    if row_idx == 0 and col_idx > 0 and col_idx < self.cells_in_row - 1:
                        nbrs.append(self.cells[row_idx][col_idx-1])  # left
                        nbrs.append(self.cells[row_idx][col_idx+1])  # right
                        nbrs.append(self.cells[row_idx+1]
                                    [col_idx-1])  # left bottom
                        nbrs.append(self.cells[row_idx+1][col_idx])  # bottom
                        # right bottom
                        nbrs.append(self.cells[row_idx+1][col_idx+1])
                    # bottom row not corners
                    elif row_idx == self.rows_no - 1 and col_idx > 0 and col_idx < self.cells_in_row - 1:
                        nbrs.append(self.cells[row_idx][col_idx-1])  # left
                        nbrs.append(self.cells[row_idx-1]
                                    [col_idx-1])  # left top
                        nbrs.append(self.cells[row_idx-1][col_idx])  # top
                        nbrs.append(self.cells[row_idx-1]
                                    [col_idx+1])  # right top
                        nbrs.append(self.cells[row_idx][col_idx+1])  # right
                    # left edge not corners
                    elif col_idx == 0 and row_idx > 0 and row_idx < self.rows_no - 1:
                        nbrs.append(self.cells[row_idx-1][col_idx])  # top
                        nbrs.append(self.cells[row_idx-1]
                                    [col_idx+1])  # right top
                        nbrs.append(self.cells[row_idx][col_idx+1])  # right
                        # right bottom
                        nbrs.append(self.cells[row_idx+1][col_idx+1])
                        nbrs.append(self.cells[row_idx+1][col_idx])  # bottom
                    # right edge not corners
                    elif col_idx == self.cells_in_row-1 and row_idx > 0 and row_idx < self.rows_no - 1:
                        nbrs.append(self.cells[row_idx-1][col_idx])  # top
                        nbrs.append(self.cells[row_idx-1]
                                    [col_idx-1])  # left top
                        nbrs.append(self.cells[row_idx][col_idx-1])  # left
                        nbrs.append(self.cells[row_idx+1]
                                    [col_idx-1])  # left bottom
                        nbrs.append(self.cells[row_idx+1][col_idx])  # bottom
                    # left top corner
                    elif row_idx == 0 and col_idx == 0:
                        nbrs.append(self.cells[row_idx][col_idx+1])  # right
                        # right bottom
                        nbrs.append(self.cells[row_idx+1][col_idx+1])
                        nbrs.append(self.cells[row_idx+1][col_idx])  # bottom
                    # right top corner
                    elif row_idx == 0 and col_idx == self.cells_in_row-1:
                        nbrs.append(self.cells[row_idx][col_idx-1])  # left
                        nbrs.append(self.cells[row_idx+1]
                                    [col_idx-1])  # left bottom
                        nbrs.append(self.cells[row_idx+1][col_idx])  # bottom
                    # left bottom corner
                    elif row_idx == self.rows_no-1 and col_idx == 0:
                        nbrs.append(self.cells[row_idx-1][col_idx])  # top
                        nbrs.append(self.cells[row_idx-1]
                                    [col_idx+1])  # right top
                        nbrs.append(self.cells[row_idx][col_idx+1])  # right
                    # right bottom corner
                    elif row_idx == self.rows_no-1 and col_idx == self.cells_in_row-1:
                        nbrs.append(self.cells[row_idx-1]
                                    [col_idx-1])  # left top
                        nbrs.append(self.cells[row_idx][col_idx-1])  # left
                        nbrs.append(self.cells[row_idx-1][col_idx])  # top

    def print_conboard_pretty(self):
        print("=" * len(self.cells))
        print(f'{self.name} {self.alive_cells()}')
        for row in self.cells:
            row_repr = ""
            for cell in row:
                if cell.alive:
                    row_repr = row_repr + self.ALIVE_CELL_CHAR
                else:
                    row_repr = row_repr + self.EMPTY_CELL_CHAR
            print(row_repr)

    def load_from_file(self, path_to_file: str = None):
        with open(path_to_file) as specimen:
            dead_marker = specimen.readline().rstrip()
            data = specimen.readlines()
            self.rows_no = len(data)
            self.cells_in_row = len(data[0].rstrip())
            self._init_cells(randomize=False)
            for row_idx, row in enumerate(data):
                for char_idx, character in enumerate(row.rstrip()):
                    self.cells[row_idx][char_idx].setAlive(
                        character != dead_marker)
