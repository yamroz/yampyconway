from yamconwaylib import *

if __name__ == '__main__':
    conway = YamConway(rows = 8, cells_in_row = 8, presentation=YamConway.Presentation.NUMBERS)
    conway.run_simulation(3, 0.1)
