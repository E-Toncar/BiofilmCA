"""
    Konstanty využívané v kódu
"""
class Constants:
    # + 2 proto, aby se dalo počítat s okrajem, který je vždy prázdný
    rows = 1002
    cols = 1002

    ## stavy bunek CA

    empty = 0
    unprotected = 1
    protected = 2
    dead = 3
