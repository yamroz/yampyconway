import array
import os
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
    """
    This class stores board with each cell containing list of neighbours.
    """

    def __init__(self, name: str = 'no_name', rows_no: int = 16, cells_in_row: int = 16, randomize: bool = True):
        self.name = name
        self.cells_in_row = cells_in_row
        self.rows_no = rows_no
        self.cells: Cell = []
        self._make_cells(randomize)
        self._connect_neighbours()

    def reset_cells(self):
        """
        Deletes Cells collection and sets widtdh and height to 0
        """
        self.cells: Cell = []
        self.rows_no = 0
        self.cells_in_row = 0

    def _make_cells(self, randomize=True):
        for new_row_no in range(self.rows_no):
            self.cells.append([])
            for _ in range(self.cells_in_row):
                self.cells[new_row_no].append(Cell(randomize))

    def _connect_neighbours(self) -> None:
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

    def count_alive_cells(self) -> int:
        res = 0
        for row in self.cells:
            for cell in row:
                if cell.alive:
                    res += 1
        return res
