from time import sleep, time
from random import seed
from enum import Enum
from yamconway.ConnectedBoard import ConnectedBoard, Cell
from yamconway.ConnBoardIO import ConnBoardIO
from asciimatics.screen import Screen
from asciimatics.screen import ManagedScreen

import logging

class PresentationType(Enum):
        HEADLESS = "headless"
        PRETTY = "pretty"
        NUMBERS = "numbers"
        ASCIIMATICS = "asciimatics"

class SimulationHQ:
    ALIVE_CELL_CHAR = '#'
    EMPTY_CELL_CHAR = '-'
    NR_OF_NBRS_TO_STARVE = 2
    NR_OF_NBRS_TO_CREATE = 3
    step = 0
    presentation: PresentationType = None
    current_board: ConnectedBoard = None
    future_board: ConnectedBoard = None
    asciimatics_sreen = None

    def __init__(self, rows: int=20, cells_in_row: int=20, randomize: bool=True, presentation: PresentationType=PresentationType.HEADLESS) -> None:
        logging.info(f'Initializing Simulation with presentation type: {presentation.value}.')
        self.current_board = ConnectedBoard(
            rows_no=rows, cells_in_row=cells_in_row, randomize=True, name='board1')
        self.future_board = ConnectedBoard(
            rows_no=rows, cells_in_row=cells_in_row, randomize=False, name='board2')
        self.stats = SimulationHQ.YamConStats()
        self.presentation = presentation
        if presentation == PresentationType.ASCIIMATICS: # Should be moved to separate simulation class.
            self.asciimatics_sreen = Screen.open()

    def next_turn(self) -> None:
        self._update_conboard(self.current_board, self.future_board)
        self.step += 1
        self.current_board, self.future_board = self.future_board, self.current_board

    class YamConStats:
        verbose = False
        births = 0
        deaths = 0
        sim_start_tmstpm = 0.0
        sim_end_tmpstmp = 0.0
        sim_duration = 0.0

        def start_simulation_time(self):
            from time import time
            self.sim_start_tmstpm = time()
        
        def end_simulation_time(self):
            self.sim_end_tmpstmp = time()
            self.sim_duration = self.sim_end_tmpstmp - self.sim_start_tmstpm

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

    def run_simulation_with_console_output(self, turns: int=1000, delay_sec: float=0.5): # TODO refactor into inheritance
        seed(1)        
        logging.info('*********** START ***********')
        if self.presentation == PresentationType.PRETTY:
            for _ in range(turns):
                self.next_turn()
                self.print_conboard_pretty(self.current_board)
                sleep(delay_sec)
        elif self.presentation == PresentationType.NUMBERS:
            for _ in range(turns):
                self.next_turn()
                self.print_conboard_nbrs(self.current_board)
                sleep(delay_sec)
        elif self.presentation == PresentationType.ASCIIMATICS:
            with ManagedScreen() as screen:
                for _ in range(turns):
                    self.next_turn()
                    self.print_conboard_asciimatics(self.current_board, screen)
                    sleep(delay_sec)
        elif self.presentation == PresentationType.HEADLESS:
            self.stats.start_simulation_time()
            for _ in range (turns):
                self.next_turn()
            self.stats.end_simulation_time()
            print(f"The simulation took {self.stats.sim_duration} seconds")

        print('Stats:')
        print('Born {} Died {}'.format(self.stats.births, self.stats.deaths))
      
    def print_conboard_pretty(self, board: ConnectedBoard) -> None:
        print("=" * len(board.rows))
        print(f'{board.name} {board.count_alive_cells()} step {self.step}')
        for row in board.rows:
            print(self._get_row_cells_ascii(row))

    def _get_row_cells_ascii(self, row: list[Cell]) -> str:
        """
        Returns row as a string made from alive and empty cell representations.
        """
        return ''.join([self.ALIVE_CELL_CHAR if cell.alive else self.EMPTY_CELL_CHAR for cell in row ])

    def print_conboard_nbrs(self, board: ConnectedBoard):
        print("=" * len(board.rows))
        print(f'{board.name} {board.count_alive_cells()} step {self.step}')
        for row in board.rows:
            row_repr = ""
            for cell in row:
                if cell.alive:
                    row_repr = row_repr + str(cell.count_alive_neighbors())
                else:
                    row_repr = row_repr + self.EMPTY_CELL_CHAR
            print(row_repr)
    
    def print_conboard_asciimatics(self, board: ConnectedBoard, screen: Screen):
        screen.print_at("=" * len(board.rows),0,0)
        screen.print_at(f'{board.name} {board.count_alive_cells()} step {self.step}',0,1)
        for row_index,row in enumerate(board.rows):
            screen.print_at(self._get_row_cells_ascii(row),0,row_index+2)
        screen.refresh()

    def get_network_board(self) -> str:
        result = ''
        for row in self.current_board.rows:
            row_repr = self._get_row_cells_ascii(row)
            row_repr += '<BR>'
            result += row_repr
        return result

    def _update_conboard(self, source_board: ConnectedBoard, target_board: ConnectedBoard):
        """
        THE function - does all necessary operations to calculate next state of board.
        """
        for row_index, row in enumerate(source_board.rows):
            for cell_index, cell in enumerate(row):
                alive_nbrs = cell.count_alive_neighbors()
                if cell.alive:
                    if alive_nbrs < self.NR_OF_NBRS_TO_STARVE:
                        target_board.rows[row_index][cell_index].setAlive(
                            False)
                        self.stats.cell_died()
                    elif alive_nbrs >= self.NR_OF_NBRS_TO_STARVE and alive_nbrs <= self.NR_OF_NBRS_TO_CREATE:
                        target_board.rows[row_index][cell_index].setAlive(
                            True)
                    else:
                        target_board.rows[row_index][cell_index].setAlive(
                            False)
                        self.stats.cell_died()
                else:
                    if alive_nbrs == self.NR_OF_NBRS_TO_CREATE:
                        target_board.rows[row_index][cell_index].setAlive(
                            True)
                        self.stats.cell_was_born()
                    else:
                        target_board.rows[row_index][cell_index].setAlive(
                            False)
