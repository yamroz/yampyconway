from yamconway.yamconwaylib import YamConway

if __name__ == '__main__':
    conway = YamConway(32, 64)
    conway.run_simulation(10, 0.2)