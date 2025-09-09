import numpy as np


def getGrid(model):
    grid = np.zeros((model.grid.width + 2, model.grid.height + 2), dtype=object)
    for content, (x, y) in model.grid.coord_iter():
        grid[x][y] = model.cells[x][y]
        if content != None:
            grid[x][y] = 2
    return grid
