from yamconwaylib import *

if __name__ == '__main__':
    conway = YamConway(rows = 20, cells_in_row = 40)
    conway.run_simulation(20, 0.2)
