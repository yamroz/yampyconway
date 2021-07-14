from time import sleep
from random import seed, choice
from enum import Enum   

class Cell:
    neighbors = None
    alive: bool = False
    def __init__(self, randomize=True):
        if randomize:
            self.alive = choice([True,False])
        else:
            self.alive = False
        self.neighbors = []

    def setAlive(self, alive: bool):
        self.alive = alive

    def count_alive_neighbors(self):
        return sum(n.alive for n in self.neighbors)

class ConBoard:
    # cells_in_row, rows_no = 16, 16
    # cells: Cell = None
    def __init__(self, name: str, rows_no: int = 16, cells_in_row: int = 16, randomize: bool = True):
        self.name = name
        self.cells_in_row = cells_in_row
        self.rows_no = rows_no
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
                nbrs = self.cells[row_idx][col_idx].neighbors #get neighbors for convenience
                #lets firs take cells not on edges
                if (row_idx > 0 and row_idx < self.rows_no - 1 and
                    col_idx > 0 and col_idx < self.cells_in_row - 1):
                        nbrs.append(self.cells[row_idx-1][col_idx-1]) #left top
                        nbrs.append(self.cells[row_idx-1][col_idx]) #top
                        nbrs.append(self.cells[row_idx-1][col_idx+1]) #right top
                        nbrs.append(self.cells[row_idx][col_idx-1]) #left
                        nbrs.append(self.cells[row_idx][col_idx+1]) #right
                        nbrs.append(self.cells[row_idx+1][col_idx-1]) #left bottom
                        nbrs.append(self.cells[row_idx+1][col_idx]) #bottom
                        nbrs.append(self.cells[row_idx+1][col_idx+1]) #right bottom
                else:
                    #top row not corners
                    if row_idx == 0 and col_idx > 0 and col_idx < self.cells_in_row - 1:
                            nbrs.append(self.cells[row_idx][col_idx-1]) #left
                            nbrs.append(self.cells[row_idx][col_idx+1]) #right
                            nbrs.append(self.cells[row_idx+1][col_idx-1]) #left bottom
                            nbrs.append(self.cells[row_idx+1][col_idx]) #bottom
                            nbrs.append(self.cells[row_idx+1][col_idx+1]) #right bottom
                    #bottom row not corners
                    elif row_idx == self.rows_no - 1 and col_idx > 0 and col_idx < self.cells_in_row - 1:
                            nbrs.append(self.cells[row_idx][col_idx-1]) #left
                            nbrs.append(self.cells[row_idx-1][col_idx-1]) #left top
                            nbrs.append(self.cells[row_idx-1][col_idx]) #top
                            nbrs.append(self.cells[row_idx-1][col_idx+1]) #right top
                            nbrs.append(self.cells[row_idx][col_idx+1]) #right
                    #left edge not corners
                    elif col_idx == 0 and row_idx > 0 and row_idx < self.rows_no - 1:
                            nbrs.append(self.cells[row_idx-1][col_idx]) #top
                            nbrs.append(self.cells[row_idx-1][col_idx+1]) #right top
                            nbrs.append(self.cells[row_idx][col_idx+1]) #right
                            nbrs.append(self.cells[row_idx+1][col_idx+1]) #right bottom
                            nbrs.append(self.cells[row_idx+1][col_idx]) #bottom
                    #right edge not corners
                    elif col_idx == self.cells_in_row-1 and row_idx > 0 and row_idx<self.rows_no -1:
                            nbrs.append(self.cells[row_idx-1][col_idx]) #top
                            nbrs.append(self.cells[row_idx-1][col_idx-1]) #left top
                            nbrs.append(self.cells[row_idx][col_idx-1]) #left
                            nbrs.append(self.cells[row_idx+1][col_idx-1]) #left bottom
                            nbrs.append(self.cells[row_idx+1][col_idx]) #bottom
                    #left top corner
                    elif row_idx == 0 and col_idx == 0:
                            nbrs.append(self.cells[row_idx][col_idx+1]) #right
                            nbrs.append(self.cells[row_idx+1][col_idx+1]) #right bottom
                            nbrs.append(self.cells[row_idx+1][col_idx]) #bottom
                    #right top corner
                    elif row_idx == 0 and col_idx == self.cells_in_row-1:
                            nbrs.append(self.cells[row_idx][col_idx-1]) #left
                            nbrs.append(self.cells[row_idx+1][col_idx-1]) #left bottom
                            nbrs.append(self.cells[row_idx+1][col_idx]) #bottom
                    #left bottom corner
                    elif row_idx == self.rows_no-1 and col_idx == 0:
                            nbrs.append(self.cells[row_idx-1][col_idx]) #top
                            nbrs.append(self.cells[row_idx-1][col_idx+1]) #right top
                            nbrs.append(self.cells[row_idx][col_idx+1]) #right
                    #right bottom corner
                    elif row_idx == self.rows_no-1 and col_idx == self.cells_in_row-1:
                            nbrs.append(self.cells[row_idx-1][col_idx-1]) #left top
                            nbrs.append(self.cells[row_idx][col_idx-1]) #left                    
                            nbrs.append(self.cells[row_idx-1][col_idx]) #top


