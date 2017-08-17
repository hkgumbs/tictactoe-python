#! /usr/bin/env python3
if __name__ == '__main__':
    try:
        from src import simulation
        for output in simulation.Simulation():
            print(output)
    except (KeyboardInterrupt, EOFError):
        pass
