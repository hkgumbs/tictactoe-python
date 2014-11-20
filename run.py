#! /usr/bin/env python
if __name__ == '__main__':
    try:
        from src import simulation
        sim = simulation.Simulation()
        while sim.has_next():
            print sim.next()
    except (KeyboardInterrupt, EOFError):
        print  # print new line for clarity
