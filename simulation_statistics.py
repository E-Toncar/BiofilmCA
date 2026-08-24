"""
    Sběr a zpracování dat ze simulace CA
"""

class Statistics:
    def __init__(self):
        self.unprotected_count = 0
        self.protected_count = 0
        self.dead_count = 0
        self.history = []

    def update(self, grid):
        self.unprotected_count = sum(row.count(1) for row in grid)
        self.protected_count = sum(row.count(2) for row in grid)
        self.dead_count = sum(row.count(3) for row in grid)

    def get_statistics(self):
        snapshot = {
            "unprotected": self.unprotected_count,
            "protected": self.protected_count,
            "dead": self.dead_count
        }
        self.history.append(snapshot)
        return snapshot