"""
Tkinter vizualizace CA
"""

import tkinter as tk
from constants import Constants


class SimulationWindow:
    # Barvy jednotlivých stavů
    COLORS = {
        Constants.empty: "#ffffff",        # prázdná
        Constants.unprotected: "#4caf50",  # zelená
        Constants.protected: "#2196f3",    # modrá
        Constants.dead + 4: "#ffb3b3",         # dead_end, nejmene eDNA
        Constants.dead + 3: "#f99c9c",
        Constants.dead + 2: "#f78c8c",
        Constants.dead + 1: "#fc8989",
        Constants.dead: "#f76969",     # dead prvn9 f8ye
    }

    def __init__(
        self,
        grid,
        update_callback=None,
        cell_size=6,
        tick_interval=200,
    ):
        self.initial_grid = [row[:] for row in grid]
        self.grid = [row[:] for row in grid]

        self.update_callback = update_callback
        self.cell_size = cell_size
        self.tick_interval = tick_interval

        self.tick_number = 0
        self.running = False
        self.after_id = None

        self.window = tk.Tk()
        self.window.title("Biofilm CA Simulation")
        self.window.resizable(False, False)

        width = Constants.cols * self.cell_size
        height = Constants.rows * self.cell_size

        self.canvas = tk.Canvas(
            self.window,
            width=width,
            height=height,
            background="white",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=(10, 5))

        # Informace nad ovládáním
        self.info_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 11),
        )
        self.info_label.pack(pady=(0, 5))

        # Ovládání
        controls = tk.Frame(self.window)
        controls.pack(pady=(0, 10))

        self.start_button = tk.Button(
            controls,
            text="Start",
            width=10,
            command=self.start,
        )
        self.start_button.grid(row=0, column=0, padx=3)

        self.pause_button = tk.Button(
            controls,
            text="Pause",
            width=10,
            command=self.pause,
        )
        self.pause_button.grid(row=0, column=1, padx=3)

        self.step_button = tk.Button(
            controls,
            text="Step",
            width=10,
            command=self.step,
        )
        self.step_button.grid(row=0, column=2, padx=3)

        self.reset_button = tk.Button(
            controls,
            text="Reset",
            width=10,
            command=self.reset,
        )
        self.reset_button.grid(row=0, column=3, padx=3)

        # Rychlost animace
        tk.Label(controls, text="Interval [ms]:").grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(8, 0),
        )

        self.speed_scale = tk.Scale(
            controls,
            from_=50,
            to=1000,
            orient="horizontal",
            resolution=50,
            length=180,
        )
        self.speed_scale.set(self.tick_interval)
        self.speed_scale.grid(
            row=1,
            column=2,
            columnspan=2,
            pady=(8, 0),
        )

        # Legenda
        legend = tk.Frame(self.window)
        legend.pack(pady=(0, 10))

        self._add_legend_item(
            legend,
            "Empty",
            self.COLORS[Constants.empty],
            0,
        )
        self._add_legend_item(
            legend,
            "Unprotected",
            self.COLORS[Constants.unprotected],
            1,
        )
        self._add_legend_item(
            legend,
            "Protected",
            self.COLORS[Constants.protected],
            2,
        )

        # Mrtvé fáze zobrazené společně jako Dead
        self._add_legend_item(
            legend,
            "Dead",
            self.COLORS[Constants.dead],
            3,
        )

        self._draw_grid()

        # Pokud je okno zavřeno kliknutím na X
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def _add_legend_item(self, parent, text, color, column):
        frame = tk.Frame(parent)
        frame.grid(row=0, column=column, padx=8)

        color_box = tk.Label(
            frame,
            width=2,
            height=1,
            bg=color,
            relief="solid",
            borderwidth=1,
        )
        color_box.pack(side="left", padx=(0, 4))

        tk.Label(frame, text=text).pack(side="left")

    def _color_for_state(self, value):
        if Constants.dead <= value <= Constants.dead_end:
            return self.COLORS.get(
                value,
                self.COLORS[Constants.dead],
            )

        return self.COLORS.get(
            value,
            self.COLORS[Constants.empty],
        )

    def _draw_grid(self):
        self.canvas.delete("all")

        for row in range(Constants.rows):
            for col in range(Constants.cols):
                value = self.grid[row][col]

                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = self._color_for_state(value)

                # U prázdných buněk nekreslíme rámeček,
                # což výrazně zrychluje vykreslování.
                outline = "" if value == Constants.empty else "#555555"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=outline,
                )

        self._update_info()

    def _update_info(self):
        counts = {
            "unprotected": 0,
            "protected": 0,
            "dead": 0,
            "empty": 0,
        }

        for row in self.grid:
            for value in row:
                if value == Constants.empty:
                    counts["empty"] += 1
                elif value == Constants.unprotected:
                    counts["unprotected"] += 1
                elif value == Constants.protected:
                    counts["protected"] += 1
                elif Constants.dead <= value <= Constants.dead_end:
                    counts["dead"] += 1

        self.info_label.config(
            text=(
                f"Step: {self.tick_number} / {Constants.iterations}    "
                f"Unprotected: {counts['unprotected']}    "
                f"Protected: {counts['protected']}    "
                f"Dead: {counts['dead']}    "
                f"Empty: {counts['empty']}"
            )
        )

    def start(self):
        if self.running:
            return

        if self.tick_number >= Constants.iterations:
            return

        self.running = True
        self._schedule_next_step()

    def pause(self):
        self.running = False

        if self.after_id is not None:
            self.window.after_cancel(self.after_id)
            self.after_id = None

    def step(self):
        if self.tick_number >= Constants.iterations:
            return

        self.pause()
        self._advance()

    def reset(self):
        self.pause()

        self.grid = [row[:] for row in self.initial_grid]
        self.tick_number = 0

        self._draw_grid()

    def _schedule_next_step(self):
        if not self.running:
            return

        if self.tick_number >= Constants.iterations:
            self.running = False
            return

        interval = self.speed_scale.get()

        self.after_id = self.window.after(
            interval,
            self._advance,
        )

    def _advance(self):
        self.after_id = None

        if self.tick_number >= Constants.iterations:
            self.running = False
            return

        if self.update_callback is not None:
            self.grid = self.update_callback(
                self.grid,
                self.tick_number,
            )

        # Nyní už opravdu ukazujeme číslo právě vypočítaného kroku.
        self.tick_number += 1

        self._draw_grid()

        if self.tick_number >= Constants.iterations:
            self.running = False
            return

        if self.running:
            self._schedule_next_step()

    def close(self):
        self.pause()
        self.window.destroy()

    def run(self):
        self.window.mainloop()