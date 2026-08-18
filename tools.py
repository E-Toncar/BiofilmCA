"""
    Nástroje pro řízení simulace CA

"""
from constants import Constants

class Tools:

    def create_grid():
        return [[Constants.empty for _ in range(Constants.cols)] for _ in range(Constants.rows)]