import yamconway
from yamconway.yamconway import SimulationHQ

if __name__ == '__main__':
    conway = SimulationHQ(32, 64,presentation=SimulationHQ.PresentationType.PRETTY)
    conway.run_simulation_with_console_output(200, 0.1)
    # conway.board1.save_to_file('test_file.yc')
    # deprecated - save_to_file has to be moved to other class