class YamConway:
    ALIVE_CELL_CHAR = '#'
    EMPTY_CELL_CHAR = '-'
    NR_OF_NBRS_TO_STARVE = 2
    NR_OF_NBRS_TO_CREATE = 3
    step = 0
    presentation = None

    class Presentation(Enum):
        PRETTY=1
        NUMBERS=2

    def __init__(self, rows = 20, cells_in_row=20, randomize=True, presentation=Presentation.PRETTY):
        self.board1 = ConBoard(rows_no=rows,cells_in_row=cells_in_row, randomize=True, name = 'board1')
        self.board2 = ConBoard(rows_no=rows,cells_in_row=cells_in_row, randomize=False, name = 'board2')
        self.stats = YamConway.YamConStats()
        self.presentation = presentation



    class YamConStats:
        verbose = False
        births = 0
        deaths = 0

        def bury(self):
            self.deaths = self.deaths + 1
            if self.verbose: self._verbose()

        def born(self):
            self.births = self.births + 1
            if self.verbose: self._verbose()

        def _verbose(self):
            print(f'born {self.births} died {self.deaths}')

    def run_simulation(self, turns, delay, presentation=Presentation.PRETTY):
        seed(1)
        self.print_conboard_nbrs(self.board1)
        print('*********** START ***********')
        for _ in range(turns):
            self.next_turn()
            if self.presentation == self.Presentation.PRETTY:
                self.print_conboard_pretty(self.board1)
            elif self.presentation == self.Presentation.NUMBERS:
                self.print_conboard_nbrs(self.board1)
            sleep(delay)
        print('Stats:')
        print('Born {} Died {}'.format(self.stats.births, self.stats.deaths))

    @staticmethod
    def print_board(board):
        for row in range(len(board)):
            print(board[row])

    def print_conboard_pretty(self, board: ConBoard):
        print("=" * len(board.cells))
        print(f'{board.name} {board.alive_cells()} step {self.step}')
        for row in board.cells:
            row_repr = ""
            for cell in row:
                if cell.alive:
                    row_repr = row_repr + self.ALIVE_CELL_CHAR
                else:
                    row_repr = row_repr + self.EMPTY_CELL_CHAR
            print(row_repr)

    def print_conboard_nbrs(self, board: ConBoard):
        print("=" * len(board.cells))
        print(f'{board.name} {board.alive_cells()} step {self.step}')
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

    def update_conboard(self, source_board: ConBoard, target_board: ConBoard):
        print(f'updating from {source_board.name} to {target_board.name}')
        for row_index, row in enumerate(source_board.cells):
            for cell_index, cell in enumerate(row):
                alive_nbrs = cell.count_alive_neighbors()
                if cell.alive:
                    if alive_nbrs < self.NR_OF_NBRS_TO_STARVE:
                        target_board.cells[row_index][cell_index].setAlive(False)
                        self.stats.bury()
                    elif alive_nbrs >=self.NR_OF_NBRS_TO_STARVE and alive_nbrs <= self.NR_OF_NBRS_TO_CREATE:
                        target_board.cells[row_index][cell_index].setAlive(True)
                    else:
                        target_board.cells[row_index][cell_index].setAlive(False)
                        self.stats.bury()
                else:
                    if alive_nbrs == self.NR_OF_NBRS_TO_CREATE:
                        target_board.cells[row_index][cell_index].setAlive(True)
                        self.stats.born()
                    else:
                        target_board.cells[row_index][cell_index].setAlive(False)

    def next_turn(self):
        self.update_conboard(self.board1, self.board2)
        self.step += 1
        temp_board = self.board2
        self.board2 = self.board1
        self.board1 = temp_board
        #self.board1, self.board2 = self.board2, self.board1
