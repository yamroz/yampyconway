import yamconway
from yamconway.yamconway import YamConway

if __name__ == '__main__':
    conway = YamConway(32, 64,presentation=YamConway.Presentation.PRETTY)
    conway.run_simulation_with_console_output(100, 0.1)