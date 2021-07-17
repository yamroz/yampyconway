import yamconway
from yamconway.yamconway import YamConway

if __name__ == '__main__':
    conway = YamConway(32, 64,presentation=YamConway.Presentation.PRETTY)
    conway.run_simulation_with_console_output(20, 0.1)
    conway.board1.save_to_file('test_file.yc')