"""
    řízení simulace CAs
"""
import argparse
import os

from tools import Tools
from constants import Constants
from simulation_statistics import Statistics
import statistics
from visual import SimulationWindow


def main(use_visuals=None, rows=None, cols=None, iterations=None):
    rows = Constants.rows if rows is None else rows
    cols = Constants.cols if cols is None else cols
    iterations = Constants.iterations if iterations is None else iterations

    if use_visuals is None:
        use_visuals = bool(
            os.environ.get("DISPLAY")
            or os.environ.get("WAYLAND_DISPLAY")
        )

    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive integers")

    if iterations < 0:
        raise ValueError("iterations must be non-negative")

    Constants.rows = rows
    Constants.cols = cols
    Constants.iterations = iterations

    grid = Tools.create_grid()
    grid = Tools.seed_grid(grid)

    #test
    print("Initial protected:", sum(row.count(Constants.protected) for row in grid))
    print("Initial unprotected:", sum(row.count(Constants.unprotected) for row in grid))

    stats = Statistics()
    stats.update(grid)
    stats.get_statistics()

    if use_visuals:

        def tick_callback(current_grid, tick_number):
            next_grid = Tools.update_grid(current_grid)

            stats.update(next_grid)
            stats.get_statistics()

            return next_grid

        print(
            f"Starting visual simulation "
            f"({Constants.rows}x{Constants.cols}, "
            f"{Constants.iterations} steps)"
        )

        window = SimulationWindow(
            grid,
            cell_size=6,
            tick_interval=200,
            update_callback=tick_callback,
        )

        window.run()

        print(
            "Final statistics:",
            stats.get_statistics(),
        )
        return

    print(
        f"Running headless simulation "
        f"({Constants.rows}x{Constants.cols}, "
        f"{Constants.iterations} steps)"
    )

    for _ in range(Constants.iterations):
        grid = Tools.update_grid(grid)
        stats.update(grid)
        stats.get_statistics()

    print(
        "Final statistics:",
        stats.get_statistics(),
    )

def count_alive(grid):
    """
    Spočítá všechny živé buňky:
    unprotected + protected.
    """
    return sum(
        row.count(Constants.unprotected)
        + row.count(Constants.protected)
        for row in grid
    )

def run_single_simulation(iterations=None):
    """
    Spustí jednu simulaci a po každém kroku vypíše celkový počet živých buněk.
    """
    if iterations is None:
        iterations = Constants.iterations

    grid = Tools.create_grid()
    grid = Tools.seed_grid(grid)

    survivors = count_alive(grid)

    print()
    print("Single simulation")
    print("=" * 60)
    print(survivors)

    for step in range(1, iterations + 1):
            grid = Tools.update_grid(grid)
    
            survivors = count_alive(grid)
            print(survivors)


    """

    print()
    print("Single simulation")
    print("=" * 60)
    print(
        f"Step 0: "
        f"survivors={survivors}"
    )

    for step in range(1, iterations + 1):
        grid = Tools.update_grid(grid)

        survivors = count_alive(grid)
        

        print(
            f"Step {step}: "
            f"survivors={survivors}"
        )

    """

    return grid

def run_monte_carlo(runs=1000, iterations=None):
    """
    Provede Monte Carlo simulaci.

    1000 běhů simulace, každý s 50 iteracemi.
    """
    if iterations is None:
        iterations = Constants.iterations

    initial_counts = []
    final_counts = []
    retention_rates = []

    for run in range(runs):
        grid = Tools.create_grid()
        grid = Tools.seed_grid(grid)

        initial_alive = count_alive(grid)
        initial_counts.append(initial_alive)

        for _ in range(iterations):
            grid = Tools.update_grid(grid)

        final_alive = count_alive(grid)
        final_counts.append(final_alive)

        # podíl živých buněk na konci oproti začátku
        if initial_alive > 0:
            retention = final_alive / initial_alive
        else:
            retention = 0.0

        retention_rates.append(retention)

    # agregované výsledky
    mean_initial = statistics.mean(initial_counts)
    mean_final = statistics.mean(final_counts)
    mean_retention = statistics.mean(retention_rates)


    print()
    print("=" * 60)
    print("MONTE CARLO SIMULATION")
    print("=" * 60)
    print(f"Runs:                  {runs}")
    print(f"Grid:                  {Constants.rows} x {Constants.cols}")
    print(f"Iterations per run:    {iterations}")
    print()
    print(f"Mean initial alive:    {mean_initial:.2f}")
    print(f"Mean final alive:      {mean_final:.2f}")
    print(f"Mean retention:        {mean_retention:.4f}")
    print()
    print("=" * 60)

    return {
        "runs": runs,
        "initial_counts": initial_counts,
        "final_counts": final_counts,
        "retention_rates": retention_rates,
        "mean_initial_alive": mean_initial,
        "mean_final_alive": mean_final,
        "mean_retention": mean_retention,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Biofilm CA simulation"
    )

    parser.add_argument(
        "--visual",
        action="store_true",
        help="Open the Tk animation window",
    )

    parser.add_argument(
        "--single",
        action="store_true",
        help="Run one simulation and print survivors after every step",
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without opening the Tk window",
    )

    parser.add_argument(
        "--monte-carlo",
        type=int,
        metavar="N",
        help="Run N Monte Carlo simulations",
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=None,
        help="Grid rows",
    )

    parser.add_argument(
        "--cols",
        type=int,
        default=None,
        help="Grid columns",
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Number of simulation steps",
    )

    args = parser.parse_args()

    # Parametry konfigurace
    rows = Constants.rows if args.rows is None else args.rows
    cols = Constants.cols if args.cols is None else args.cols
    iterations = (
        Constants.iterations
        if args.iterations is None
        else args.iterations
    )

    Constants.rows = rows
    Constants.cols = cols
    Constants.iterations = iterations

    if args.single:
        run_single_simulation(iterations=iterations)

    elif args.monte_carlo is not None:
        if args.monte_carlo <= 0:
            raise ValueError(
                "Number of Monte Carlo runs must be positive."
            )

        run_monte_carlo(
            runs=args.monte_carlo,
            iterations=iterations,
        )

    else:
        if args.headless:
            use_visuals = False
        elif args.visual:
            use_visuals = True
        else:
            use_visuals = None

        main(
            use_visuals=use_visuals,
            rows=rows,
            cols=cols,
            iterations=iterations,
        )