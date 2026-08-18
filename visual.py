"""
    Visualizace simulace CA v okně
"""

import tkinter as tk

from constants import Constants


def state_color(value):
    """Return the color used for each cell state."""
    if value == Constants.empty:
        return "#ffffff"
    if value == Constants.unprotected:
        return "#4ade80"
    if value == Constants.protected:
        return "#2563eb"
    if Constants.dead <= value <= Constants.dead_end:
        return "#6b7280"
    return "#111827"


class SimulationWindow:
    def __init__(self, grid, cell_size=2, tick_interval=100, tick_callback=None):
        self.grid = [row[:] for row in grid]
        self.cell_size = cell_size
        self.tick_interval = tick_interval
        self.tick_callback = tick_callback
        self.tick_number = 0

        self.root = tk.Tk()
        self.root.title("Biofilm CA Simulation")

        width = max(1, len(self.grid[0]) * self.cell_size)
        height = max(1, len(self.grid) * self.cell_size)
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack()

    def render(self):
        self.canvas.delete("all")
        for row_index, row in enumerate(self.grid):
            for col_index, value in enumerate(row):
                x0 = col_index * self.cell_size
                y0 = row_index * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=state_color(value),
                    outline=""
                )

    def _tick(self):
        if self.tick_callback is not None:
            self.grid = self.tick_callback(self.grid, self.tick_number)

        self.render()
        self.tick_number += 1
        self.root.after(self.tick_interval, self._tick)

    def run(self):
        self.render()
        self.root.after(self.tick_interval, self._tick)
        self.root.mainloop()
