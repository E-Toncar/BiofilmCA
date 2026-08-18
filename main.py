"""
    řízení simulace CAs
"""
from tools import Tools
from constants import Constants

def main():
    grid = Tools.create_grid()
    grid = Tools.seed_grid(grid)
    #print(f"Grid size: {Constants.rows} x {Constants.cols}")
    

    # add the rest of your simulation here
    # update cells
    # render visuals
    # collect statistics

if __name__ == "__main__":
    main()



