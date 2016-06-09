import argparse


def main():
    """choose a simulation and run it"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--ls', help="list the available simulations", action='store_true')
    parser.add_argument("simulation", help="The simulation to run", nargs='?')
    args = parser.parse_args()
    if args.simulation:
        for sim in list_simulations():
            if sim.name == args.simulation:
                print('running simulation "{}"'.format(args.simulation))
                sim().run()
                return
        else:
            print('No simulation with that name')

    if args.ls:
        for simulation in list_simulations():
            print simulation.name
()


def list_simulations():
    import whitepaper1
    sims = [
        whitepaper1.WhitePaper1,
        whitepaper1.WhitePaper2,
        whitepaper1.WhitePaper3,
    ]
    return sims
