import yamconway
from yamconway.yamconway import YamConway

if __name__ == '__main__':
    conway = YamConway(32, 64,presentation=YamConway.PresentationType.PRETTY)
    conway.run_simulation_with_console_output(200, 0.1)
    # conway.board1.save_to_file('test_file.yc')
    # deprecated - save_to_file has to be moved to other class