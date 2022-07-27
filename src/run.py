from yamconway.yamconway import SimulationHQ

if __name__ == '__main__':
    conway = SimulationHQ(32, 128,presentation=SimulationHQ.PresentationType.HEADLESS)
    conway.run_simulation_with_console_output(10000, 0.05)
    # conway.board1.save_to_file('test_file.yc')
    # deprecated - save_to_file has to be moved to other class