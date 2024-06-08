from yamconway.SimulationHQ import SimulationHQ, PresentationType

if __name__ == '__main__':
    conway = SimulationHQ(rows=32,
                          cells_in_row=128,
                          presentation=PresentationType.ASCIIMATICS)
    conway.run_simulation_with_console_output(turns=10000, delay_sec=0.05)
    # conway.board1.save_to_file('test_file.yc')
    # deprecated - save_to_file has to be moved to other class