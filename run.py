#! /usr/bin/env python
if __name__ == '__main__':
    from src import simulation
    sim = simulation.Simulation()
    for line in sim.start():
        print line
