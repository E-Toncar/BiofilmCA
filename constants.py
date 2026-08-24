"""
    Konstanty využívané v kódu
"""
class Constants:
    # + 2 proto, kvůli okrajům mřížky, které se neaktualizují
    rows = 52
    cols = 102
    iterations = 50

    ## stavy bunek CA

    empty = 0
    unprotected = 1
    protected = 2
    dead = 3
    dead_end = 7

    min_protected_neighbors = 5
    min_neighbors_to_live = 2
    base_death_probability = 0.6

    dead_cell_protection = 0.05
    cluster_protection = 0.4