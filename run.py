#! /usr/bin/env python
if __name__ == '__main__':
    try:
        from src import controllers
        for output in controllers.Simulation():
            print output
    except (KeyboardInterrupt, EOFError):
        pass
