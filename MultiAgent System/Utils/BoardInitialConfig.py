# Each digit represents a wall in the cell (up, right, down, left)
cells = [
    [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0]],
    [[0, 0, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 1, 0], [0, 1, 1, 0]],
    [[0, 0, 0, 1], [0, 1, 0, 0], [1, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0]],
    [[0, 0, 1, 1], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 1, 0]],
    [[1, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 1]],
    [[0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 1, 0], [0, 1, 1, 1]]
]

# [x, y, victim/falseAlarm]
POILocations = [[2, 4, 1], [5, 1, 0], [5, 8, 1]]

# [x, y]
fireLocations = [[2, 2], [2, 3], [3, 2], [3, 3], [3, 4], [3, 5], [4, 4], [5, 6], [5, 7], [6, 6]]

# [x1, y1, x2, y2]
doorLocations = [[1, 3, 1, 4], [2, 5, 2, 6], [2, 8, 3, 8], [3, 2, 3, 3], [4, 4, 5, 4],  [4, 6, 4, 7], [6, 5, 6, 6], [6, 7, 6, 8]]

# [x, y]
accessPoints = [[1, 6], [3, 1], [4, 8], [6, 3]]

# Añadir los puntos en los que pueden aparecer los bomberos
spawnPoints = []

ambulancePosition = []

boardConfig = {
    "cells": cells,
    "POILocations": POILocations,
    "fireLocations": fireLocations,
    "doorLocations": doorLocations,
    "accessPoints": accessPoints,
    "spwanPoints": spawnPoints,
    "ambulancePosition": ambulancePosition,
}
