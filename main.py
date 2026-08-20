"""
    řízení simulace CAs
"""
import argparse
import os

from tools import Tools
from constants import Constants
from statistics import Statistics
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
        "--headless",
        action="store_true",
        help="Run without opening the Tk window",
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

    if args.headless:
        use_visuals = False
    elif args.visual:
        use_visuals = True
    else:
        use_visuals = None

    main(
        use_visuals=use_visuals,
        rows=args.rows,
        cols=args.cols,
        iterations=args.iterations,
    )