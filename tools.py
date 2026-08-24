"""
    Nástroje pro řízení simulace CA

"""
from constants import Constants
import random

class Tools:

    def create_grid():
        return [[Constants.empty for _ in range(Constants.cols)] for _ in range(Constants.rows)]

    def search_neighbors(grid, row, col):
        """"
        Shromáždí sousedy hledané buňky v mřížce. Vrací seznam 8 sousedů. (Mooreovo okolí)
        """
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_row = row + i
                neighbor_col = col + j
                if 0 <= neighbor_row < Constants.rows and 0 <= neighbor_col < Constants.cols:
                    neighbors.append(grid[neighbor_row][neighbor_col])
        return neighbors

    def seed_grid(grid):
        """
        Inicializuje mřížku s počátečními hodnotami. Náhodně vytvoří živé buňky ve spodu mřížky (simulace růstu biofilmu od povrchu vzhůru.)
        Následně prochází mřížku a pokud má buňka více než 5 živých sousedů, stává se chráněnou buňkou.
        """
        p = 0.9

        for i in range(0, 18):
            for j in range(0, Constants.cols):
                if random.random() < p:
                    grid[Constants.rows - 1 - i][j] = Constants.unprotected
            p -= 0.05 # postupně snižuje pravděpodobnost r;stu biofilmu směrem nahoru

        for i in range(1, 18):
            for j in range(1, Constants.cols -1):
                if grid[Constants.rows - 1 - i][j] == Constants.unprotected:
                    neighbors = Tools.search_neighbors(grid, Constants.rows - 1 - i, j)
                    if neighbors.count(Constants.unprotected) + neighbors.count(Constants.protected) > Constants.min_protected_neighbors:
                        grid[Constants.rows - 1 - i][j] = Constants.protected

        return grid

    def update_grid(grid):
        """
        Aktualizuje mřížku podle pravidel CA. (Viz dokumetace)
        """
        new_grid = [row[:] for row in grid]
        for i in range(1, Constants.rows - 1):
            for j in range(1, Constants.cols - 1):

                d = 0 # počet mrtvých sousedů / produkují eDNA a típ pádem zvyšují ochranu sousedních buňek.
                p = Constants.base_death_probability # počáteční pravděpodobnost, že buňka podlehne antibiotiiku a zemře. (Snižuje se s počtem mrtvých sousedů a pokud je buňka protected.)

                neighbors = Tools.search_neighbors(grid, i, j)

                if grid[i][j] == Constants.empty:
                    # pokud je buňka prázdná, zkontroluje se počet živých sousedů. Pokud má aspoň 3, tak se stane živou.
                    if (neighbors.count(Constants.unprotected) + neighbors.count(Constants.protected)) > Constants.min_neighbors_to_live:
                        new_grid[i][j] = Constants.unprotected
                elif grid[i][j] == Constants.unprotected or grid[i][j] == Constants.protected:
                    if grid[i][j] == Constants.protected:
                        p -= Constants.cluster_protection # pokud je buňka chráněná, tak se sníží pravděpodobnost, že zemře.
                    d = 8 - (neighbors.count(Constants.unprotected) + neighbors.count(Constants.protected) + neighbors.count(Constants.empty)) # počet mrtvých sousedů
                    p -= d * Constants.dead_cell_protection # čím více mrtvých sousedů, tím menší pravděpodobnost, že buňka zemře.
                    if p < 0:
                        p = 0# minimální pravděpodobnost, že buňka zemře.
                    if random.random() < p:
                        new_grid[i][j] = Constants.dead
                elif Constants.dead <= grid[i][j] < Constants.dead_end:
                    new_grid[i][j] += 1
                elif grid[i][j] == Constants.dead_end:
                    new_grid[i][j] = Constants.empty
                else:
                    print(f"Unexpected cell state: {grid[i][j]} at ({i}, {j})")
                    break

        for i in range(1, Constants.rows - 1):
            for j in range(1, Constants.cols - 1):
                if new_grid[i][j] == Constants.unprotected:
                    neighbors = Tools.search_neighbors(new_grid, i, j)
                    if neighbors.count(Constants.unprotected) + neighbors.count(Constants.protected) > Constants.min_protected_neighbors:
                        new_grid[i][j] = Constants.protected


        return new_grid