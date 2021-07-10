from yamconwaylib import *

if __name__ == '__main__':
    conway = YamConway(rows = 32, cells_in_row = 128, presentation=YamConway.Presentation.NUMBERS)
    conway.run_simulation(1000, 0.01)
